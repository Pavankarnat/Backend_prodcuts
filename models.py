'''from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Float, Boolean
from typing import Optional
from sqlalchemy .ext.declarative import declarative_base
Base = declarative_base()
class product(Base):
    _tabelname_="product"
    id =Column(Integer, primary_key=True, index=True, autoincrement=True)
    name=Column(String, index=True)
    description=Column(String)
    price=Column(Float)
    is_offer=Column(Boolean, default=False)'''

from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    price: float
    is_offer: bool = False

'''class Product(BaseModel):
    id: Optional[int] = None  # Auto-generated if not provided
    name: str = Field(..., min_length=1, description="Product name")
    description: str = Field(..., min_length=1, description="Product description")
    price: float = Field(..., gt=0, description="Product price")
    is_offer: bool = Field(default=False, description="Is this product on offer")'''