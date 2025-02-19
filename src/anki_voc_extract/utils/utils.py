import re


def extract_korean(text: str) -> str:
    """Rephrase the front text in anki note. remove the [] symbols.

    Args:
        text (str): _description_

    Returns:
        _type_: _description_
    """
    # Define the regex pattern for Korean characters
    korean_pattern = re.compile(r"[\uac00-\ud7a3]+")
    # Find all Korean characters in the text
    korean_text = korean_pattern.findall(text)
    # Join all found Korean parts into a single string
    return " ".join(korean_text)
