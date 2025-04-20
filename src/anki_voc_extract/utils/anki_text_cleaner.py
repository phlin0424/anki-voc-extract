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
            input_text = self.__extract_target_language_text(input_text)

        if self.config.rm_html_path_flg:
            input_text = self.__remove_html_tags(input_text)

        return input_text

    def __extract_target_language_text(self, text: str) -> str:
        """Rephrase the front text in anki note. remove the [] symbols.

        Args:
            text (str): _description_

        Returns:
            str: _description_
        """
        # Language-specific character ranges
        language_patterns = {
            "ko": r"[\uac00-\ud7a3]+",  # Korean Hangul
            "ja": r"[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9faf]+",  # Japanese (Hiragana, Katakana, Kanji)
            "zh": r"[\u4e00-\u9fff]+",  # Chinese
            # Add more languages as needed
        }

        # Get pattern for target language
        pattern = language_patterns.get(self.config.target_lang, r"[\uac00-\ud7a3]+")  # Default to Korean

        # Extract text in target language
        target_text = re.compile(pattern).findall(text)

        # Join all found parts into a single string
        return " ".join(target_text)

    def __remove_html_tags(self, text: str) -> str:
        """Remove html tags in the given string.

        Args:
            text (_type_): _description_

        Returns:
            str: _description_
        """
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()
