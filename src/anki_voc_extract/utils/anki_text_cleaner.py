import re

from bs4 import BeautifulSoup
from injector import inject

from anki_voc_extract.configs import AnkiTextCleanerConfig


class AnkiTextCleaner:
    @inject
    def __init__(self, config: AnkiTextCleanerConfig) -> None:
        self.config = config

    def clean(self, input_text: str) -> str:
        """CLean the text.

        Args:
            input_text (str): _description_

        Returns:
            str: _description_
        """
        if self.config.rm_mp3_path_flg:
            input_text = self.__remove_mp3_path(input_text)

        if self.config.rm_html_path_flg:
            input_text = self.__remove_html_tags(input_text)

        return input_text

    def __remove_mp3_path(self, text: str) -> str:
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
