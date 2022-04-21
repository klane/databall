from functools import wraps

from sqlalchemy import CheckConstraint, Column
from sqlalchemy.orm import declared_attr


def positive_column(column_name, column_type, *args, **kwargs):
    constraint = CheckConstraint(f'{column_name} >= 0')
    return Column(column_name, column_type, constraint, *args, **kwargs)


_priority_order = 1


def priority_column(func):
    @wraps(func)
    @declared_attr
    def wrapper(cls):
        global _priority_order
        column = func(cls)
        column._creation_order = _priority_order
        _priority_order += 1
        return column

    return wrapper
