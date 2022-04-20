from sqlalchemy import Column, ForeignKey


def foreign_key(column, *args, **kwargs):
    return Column(column.type, ForeignKey(column), *args, **kwargs)
