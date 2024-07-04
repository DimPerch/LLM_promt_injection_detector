# LLM API Server

This document outlines how to interact with the API's available endpoints, specifically focusing on the `/check_output` endpoint.

There are two servers (one to set up in foreign countries such `USA`, `Netherlands`, etc., and one in `Russia`) to satisfy region restrictions for model using.

Access provided to:
- ChatGPT (`3.5-turbo`, `4o`, `4`)
- YandexGPT (`yandexgpt-lite`, `yandexgpt`, `yandexgpt-pro`)
- GigaChat (`GigaChat`)

## Setting up

### #1 Modules
```sh
sudo apt install screen
```
```sh
pip install gunicorn
```

### #2 Starting
```sh
screen -S camp_project_session
```

```sh
gunicorn -w 4 -b 0.0.0.0:8989 app:app
```

And, then press `Ctrl-A` following by `D` to detach from the session.


## API Documentation
### Endpoints

- `output` (required): The output of a large language model to process.
- `header` (optional): Additional system information to say the model its task.
- `model` (optional): Specifies the model to be used for processing. Defaults default (`gpt4o`, `yandexgpt`, `GigaChat` accordingly) model if not specified.

#### Request Format

The request should be a JSON object with the following keys:

```json
{
  "output": "Your main content here",
  "header": "Optional header content",
  "model": "Optional model identifier"
}