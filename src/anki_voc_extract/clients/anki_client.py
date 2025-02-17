import requests
from injector import inject

from anki_voc_extract.configs import AnkiClientConfig


class AnkiClient:
    @inject
    def __init__(self, config: AnkiClientConfig) -> None:
        self.config = config

    def get_api_url(self) -> str:
        """Return a api url.

        Returns:
            str: API url for AnkiConnector.
        """
        return self.config.ankiconnector_url

    def get_note_ids(self) -> list:
        """Get all the flash cards stored in the specified deck.

        Returns:
            list: _description_
        """
        payload = {
            "action": "findNotes",
            "version": 6,
            "params": {"query": f"deck:{self.config.deck_name}"},
        }

        return (
            requests.post(
                self.config.ankiconnector_url,
                json=payload,
                timeout=self.config.timeout,
            )
            .json()
            .get("result")
        )
