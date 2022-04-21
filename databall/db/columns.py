from sqlalchemy import CheckConstraint, Column


def positive_column(column_name, column_type, *args, **kwargs):
    constraint = CheckConstraint(f'{column_name} >= 0')
    return Column(column_name, column_type, constraint, *args, **kwargs)


_priority_order = 1


class PriorityColumn(Column):
    def __init__(self, *args, **kwargs):
        global _priority_order
        super().__init__(*args, **kwargs)
        self._creation_order = _priority_order
        _priority_order += 1
