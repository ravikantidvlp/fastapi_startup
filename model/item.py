from pydantic import BaseModel
from typing import Union
class Item(BaseModel):
    itemname: str
    itemprice: float
    isactive: int