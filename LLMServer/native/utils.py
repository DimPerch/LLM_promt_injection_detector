import json
from pathlib import Path
from types import SimpleNamespace


BASE_DIR = Path(__file__).parent


class Secrets:
    def __init__(self) -> None:
        self.read()

    def read(self) -> None:
        with open(f"{str(BASE_DIR)}/.secrets", 'r') as file:
            for line in file.read().strip().split():
                if not line.strip():
                    continue
                key, value = map(lambda x: x.strip(), line.strip().split("=", 1))
                setattr(self, key, value)


def process_output(output: str) -> bool:
    return not output.lower().startswith("нет")