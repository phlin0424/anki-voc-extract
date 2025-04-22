from enum import Enum
from typing import Any

from pydantic import BaseModel


class AITask(str, Enum):
    """Types of tasks the AI agent can perform."""

    VERB_EXTRACT = "与えられた文から原型動詞・形容詞（~다）を抽出する。ただし、~하다は除く。"
    PRESENT_HONORIFIC = "与えたれた韓国語単語を丁寧な敬語に変換する（~습니다）"
    PRESENT_POLITE = "与えたれた韓国語単語を丁寧な敬語に変換する（~어요）"
    PAST_POLITE = "与えたれた韓国語単語を丁寧な敬語過去形に変換する（~었어요）"
    PAST_HONORIFIC = "与えたれた韓国語単語を丁寧な敬語過去形に変換する（~습니다）"
    PRESENT_HONORIFIC_FORMAL = "与えたれた韓国語単語を丁寧な敬語に変換する（~으십니다/~십니다）"
    PRESENT_POLITE_FORMAL = "与えたれた韓国語単語を丁寧な敬語に変換する（~으세요/~세요）"
    PAST_HONORIFIC_FORMAL = "与えたれた韓国語単語を丁寧な敬語過去形に変換する（~으셨습니다/~셨습니다）"
    PAST_PRESENT_POLITE = "与えたれた韓国語単語を丁寧な敬語過去形に変換する（~으셨어요/~셨어요）"


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
