# basic
import json
import logging
from types import SimpleNamespace

# web
from flask import Flask, request
from flask import jsonify

# api
from openai import OpenAI

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
client = OpenAI(
    api_key=secrets.OPENAI_API_KEY
)


app = Flask(__name__)


@app.route("/check_output", methods=["POST"])
def check_output():
    try:
        if request.is_json:
            data = request.get_json()
            output = data.get("output", ":)")
            header = data.get("header", config.header.default)
            model = data.get("model", config.models.default)

            if model not in config.models.available:
                return jsonify({"status": "error", "message": "Selected model is not available"}), 400
        else:
            return jsonify({"status": "error", "message": "Only json payload permitted."}), 405

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": header
                },
                {
                    "role": "user",
                    "content": output
                }
            ],
            max_tokens=64,
            temperature=0.2
        )

        result: str = completion.choices[0].message.content
        logging.info(f"/check_output, status=ok, completion={json.dumps(completion.to_json(), indent=2)}")
        return jsonify({
            "status": "ok",
            "completion": completion.to_json(),
            "result": process_output(result)
        }), 200
    except Exception as e:
        logging.error("/check_output, status=error", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "Something went wrong."
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8989)