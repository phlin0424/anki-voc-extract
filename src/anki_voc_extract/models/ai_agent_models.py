from enum import Enum
from typing import Any

from pydantic import BaseModel


class AITask(str, Enum):
    """Types of tasks the AI agent can perform for Korean verb transformations."""

    VERB_EXTRACT = "与えられた文から原型の動詞・形容詞（〜다）を抽出してください。ただし、〜하다は除きます。"

    PRESENT_HONORIFIC = "与えられた韓国語の語幹を丁寧な敬語（〜습니다）に変換してください。"
    PRESENT_POLITE = "与えられた韓国語の語幹を丁寧な非敬語（〜어요）に変換してください。"

    PAST_POLITE = "与えられた韓国語の語幹を丁寧な非敬語の過去形（〜었어요）に変換してください。"
    PAST_HONORIFIC = "与えられた韓国語の語幹を丁寧な敬語の過去形（〜았습니다／었습니다）に変換してください。"

    PRESENT_HONORIFIC_FORMAL = (
        "与えられた韓国語の語幹をフォーマルな丁寧敬語（〜으십니다／〜십니다）に変換してください。"
    )
    PRESENT_POLITE_FORMAL = "与えられた韓国語の語幹をフォーマルな丁寧語（〜으세요／〜세요）に変換してください。"

    PAST_HONORIFIC_FORMAL = (
        "与えられた韓国語の語幹をフォーマルな丁寧敬語の過去形（〜으셨습니다／〜셨습니다）に変換してください。"
    )
    PAST_PRESENT_POLITE = "与えられた韓国語の語幹を丁寧な非敬語の尊敬過去形（〜으셨어요／〜셨어요）に変換してください。"


class AIRequest(BaseModel):
    """Model for an AI request."""

    task: AITask
    content: str
    source_lang: str
    target_lang: str
    additional_context: dict[str, Any] | None = None


class AIResponse(BaseModel):
    """Model for an AI response."""

    task: AITask
    content: str
    raw_response: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None
    success: bool = True
    error_message: str | None = None
