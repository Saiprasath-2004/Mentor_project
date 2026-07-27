from sqlalchemy.orm import DeclarativeBase


# Parent class tracked by SQLAlchemy
# Every model inherits from this base
class Base(DeclarativeBase):
    pass