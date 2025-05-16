import json

from fastapi import Depends, FastAPI

from anki_voc_extract.clients import AnkiClient
from anki_voc_extract.di import injector
from anki_voc_extract.models import AITask
from anki_voc_extract.utils import AIAgent
from anki_voc_extract.utils.anki_text_cleaner import AnkiTextCleaner

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
    anki_text_cleaner = injector.get(AnkiTextCleaner)
    card_contents = anki_client.get_random_verb_note_contents()
    return anki_text_cleaner.clean(card_contents.front)


@app.post("/transform_verb")
async def to_honorific_form(input_verb: str):
    ai_agent = injector.get(AIAgent)
    voc = ai_agent.generate_content(AITask.PRESENT_HONORIFIC_FORMAL, input_verb)
    result_dict = json.loads(voc)
    return result_dict["transformed_verb"]
