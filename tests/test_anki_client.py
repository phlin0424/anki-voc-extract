from unittest.mock import MagicMock, patch

import pytest
import requests

from anki_voc_extract.clients import AnkiClient
from anki_voc_extract.configs import AnkiClientConfig


@pytest.fixture
def anki_config():
    """Create a test configuration."""
    return AnkiClientConfig(
        ankiconnector_url="http://test-anki-server:8765",
        deck_name="TestDeck",
        timeout=5,
    )


@pytest.fixture
def anki_client(anki_config: AnkiClientConfig) -> AnkiClient:
    """Create AnkiClient instance with test config."""
    return AnkiClient(anki_config)


def test_get_api_url(anki_client: AnkiClient) -> None:
    """Test that get_api_url returns the correct URL."""
    assert anki_client.get_api_url() == "http://test-anki-server:8765"


@patch("requests.post")
def test_get_note_ids(mock_post, anki_client: AnkiClient) -> None:
    """Test get_note_ids with mocked requests.post."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": [123, 456, 789]}
    mock_post.return_value = mock_response

    # Call the method
    note_ids = anki_client.get_note_ids()

    # Verify the results
    assert note_ids == [123, 456, 789]

    # Verify the request was correctly formed
    mock_post.assert_called_once_with(
        "http://test-anki-server:8765",
        json={"action": "findNotes", "version": 6, "params": {"query": "deck:TestDeck"}},
        timeout=5,
    )


@patch("requests.post")
def test_get_note_contents(mock_post, anki_client: AnkiClient) -> None:
    """Test get_note_contents with mocked requests.post."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "result": [
            {"noteId": 123, "fields": {"表面": {"value": "안녕하세요"}, "裏面": {"value": "Hello"}}},
            {"noteId": 456, "fields": {"表面": {"value": "감사합니다"}, "裏面": {"value": "Thank you"}}},
        ]
    }
    mock_post.return_value = mock_response

    # Call the method
    note_contents = anki_client.get_note_contents([123, 456])

    # Verify the results
    assert len(note_contents) == 2
    assert note_contents[0].front == "안녕하세요"
    assert note_contents[0].back == "Hello"
    assert note_contents[0].note_id == 123
    assert note_contents[1].front == "감사합니다"
    assert note_contents[1].back == "Thank you"
    assert note_contents[1].note_id == 456

    # Verify the request was correctly formed
    mock_post.assert_called_once_with(
        "http://test-anki-server:8765",
        json={"action": "notesInfo", "version": 6, "params": {"notes": [123, 456]}},
        timeout=5,
    )


@patch("requests.post")
def test_get_note_contents_api_error(mock_post, anki_client: AnkiClient) -> None:
    """Test get_note_contents when API returns an error."""
    # Setup mock response with error
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"error": "Invalid note IDs"}
    mock_post.return_value = mock_response

    # Call the method and check for exception
    with pytest.raises(ValueError, match="Error: Invalid note IDs"):
        anki_client.get_note_contents([999])


@patch("requests.post")
def test_get_note_contents_http_error(mock_post, anki_client: AnkiClient) -> None:
    """Test get_note_contents when HTTP request fails."""
    # Setup mock response with non-200 status code
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_post.return_value = mock_response

    # Call the method and check for exception
    with pytest.raises(ValueError, match="Anki connector error"):
        anki_client.get_note_contents([123])


@patch("requests.post")
def test_get_note_contents_request_exception(mock_post, anki_client: AnkiClient) -> None:
    """Test get_note_contents when requests raises an exception."""
    # Setup mock to raise an exception
    mock_post.side_effect = requests.exceptions.ConnectionError("Connection refused")

    # Call the method and check for exception
    with pytest.raises(requests.exceptions.ConnectionError, match="Connection refused"):
        anki_client.get_note_contents([123])
