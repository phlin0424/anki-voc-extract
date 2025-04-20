import pytest

from anki_voc_extract.configs import AnkiTextCleanerConfig
from anki_voc_extract.utils.anki_text_cleaner import AnkiTextCleaner


@pytest.fixture
def anki_text_cleaner_config():
    return AnkiTextCleanerConfig(
        rm_mp3_path_flg=True,
        rm_html_path_flg=True,
        target_lang="ko",
    )


@pytest.fixture
def anki_text_cleaner(anki_text_cleaner_config: AnkiTextCleanerConfig) -> AnkiTextCleaner:
    return AnkiTextCleaner(anki_text_cleaner_config)


def test_clean_text_removes_mp3_tags(anki_text_cleaner: AnkiTextCleaner) -> None:
    """Test that the `clean` method of `AnkiTextCleaner` removes MP3 tags from the input text.

    This test ensures that when the input text contains an MP3 tag in the format
    `[sound:<filename>.mp3]`, the `clean` method correctly removes the tag and
    returns the cleaned text.

        anki_text_cleaner (AnkiTextCleaner): An instance of the `AnkiTextCleaner` class
        used to perform the text cleaning operation.

    Args:
        anki_text_cleaner (AnkiTextCleaner): _description_
    """
    input_text = "곧 만나요! [sound:naver-ea1a5e22-11b8aff9-3f2a16db-3641b665-eba36f27.mp3]"
    expected_output = "곧 만나요"
    assert anki_text_cleaner.clean(input_text) == expected_output, (
        f"Expected '{expected_output}', but got '{anki_text_cleaner.clean(input_text)}'"
    )


def test_clean_text_removes_html_tags(anki_text_cleaner: AnkiTextCleaner) -> None:
    """Test that the `clean` method of `AnkiTextCleaner` removes HTML tags from the input text.

    This test ensures that when the input text contains HTML tags like <div>, <p>, etc.,
    the `clean` method correctly removes the tags and returns the cleaned text.

    Args:
        anki_text_cleaner (AnkiTextCleaner): An instance of the `AnkiTextCleaner` class
        used to perform the text cleaning operation.
    """
    input_text = "<div>안녕하세요!</div> <p>반갑습니다.</p>"
    expected_output = "안녕하세요 반갑습니다"
    assert anki_text_cleaner.clean(input_text) == expected_output, (
        f"Expected '{expected_output}', but got '{anki_text_cleaner.clean(input_text)}'"
    )
