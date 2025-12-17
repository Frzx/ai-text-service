from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects import postgresql


class Label(Enum,str):

    postive = "positive"
    negative = "negative"

class Sentiment(SQLModel,table=True):
    __tablename__ = "sentiment"

    id: UUID = Field(
        sa_column= Column(
            postgresql.UUID,
            default= uuid4,
            primary_key=True,
        )
    )

    created_at: datetime = Field(
        sa_column= Column(
            postgresql.TIMESTAMP,
            default= datetime.now,
        )
    )

    sentiment: Label

    text: str