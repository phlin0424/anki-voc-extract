from injector import Binder, Module

from anki_voc_extract.client.anki_client import AnkiClient
from anki_voc_extract.config import Config


class ConfigModule(Module):
    def configure(self, binder: Binder) -> None:
        """Define the DI of Config module. Binding Config class to itself.

        Args:
            binder (_type_): _description_
        """
        binder.bind(Config, to=Config, scope=None)


class AnkiClientModule(Module):
    def configure(self, binder: Binder) -> None:
        """Define the DI module. Binding AnkiClient class to itself.

        Args:
            binder (Binder): _description_
        """
        binder.bind(AnkiClient, to=AnkiClient, scope=None)
