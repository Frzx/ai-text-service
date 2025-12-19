from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    text: str


class AnalyzeResponse(BaseModel):

    id: UUID
    text: str
    created_at: datetime
    label: str