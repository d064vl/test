
from sqlalchemy import String, Integer, DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
# from storeapi.schemas.Comment import CommentTable

from sqlalchemy import MetaData
from storeapi.schemas.Base import Base

class ProductTable(Base):
    """Create a test table."""

    __tablename__ = "products"

    idu: Mapped[int] = mapped_column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(120))
    amount: Mapped[int] = mapped_column(Integer)
    currency: Mapped[str] = mapped_column(String(120))
    quantity: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(String(120))
    availability_timestamp: Mapped[str] = mapped_column(String(20))


    def __repr__(self) -> str:
        """Define the model representation."""
        return f'PostTable({self.id}, "{self.name}")'
