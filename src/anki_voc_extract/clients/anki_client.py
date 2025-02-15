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
        return self.config.api_url

    def get_cards(self):
        payload = {"action": "notesInfo", "version": 6, "params": {"query": "deck:korean"}}

        return requests.post(self.config.api_url, json=payload, timeout=self.config.timeout)
