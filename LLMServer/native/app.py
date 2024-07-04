# basic
import uuid
import json
import logging
import requests
from types import SimpleNamespace

# web
from flask import Flask, request
from flask import jsonify

# others
from utils import BASE_DIR, Secrets, process_output


logging.basicConfig(
    filename=f"logger.log",
    filemode='a',
    level=logging.DEBUG,
    format="[%(asctime)s, %(levelname)s]: %(message)s"
)

config = json.load(
    open(str(BASE_DIR / "config.json"), 'r'),
    object_hook=lambda d: SimpleNamespace(**d)
)
secrets = Secrets()


app = Flask(__name__)


@app.route("/check_output_yandex", methods=["POST"])
def check_output_yandex():
    try:
        if request.is_json:
            data = request.get_json()
            output = data.get("output", ":)")
            header = data.get("header", config.yandex.header.default)
            model = data.get("model", config.yandex.models.default)

            if model not in config.yandex.models.available:
                return jsonify({"status": "error", "message": "Selected model is not available."}), 400
        else:
            return jsonify({"status": "error", "message": "Only json payload permitted."}), 405

        prompt = {
            "modelUri": f"gpt://{secrets.YANDEX_CATALOG_ID}/{model}",
            "completionOptions": {
                "stream": False,
                "temperature": 0.2,
                "maxTokens": "64"
            },
            "messages": [
                {
                    "role": "system",
                    "text": header
                },
                {
                    "role": "user",
                    "text": config.yandex.wrapping_format.format(output=output)
                }
            ]
        }


        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {secrets.YANDEX_API_KEY}"
        }

        response = requests.post(config.yandex.model_url, headers=headers, json=prompt)
        if not response.ok:
            logging.error(f"/check_output_yandex, status=error, status_code={response.status_code}, text={response.text}")
            return jsonify({
                "status": "error",
                "message": "Connection with the model cannot be established."
            }), 200
        
        completion = response.json()
        result: str = completion["result"]["alternatives"][0]["message"]["text"]
        logging.info(f"/check_output, status=ok, completion={json.dumps(completion, indent=2)}")
        return jsonify({
            "status": "ok",
            "completion": completion,
            "result": process_output(result)
        }), 200
    except Exception as e:
        logging.error("/check_output_yandex, status=error", exc_info=True)
        return jsonify({
            "status": "error"
        }), 500


def get_access_token_gigachat() -> str:
    payload="scope=GIGACHAT_API_PERS"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": str(uuid.uuid4()),
        "Authorization": f"Basic {secrets.GIGACHAT_AUTHORIZATION_DATA}"
    }

    response = requests.post(config.gigachat.access_token_url, headers=headers, data=payload, verify=False)
    if not response.ok:
        logging.error(f"/check_output_gigachat, status=error, status_code={response.status_code}, text={response.text}")
        return None
    return response.json()["access_token"]


@app.route("/check_output_gigachat", methods=["POST"])
def check_output_gigachat():
    try:
        if request.is_json:
            data = request.get_json()
            output = data.get("output", ":)")
            header = data.get("header", config.gigachat.header.default)
            model = data.get("model", config.gigachat.models.default)

            if model not in config.gigachat.models.available:
                return jsonify({"status": "error", "message": "Selected model is not available"}), 400
        else:
            return jsonify({"status": "error", "message": "Only json payload permitted."}), 405

        access_token = get_access_token_gigachat()
        if access_token is None:
            return jsonify({"status": "error", "message": "Connection with the gigachat cannot be established."}), 500

        payload = json.dumps({
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": config.gigachat.wrapping_format.format(header=header, output=output)
                }
            ],
            "n": 1,
            "stream": False,
            "max_tokens": 64,
            "repetition_penalty": 1,
            "temperature": 0.2
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.post(config.gigachat.model_url, headers=headers, data=payload, verify=False)
        if not response.ok:
            logging.error(f"/check_output_gigachat, status=error, status_code={response.status_code}, text={response.text}")
            return jsonify({
                "status": "error",
                "message": "Connection with the model cannot be established."
            }), 200

        completion = response.json()
        result: str = completion["choices"][0]["message"]["content"]
        logging.info(f"/check_output_gigachat, status=ok, completion={json.dumps(completion, indent=2)}")
        return jsonify({
            "status": "ok",
            "completion": completion,
            "result": process_output(result)
        }), 200
    except Exception as e:
        logging.error("/check_output_gigachat, status=error", exc_info=True)
        return jsonify({
            "status": "error"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8989)