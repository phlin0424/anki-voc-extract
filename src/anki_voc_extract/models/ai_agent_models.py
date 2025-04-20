from pydantic import BaseModel
from enum import Enum
from typing import Any


class AITask(str, Enum):
    """Types of tasks the AI agent can perform."""

    TRANSLATE = "translate"
    EXPLAIN_GRAMMAR = "explain_grammar"
    GENERATE_EXAMPLE = "generate_example"
    CATEGORIZE_VOCABULARY = "categorize_vocabulary"
    SUGGEST_TAGS = "suggest_tags"
    EXPLAIN_USAGE = "explain_usage"
    IDENTIFY_DIFFICULTY = "identify_difficulty"


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
