from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .order import Order
    from .order_product_associations import OrderProductAssociation


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)

    orders: Mapped[list["Order"]] = relationship(
        secondary="order_product_association",
        back_populates="products",

    )

    orders_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="product"
    )
