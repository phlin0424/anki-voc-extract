from enum import Enum

from pydantic import BaseModel, Field


class TargetLang(str, Enum):
    ko = "ko"


class AnkiTextCleanerConfig(BaseModel):
    rm_mp3_path_flg: bool = Field(default=True, description="If remove mp3 path text.")
    rm_html_path_flg: bool = Field(default=True, description="If remove the html tags.")
    target_lang: TargetLang = Field(default=TargetLang.ko)

    # TODO: an .env to define all these values
