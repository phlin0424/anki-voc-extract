import datetime

from injector import inject

from anki_voc_extract.clients import AnkiClient
from anki_voc_extract.configs import OutputterConfig
from anki_voc_extract.utils import AnkiTextCleaner


class Outputter:
    @inject
    def __init__(
        self,
        config: OutputterConfig,
        anki_client: AnkiClient,
        text_cleaner: AnkiTextCleaner,
    ) -> None:
        self.config = config
        self.client = anki_client
        self.text_cleaner = text_cleaner

    def output(self) -> None:
        """Output all the anki cards stored in Anki."""
        all_ids = self.client.get_note_ids()
        all_cards = self.client.get_note_contents(all_ids)

        # Clean the format
        clean_texts = [self.text_cleaner.clean(card.front) for card in all_cards]

        # Output the file
        dt_now = datetime.datetime.now(tz=datetime.UTC)
        fname = dt_now.strftime("%Y%m%d-%H%M") + ".txt"
        filepath = self.config.output_path / fname

        with filepath.open("w") as f:
            for text in clean_texts:
                f.write(text + "\n")
