from injector import Binder, Module, provider, singleton

from anki_voc_extract.clients import AnkiClient
from anki_voc_extract.configs import AnkiClientConfig, AnkiTextCleanerConfig, ConfigFactory, OutputterConfig


class ConfigModule(Module):
    """Module for providing all configuration dependencies."""

    @singleton
    @provider
    def provide_anki_client_config(self) -> AnkiClientConfig:
        """Provide the AnkiClientConfig instance.

        Returns:
            AnkiClientConfig: Singleton instance from factory
        """
        return ConfigFactory.get_anki_client_config()

    @singleton
    @provider
    def provide_anki_text_cleaner_config(self) -> AnkiTextCleanerConfig:
        """Provide the AnkiTextCleanerConfig instance.

        Returns:
            AnkiTextCleanerConfig: Singleton instance from factory
        """
        return ConfigFactory.get_anki_text_cleaner_config()

    @singleton
    @provider
    def provide_outputter_config(self) -> OutputterConfig:
        """Provide the OutputterConfig instance.

        Returns:
            OutputterConfig: Singleton instance from factory
        """
        return ConfigFactory.get_outputter_config()


class ClientModule(Module):
    """Module for providing all client dependencies."""

    @singleton
    @provider
    def provide_anki_client(self, config: AnkiClientConfig) -> AnkiClient:
        """Provide the AnkiClient instance with injected config.

        Args:
            config: The AnkiClient configuration

        Returns:
            AnkiClient: Singleton AnkiClient instance
        """
        return AnkiClient(config)
