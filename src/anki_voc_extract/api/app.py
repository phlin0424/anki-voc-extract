from fastapi import FastAPI

from anki_voc_extract.clients import AnkiClient
from anki_voc_extract.di import injector

# FastAPIアプリケーションの初期化
app = FastAPI(
    title="MCP API",
    description="API for managing the MCP system",
    version="0.1.0",
)


@app.get("/random_note")
async def get_random_note():
    """Get a random note from the Anki."""
    anki_client = injector.get(AnkiClient)
    card_contents = anki_client.get_random_verb_note_contents()

    return card_contents.front
