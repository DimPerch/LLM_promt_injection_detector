import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gemini_api import GeminiAPI  

class CanaryDetector:
    def __init__(self):
        self.canary_phrase = "flibbertigibbet"
        self.gemini_api = GeminiAPI()
    
    def check(self, prompt: str) -> bool:
        """
        Function to check prompt injection

        :param prompt: Input prompt to be checked
        :return: True if injection detected, False if injection undetected
        """
        modified_prompt = prompt + " " + self.canary_phrase
        
        response = self.gemini_api.generate_content(modified_prompt)
        if response is None:
            return False
        return self.canary_phrase in response