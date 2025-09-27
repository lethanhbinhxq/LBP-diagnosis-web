# core/soft_delete.py
from sqlalchemy import Column, Boolean
from sqlalchemy.orm import declared_attr

class SoftDeleteMixin:
    deleted = Column(Boolean, default=False, nullable=False)

    @declared_attr
    def __mapper_args__(cls):
        return {
            "eager_defaults": True  # ensures default values are applied
        }
