from injector import inject

from anki_voc_extract.config import Config


@inject
class AnkiClient:
    @inject
    def __init__(self, config: Config):
        self.config = Config

    def get_api_url(self):
        return self.config.api_url
