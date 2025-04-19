import requests
from injector import inject

from anki_voc_extract.configs import AnkiClientConfig
from anki_voc_extract.models import AnkiKoreanCardModel


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

    def get_note_ids(self) -> list[int]:
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

    def get_note_contents(self, note_id: list[int]) -> list[AnkiKoreanCardModel]:
        """Get a note content according a given note id.

        Args:
            note_id (list[int]): the anki note id.
        """
        # Prepare the payload to fetch the note details
        payload = {
            "action": "notesInfo",  # Action to get note information
            "version": 6,  # Version of the AnkiConnect API
            "params": {
                "notes": note_id  # Provide a list of note IDs (even if it's just one)
            },
        }

        # Send the request to AnkiConnect
        response = requests.post(self.config.ankiconnector_url, json=payload, timeout=self.config.timeout)

        # Check if the response is successful
        if response.status_code == 200:
            # Fetch the requested results
            response_json = response.json()

            # Raise error when something goes wrong
            if response_json.get("error") is not None:
                raise ValueError(f"Error: {response_json['error']}")

            # Fetch the results field from the response
            results = response_json.get("result")

            # Compose the return values
            return [
                AnkiKoreanCardModel(
                    front=result.get("fields").get("表面").get("value"),
                    back=result.get("fields").get("裏面").get("value"),
                    note_id=result.get("noteId"),
                )
                for result in results
            ]

        raise ValueError("Anki connector error")
