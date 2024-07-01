import os
from anthropic import Anthropic, APIError
from typing import Optional, List, Any
import base64

# Set this environment variable to suppress tokenizer warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"

class Claude:
    def __init__(self, model: str, api_key: Optional[str] = None) -> None:
        self.api_key = api_key
        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        self.context_window = self._get_context_window(model)
        self.max_tokens = 1000

    def _get_context_window(self, model: str) -> int:
        context_windows = {
            "claude-3-5-sonnet-20240620": 200000,
            "claude-3-opus-20240229": 200000,
            "claude-3-sonnet-20240229": 200000,
            "claude-2.1": 100000,
            "claude-2.0": 100000,
            "claude-instant-1.2": 100000,
        }
        return context_windows.get(model, 100000)

    def _prepare_messages(self, messages: List[Any]) -> List[dict]:
        prepared_messages = []
        for message in messages:
            if isinstance(message, dict) and 'role' in message and 'content' in message:
                prepared_messages.append({
                    'role': message['role'],
                    'content': str(message['content'])
                })
            else:
                print(f"Skipping invalid message: {message}")
        return prepared_messages

    def chat(self, messages: List[Any], **kwargs) -> str:
        try:
            prepared_messages = self._prepare_messages(messages)
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=prepared_messages,
                **kwargs
            )
            print(f"Response type: {type(response)}")
            print(f"Response content: {response.content}")
            return response.content[0].text if response.content else ""
        except APIError as e:
            if "credit balance is too low" in str(e):
                print("Error: Insufficient credits. Please upgrade your Anthropic account or purchase more credits.")
            else:
                print(f"An error occurred during chat: {e}")
            return ""
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return ""

    def complete(self, prompt: str, **kwargs) -> str:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            print(f"Response type: {type(response)}")
            print(f"Response content: {response.content}")
            return response.content[0].text if response.content else ""
        except APIError as e:
            if "credit balance is too low" in str(e):
                print("Error: Insufficient credits. Please upgrade your Anthropic account or purchase more credits.")
            else:
                print(f"An error occurred during completion: {e}")
            return ""
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return ""

    def chat_with_vision(self, messages: List[Any], images: List[str], **kwargs) -> str:
        try:
            prepared_messages = self._prepare_messages(messages)
            for image in images:
                prepared_messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": base64.b64encode(image).decode()
                            }
                        }
                    ]
                })
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=prepared_messages,
                **kwargs
            )
            print(f"Response type: {type(response)}")
            print(f"Response content: {response.content}")
            return response.content[0].text if response.content else ""
        except APIError as e:
            if "credit balance is too low" in str(e):
                print("Error: Insufficient credits. Please upgrade your Anthropic account or purchase more credits.")
            else:
                print(f"An error occurred during chat with vision: {e}")
            return ""
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return ""

    def get_model_name(self) -> str:
        return self.model

    def get_context_window(self) -> int:
        return self.context_window

    def get_max_tokens(self) -> int:
        return self.max_tokens