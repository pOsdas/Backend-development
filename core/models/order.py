from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .product import Product
    from .order_product_associations import OrderProductAssociation


class Order(Base):
    promocode: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now,
    )
    # ### this
    products: Mapped[list["Product"]] = relationship(
        secondary="order_product_association",
        back_populates="orders",
    )

    # ### or this
    # association between Parent -> Association -> Child
    products_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order"
    )


