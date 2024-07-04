from time import sleep

import YandexGPT_API


SYSTEM_PROMPT_FILE = 'system_prompt.txt'


class LLM_detector:
    def __init__(self):
        self.gpt = YandexGPT_API.YandexGPTEmbeddings()

    def answer(self, user_prompt):
        try:
            with open(SYSTEM_PROMPT_FILE, "r", encoding="utf-8") as file:
                system_prompt = file.read()
        except Exception as e:
            print(f"Failed to read prompt file: {e}")
            exit(1)

        message = [
            {
                "role": "system",
                "text": system_prompt
            },
            {
                "role": "user",
                "text": user_prompt
            }
        ]

        try:
            answer = self.gpt.make_request(message, temperature=0.3, max_tokens=512)
        except Exception as e:
            print(f"Error occurred: {e}")
            answer = ''

        return answer

    def check(self, text) -> bool:
        """
        Function fot check promt injection

        :return True if injection detected
                False if injection undetected
        """
        result = []
        print(result)
        for _ in range(3):
            result.append(self.answer(text))
            sleep(1)
        print(result)
        return result.count('NO') < 3




