from google import genai
from google.genai.types import GenerateContentConfig, HttpOptions
from injector import inject

from anki_voc_extract.configs import AIAgentConfig
from anki_voc_extract.models import AITask


class AIAgent:
    """Agent for handling AI-assisted language learning tasks."""

    @inject
    def __init__(self, config: AIAgentConfig) -> None:
        """Initialize the AI Agent.

        Args:
            config: Configuration for the AI agent.
        """
        self.config = config
        self._initialize_client()

    def _initialize_client(self) -> None:
        """Initialize the Gemini API client."""
        if not self.config.project or not self.config.location:
            raise ValueError("Gemini project and location are required")

        self.client = genai.Client(
            vertexai=True,
            project=self.config.project,
            location=self.config.location,
            http_options=HttpOptions(api_version="v1"),
        )

    def generate_content(self, ai_task: AITask, contents: str) -> str:
        """Generate content using the Gemini API.

        Args:
            ai_task (AITask): _description_
            contents (str): _description_

        Returns:
            str: _description_
        """
        response_schema = {
            "type": "object",
            "properties": {
                "transformed_verb": {"type": "string"},
            },
            "required": ["transformed_verb"],
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
