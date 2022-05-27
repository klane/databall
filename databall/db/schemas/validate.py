from pydantic import BaseModel


def validate_data_frame(schema, df):
    class DataFrameModel(BaseModel):
        __root__: list[schema]

    df_dict = df.to_dict(orient='records')
    DataFrameModel.parse_obj(df_dict)
