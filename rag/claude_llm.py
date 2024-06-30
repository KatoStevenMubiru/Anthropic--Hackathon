from anthropic import Anthropic
from typing import Optional, List, Any

class Claude:
    def __init__(self, model: str, api_key: Optional[str] = None) -> None:
        self.api_key = api_key
        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        self.context_window = self._get_context_window(model)
        self.max_tokens = 1000

    def _get_context_window(self, model: str) -> int:
        context_windows = {
            "claude-3-opus-20240229": 200000,
            "claude-3-sonnet-20240229": 200000,
            "claude-2.1": 100000,
            "claude-2.0": 100000,
            "claude-instant-1.2": 100000,
        }
        return context_windows.get(model, 100000)

    def chat(self, messages: List[Any], **kwargs) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=0,
            messages=messages,
            **kwargs
        )
        return response.content[0].text

    def complete(self, prompt: str, **kwargs) -> str:
        response = self.client.completions.create(
            model=self.model,
            max_tokens_to_sample=self.max_tokens,
            temperature=0,
            prompt=f"\n\nHuman: {prompt}\n\nAssistant:",
            **kwargs
        )
        return response.completion