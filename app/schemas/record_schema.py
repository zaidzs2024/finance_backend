from pydantic import BaseModel
from datetime import datetime

class RecordCreate(BaseModel):
    amount: float
    type: str
    category: str
    date: datetime
    note: str