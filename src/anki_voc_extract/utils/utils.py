import re

from bs4 import BeautifulSoup

from anki_voc_extract.configs import AnkiTextCleanerConfig


class AnkiTextCleaner:
    def __init__(self, config: AnkiTextCleanerConfig) -> None:
        self.config = config

    def clean(self) -> str:
        """Return a clean text w/o additional symbols.

        Returns:
            str: Clean text
        """
        input_text = self.config.text
        input_text = self.__remove(input_text)
        return self.__remove_html_tags(input_text)

    def __remove(self, text: str) -> str:
        """Rephrase the front text in anki note. remove the [] symbols.

        Args:
            text (str): _description_

        Returns:
            str: _description_
        """
        # Define the regex pattern for Korean characters
        korean_pattern = re.compile(r"[\uac00-\ud7a3]+")
        # Find all Korean characters in the text
        korean_text = korean_pattern.findall(text)
        # Join all found Korean parts into a single string
        return " ".join(korean_text)

    def __remove_html_tags(self, text: str) -> str:
        """Remove html tags in the given string.

        Args:
            text (_type_): _description_

        Returns:
            str: _description_
        """
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()
