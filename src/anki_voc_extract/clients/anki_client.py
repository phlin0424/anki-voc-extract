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

    def get_note_ids(self) -> None | list:
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

    # Function to retrieve content of a note by its note_id
    def get_note_content(self, note_id: int) -> None | list:
        """Get a note content according a given note id.

        Args:
            note_id (int): the anki note id.
        """
        # Prepare the payload to fetch the note details
        payload = {
            "action": "notesInfo",  # Action to get note information
            "version": 6,  # Version of the AnkiConnect API
            "params": {
                "notes": [note_id]  # Provide a list of note IDs (even if it's just one)
            },
        }

        # Send the request to AnkiConnect
        response = requests.post(self.config.ankiconnector_url, json=payload, timeout=self.config.timeout)

        # Check if the response is successful
        if response.status_code == 200:
            result = response.json()
            if result.get("error") is not None:
                # Raise error when something goes wrong
                raise ValueError(f"Error: {result['error']}")

            note_info = result["result"][0]  # Since we asked for a single note ID, access the first element
            # Retrieve and print the note fields (e.g., Front and Back)
            return note_info["fields"]

        raise ValueError("Anki connector error")
