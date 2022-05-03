from sqlalchemy import CheckConstraint, Column, Enum


class PositiveColumn(Column):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._constraints = set()

    @property
    def constraints(self):
        if self.name is not None and len(self._constraints) == 0:
            constraint = CheckConstraint(f'{self.name} >= 0')
            self._constraints.add(constraint)
            constraint._set_parent(self)

        return self._constraints

    @constraints.setter
    def constraints(self, constraints):
        self._constraints = constraints


_priority_order = 1


class PriorityColumn(Column):
    def __init__(self, *args, **kwargs):
        global _priority_order
        super().__init__(*args, **kwargs)
        self._creation_order = _priority_order
        _priority_order += 1


class ValuesEnum(Enum):
    def __init__(self, *enums, **kwargs):
        kwargs['values_callable'] = lambda enum: [e.value for e in enum]
        super().__init__(*enums, **kwargs)
