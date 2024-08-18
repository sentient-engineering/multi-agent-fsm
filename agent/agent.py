from openai import OpenAI
from pydantic import BaseModel
from typing import Type

class Agent:
    def __init__(self, name: str, system_prompt: str, input_format: Type[BaseModel], output_format: Type[BaseModel], keep_message_history: bool = True):
        self.name = name
        self.messages = [{"role": "system", "content": system_prompt}]
        self.client = OpenAI()
        self.keep_message_history = keep_message_history
        self.input_format = input_format
        self.output_format = output_format

    def run(self, input_data: BaseModel) -> BaseModel:
        if not isinstance(input_data, self.input_format):
            raise ValueError(f"Input data must be of type {self.input_format.__name__}")

        self.messages.append({"role": "user", "content": input_data.model_dump_json()})
        
        
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=self.messages,
            response_format=self.output_format,
        )
       
        
        response_content: self.output_format = response.choices[0].message.parsed
        
        if self.keep_message_history:
            self.messages.append({"role": "assistant", "content": response_content.model_dump_json()})
        
        return response_content