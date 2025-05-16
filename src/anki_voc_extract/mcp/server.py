from mcp.server.fastmcp import FastMCP

from anki_voc_extract.clients import AnkiClient
from anki_voc_extract.di import injector
from anki_voc_extract.utils.anki_text_cleaner import AnkiTextCleaner

# "hello" という名前のサーバを作成
mcp = FastMCP("AnkiMCPServer")


# MCPツールとして関数を登録
@mcp.tool()
async def get_random_anki_korean_word() -> str:
    """Get a random note from the Anki."""
    anki_client = injector.get(AnkiClient)
    card_contents = anki_client.get_random_verb_note_contents()
    anki_text_cleaner = injector.get(AnkiTextCleaner)

    return anki_text_cleaner.clean(card_contents.front)


if __name__ == "__main__":
    mcp.run(transport="stdio")
    # mcp.run(transport="sse")
