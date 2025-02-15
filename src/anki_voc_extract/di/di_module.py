from injector import Binder, Module

from anki_voc_extract.clients import AnkiClient
from anki_voc_extract.configs import AnkiClientConfig


class AnkiClientConfigModule(Module):
    def configure(self, binder: Binder) -> None:
        """Define the DI of AnkiCLientConfig module. Binding Config class to itself.

        Args:
            binder (_type_): _description_
        """
        binder.bind(AnkiClientConfig, to=AnkiClientConfig, scope=None)


class AnkiClientModule(Module):
    def configure(self, binder: Binder) -> None:
        """Define the DI module. Binding AnkiClient class to itself.

        Args:
            binder (Binder): _description_
        """
        binder.bind(AnkiClient, to=AnkiClient, scope=None)
