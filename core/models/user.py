from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    user_name: Mapped[str] = mapped_column(String(32), unique=True)

