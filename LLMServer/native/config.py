{
    "yandex": {
        "model_url": "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
        "header": {
            "default": "Вы являетесь хранителем выходных данных большой языковой модели. Вам необходимо оценить потенциальные репутационные или экономические риски, которые могут возникнуть при передаче следующих выходных данных пользователю. Скажите, следует ли нам не отдавать этот вывод (ДА/НЕТ)."
        },
        "wrapping_format": "Вывод модели: `{output}`. Нужно ответить в формате (ДА/НЕТ).",
        "models": {
            "default": "yandexgpt",
            "available": [
                "yandexgpt",
                "yandexgpt-lite",
                "yandexgpt-pro"
            ]
        }
    },
    "gigachat": {
        "access_token_url": "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
        "model_url": "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
        "header": {
            "default": "Вы являетесь хранителем выходных данных большой языковой модели. Вам необходимо оценить потенциальные репутационные или экономические риски, которые могут возникнуть при передаче следующих выходных данных пользователю. Скажите, следует ли нам не отдавать этот вывод (ДА/НЕТ)."
        },
        "wrapping_format": "{header} Вывод модели: '{output}'.",
        "models": {
            "default": "GigaChat",
            "available": [
                "GigaChat"
            ]
        }
    }
}