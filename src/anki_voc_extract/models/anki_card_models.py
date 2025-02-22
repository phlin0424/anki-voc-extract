from pydantic import BaseModel


class AnkiKoreanCardModel(BaseModel):
    front: str
    back: str
    note_id: int
