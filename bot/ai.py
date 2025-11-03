import requests
import os
import re

from dotenv import load_dotenv

CONFIG_SYSTEM_MESSAGE =\
    """
Ты эксперт в области DevOps и анализа файлов конфигураций Terraform.
Проанализируй этот .tf файл на корректность и безопасность.
Дай ответ можно ли запускать его (yes/no) и комментарий. Отвечай ТОЛЬКО на английском.
Дай ответ в формате json. Пример: {answer:"yes/no", comment:"Configuration is good"}
"""

LOGS_SYSTEM_MESSAGE =\
'''
Ты эксперт в области анализа логов. 
Твоя задача проанализировать логи и дать комментарии и советы как исправить ошибки.
Отвечай ТОЛЬКО на английском.
'''

load_dotenv()

id_key_load = os.getenv("ID_KEY")
key_load = os.getenv("KEY")

def send_request_to_yandex_gpt(text, context, id_key=id_key_load, key=key_load):

    prompt = {
        "modelUri": f"gpt://{id_key}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "1000"
        },
        "messages": [
            {
                "role": "system",
                "text": context
            },
            {
                "role": "user",
                "text": text
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {key}"
    }

    try:
        response = requests.post(url, headers=headers, json=prompt)
        response.raise_for_status()  # Проверка на ошибки HTTP
        result_text = response.json()['result']['alternatives'][0]['message']['text']
        return result_text
    except Exception as e:
        print(f"Ошибка при отправке запроса к YandexGPT: {e}")
        return None


def get_clean_flask_logs(log_path) -> str:
    if not os.path.exists(log_path):
        return "❌ File flask.log is not found."

    try:
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        cleaned_lines = []
        for line in lines:
            if not line.strip():
                continue

            cleaned = re.sub(
                r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(,\d+)?\s*(DEBUG|INFO|WARNING|ERROR|CRITICAL)?\s*[:\-]?\s*",
                "",
                line.strip()
            )
            cleaned_lines.append(cleaned)

        return "\n".join(cleaned_lines).strip()

    except Exception as e:
        return f"⚠️ Error during the reading logs: Flask: {e}"

def get_clean_terraform_logs(log_path) -> str:

    if not os.path.exists(log_path):
        return "❌ File terraform.log is not found."

    try:
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        cleaned_lines = []
        for line in lines:
            if "WARN" in line:
                cleaned = line.split("WARN")[1]
                cleaned_lines.append(cleaned)
            else:
                continue
        return "\n".join(cleaned_lines).strip().replace("]  ","")

    except Exception as e:
        return f"⚠️ Error during the reading logs Terraform: {e}"


