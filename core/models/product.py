from .base import Base

from sqlalchemy.orm import Mapped, mapped_column


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
