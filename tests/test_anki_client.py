from anki_voc_extract.clients import AnkiClient
from anki_voc_extract.di import injector
from anki_voc_extract.configs import AnkiClientConfig
import pytest
from unittest.mock import MagicMock
from anki_voc_extract.models import AnkiKoreanCardModel


@pytest.fixture
def mock_config():
    return AnkiClientConfig(
        ankiconnector_url="http://127.0.0.1:8765",
        deck_name="TestDeck",
        timeout=5,
    )


@pytest.fixture
def mock_anki_client(mock_config):
    client = AnkiClient(mock_config)
    client.get_api_url = MagicMock(return_value=mock_config.ankiconnector_url)
    client.get_note_ids = MagicMock(return_value=[123, 456])
    client.get_note_contents = MagicMock(
        return_value=[
            AnkiKoreanCardModel(front="Front1", back="Back1", note_id=123),
            AnkiKoreanCardModel(front="Front2", back="Back2", note_id=456),
        ]
    )
    return client


def test_get_api_url(mock_anki_client):
    assert mock_anki_client.get_api_url() == "http://127.0.0.1:8765"


def test_get_note_ids(mock_anki_client):
    note_ids = mock_anki_client.get_note_ids()
    assert note_ids == [123, 456]


def test_get_note_contents(mock_anki_client):
    note_contents = mock_anki_client.get_note_contents([123, 456])
    assert len(note_contents) == 2
    assert note_contents[0].front == "Front1"
    assert note_contents[0].back == "Back1"
    assert note_contents[0].note_id == 123
    assert note_contents[1].front == "Front2"
    assert note_contents[1].back == "Back2"
    assert note_contents[1].note_id == 456


def test_get_note_contents_error_handling(mock_config):
    client = AnkiClient(mock_config)
    client.get_note_contents = MagicMock(side_effect=ValueError("Anki connector error"))
    with pytest.raises(ValueError, match="Anki connector error"):
        client.get_note_contents([789])
