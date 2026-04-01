from typing import Iterator
from google import genai
from google.genai import types
from .base import BaseProvider, Message


class GoogleProvider(BaseProvider):
    name = "Google"
    max_context_tokens = 1048576

    def __init__(self, api_key: str, model: str = "", base_url: str = ""):
        # Use http_options only if base_url is provided
        options = {"api_key": api_key}
        if base_url:
            options["http_options"] = {"base_url": base_url}
        
        self.client = genai.Client(**options)
        self.model = model or "gemini-2.5-flash"

    def stream_chat(self, messages: list[Message], system: str = "") -> Iterator[str]:
        contents = []
        for m in messages:
            role = "user" if m.role == "user" else "model"
            contents.append(types.Content(role=role, parts=[types.Part.from_text(text=m.content)]))

        config = None
        if system:
            config = types.GenerateContentConfig(
                system_instruction=system
            )

        response = self.client.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=config
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text

    def list_models(self) -> list[str]:
        try:
            models = []
            for m in self.client.models.list():
                if "generateContent" in m.supported_generation_methods:
                    name = m.name
                    if name.startswith("models/"):
                        name = name[len("models/"):]
                    models.append(name)
            return sorted(models)
        except Exception:
            return ["gemini-2.5-flash", "gemini-3.1-flash-lite-preview", "gemini-3.1-pro-preview", "gemini-2.0-flash"]
