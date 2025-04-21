from anki_voc_extract import api
from google import genai
from google.genai.types import GenerateContentConfig, HttpOptions
from injector import inject

from anki_voc_extract.configs import AIAgentConfig
from anki_voc_extract.models import AITask


class AIAgent:
    """Agent for handling AI-assisted language learning tasks."""

    @inject
    def __init__(self, config: AIAgentConfig):
        """Initialize the AI Agent.

        Args:
            config: Configuration for the AI agent.
        """
        self.config = config
        self._initialize_client()

    def _initialize_client(self) -> None:
        """Initialize the Gemini API client."""
        if not self.config.gemini_api_key:
            raise ValueError("Gemini API key is required")

        self.client = genai.Client(
            vertexai=True,
            project=self.config.project,
            api_key=self.config.gemini_api_key,
            location=self.config.location,
            http_options=HttpOptions(api_version="v1"),
        )

    def generate_content(self, ai_task: AITask, contents: str) -> str:
        response_schema = {
            "type": "object",
            "properties": {
                "greeting": {"type": "string"},
            },
            "required": ["greeting"],
        }
        response = self.client.models.generate_content(
            model=self.config.gemini_model_name,
            contents=contents,
            config=GenerateContentConfig(
                system_instruction=ai_task.value,
                temperature=0.4,
                response_mime_type="application/json",
                response_schema=response_schema,
            ),
        )

        return "\n".join([p.text for p in response.candidates[0].content.parts if p.text])
