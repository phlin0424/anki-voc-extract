from pydantic import BaseModel, Field


class AnkiTextCleanerConfig(BaseModel):
    text: str = Field(default="", description="input text fetched from Anki front card.")
