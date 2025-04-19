import argparse

from injector import inject

from anki_voc_extract.configs import BaseConfig


class ArgumentParserInterface:
    @inject
    def __init__(self, config: BaseConfig, parser: argparse.ArgumentParser) -> None:
        self.config = config
        self.parser = parser

    def create_parser(self) -> argparse.ArgumentParser:
        """Create a parser.

        Returns:
            argparse.ArgumentParser: _description_
        """
        # The arguments that are necessary
        group = self.parser.add_mutually_exclusive_group(required=True)

        group.add_argument(
            "-f",
            "--file",
            help="File containing text for Anki cards.",
        )
        group.add_argument(
            "-w",
            "--word",
            help="The vocabulary for Anki cards.",
        )

        self.parser.add_argument(
            "-d",
            "--deck_name",
            default=self.config.deck_name,
            help="Name of the Anki deck to which the cards will be added.",
        )
