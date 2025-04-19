from pathlib import Path

from pydantic import Field

from anki_voc_extract.configs.base_config import BaseConfig


class OutputterConfig(BaseConfig):
    output_path: Path = Field(default=Path("."), description="File path for the output file.")
