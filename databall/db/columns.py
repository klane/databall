from sqlalchemy import CheckConstraint, Enum
from sqlmodel import Field


def ConstrainedField(name, **kwargs):
    arg_to_constraint = {
        'gt': '>',
        'ge': '>=',
        'lt': '<',
        'le': '<=',
    }

    constraint_text = [
        f'{name} {arg_to_constraint[arg_name]} {arg_value}'
        for arg_name, arg_value in kwargs.items()
        if arg_name in arg_to_constraint
    ]
    constraint_text = ' AND '.join(constraint_text)

    if len(constraint_text) == 0:
        raise ValueError(
            f'Field {name} is unconstrained. One of ge, gt, le, lt should be specified.'
        )

    constraint = CheckConstraint(constraint_text)
    sa_column_args = kwargs.pop('sa_column_args', [])
    sa_column_args.append(constraint)
    return Field(sa_column_args=sa_column_args, **kwargs)


def EnumField(enum, create_constraint=True, use_values=False, **kwargs):
    values_callable = None if not use_values else lambda enum: [e.value for e in enum]
    column_type = Enum(
        enum,
        create_constraint=create_constraint,
        values_callable=values_callable,
    )

    sa_column_args = kwargs.pop('sa_column_args', [])
    sa_column_args.append(column_type)
    return Field(sa_column_args=sa_column_args, **kwargs)


def PositiveField(name, **kwargs):
    return ConstrainedField(name, ge=0, **kwargs)


def UniqueField(**kwargs):
    sa_column_kwargs = kwargs.pop('sa_column_kwargs', {})
    sa_column_kwargs['unique'] = True
    return Field(sa_column_kwargs=sa_column_kwargs, **kwargs)
