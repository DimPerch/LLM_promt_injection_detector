import requests
from typing import Final


FOREIGN_SERVER_ADDRESS: Final = "138.124.187.4:8989"
NATIVE_SERVER_ADDRESS: Final = "185.179.190.33:8989"

COEFFICIENTS: Final = {
    "chatgpt": 0.4,
    "yandexgpt": 0.4,
    "gigachat": 0.2
}


class LLM_detector:
    def __init__(self):
        pass

    def _check_chatgpt(self, output: str) -> bool | None:
        response = requests.post(f"{FOREIGN_SERVER_ADDRESS}/check_output", json={
            "output": output
        })
        if not response.ok:
            return None
        return response.json()["result"]
    
    def _check_yandexgpt(self, output: str) -> bool | None:
        response = requests.post(f"{NATIVE_SERVER_ADDRESS}/check_output_yandex", json={
            "output": output
        })
        if not response.ok:
            return None
        return response.json()["result"]
    
    def _check_gigachat(self, output: str) -> bool | None:
        response = requests.post(f"{NATIVE_SERVER_ADDRESS}/check_output_gigachat", json={
            "output": output
        })
        if not response.ok:
            return None
        return response.json()["result"]

    def check(self, output: str) -> bool:
        results = {
            "chatgpt": self._check_chatgpt(output),
            "yandexgpt": self._check_yandexgpt(output),
            "gigachat": self._check_gigachat(output)
        }
        if not any(map(lambda x: x is not None, results.values())):
            return False  # under discussion
        
        contributions = [
            (int(value) if value is not None else 0.5) * COEFFICIENTS[model]
            for model, value in results
        ]
        return bool(round(sum(contributions) / len(contributions)))
