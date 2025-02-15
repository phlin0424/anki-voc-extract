from injector import inject

from anki_voc_extract.config import Config


class AnkiClient:
    @inject
    def __init__(self, config: Config) -> None:
        self.config = config

    def get_api_url(self) -> str:
        """Return a api url.

        Returns:
            _type_: _description_
        """
        return self.config.api_url
