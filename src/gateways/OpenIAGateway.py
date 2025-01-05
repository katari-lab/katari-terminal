import os
from openai import OpenAI
import openai
import logging

LOGGER = logging.getLogger(__name__)

class OpenAIGateway:

    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI()

    def transcription_to_action(self, transcription: str):
        system_message ="""
            you are a expert system in a terminal commands and you need to fix audio transcriptions to the more accurate terminal command. 
            you must responde with the terminal command without additional comments or explanations.
        """
        user_prompt = transcription
        response = self.text_to_action(system_message=system_message, user_prompt=user_prompt, model_name="gpt-4o", temperature=0.5, max_tokens=2000)
        if len(response.choices) == 0:
            LOGGER.info("No response from OpenAI")
            return None
        content = response.choices[0].message.content
        if content.startswith("```bash"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.replace("\n", "")
        content = content.strip()
        return content

    def text_to_action(
        self, system_message: str, user_prompt: str, model_name="gpt-4o", temperature=0.8, max_tokens=2000
    ):
        try:
            chat_completion = self.client.chat.completions.create(
                temperature=temperature,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_prompt},
                ],
                model=model_name,
            )
            return chat_completion
        except Exception as ex:
            raise ValueError(f"Error with model {model_name}") from ex