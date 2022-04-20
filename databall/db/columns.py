from sqlalchemy import CheckConstraint, Column, ForeignKey


def foreign_key(column, *args, **kwargs):
    return Column(column.type, ForeignKey(column), *args, **kwargs)


def positive_column(column_name, column_type, *args, **kwargs):
    constraint = CheckConstraint(f'{column_name} >= 0')
    return Column(column_name, column_type, constraint, *args, **kwargs)
