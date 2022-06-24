import re

import pandas as pd
from pydantic import BaseModel
from sqlalchemy import inspect, select
from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel

from databall.db.session import Session, engine


class Base(SQLModel):
    @declared_attr
    def __tablename__(cls):
        return re.sub(r'([a-z\d])([A-Z])', r'\1_\2', cls.__name__).lower()

    @classmethod
    def populate(cls, *args, **kwargs):
        raise NotImplementedError(
            f'Method populate not implemented for table {cls.__tablename__}'
        )

    @classmethod
    @property
    def primary_keys(cls):
        with Session() as session, session.connection() as connection:
            columns = inspect(cls).primary_key
            query = select(columns)
            df = pd.read_sql(query, connection)

        return df

    @classmethod
    def save_df(cls, df):
        df_save = df.merge(cls.primary_keys, how='left', indicator=True)
        df_save = df_save[df_save._merge == 'left_only']

        if df_save.empty:
            print(f'All primary keys already in {cls.__tablename__}')
            return

        columns_to_drop = set(df_save.columns) - set(cls.__table__.columns.keys())
        df_save = df_save.drop(columns_to_drop, axis=1)
        cls.validate_df(df_save)
        df_save.to_sql(cls.__tablename__, engine, if_exists='append', index=False)
        print(f'Saved {len(df_save)} rows to {cls.__tablename__}')

    @classmethod
    def validate_df(cls, df):
        class DataFrameModel(BaseModel):
            __root__: list[cls]

        df_dict = df.to_dict(orient='records')
        DataFrameModel.parse_obj(df_dict)
