import os
from pathlib import Path
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

from dotenv import load_dotenv

from terraform.terraform_runner import run_terraform
from terraform.terraform_get_config import read_terraform_config
from ai import (
    send_request_to_yandex_gpt,
    CONFIG_SYSTEM_MESSAGE,
    LOGS_SYSTEM_MESSAGE,
    get_clean_flask_logs,
    get_clean_terraform_logs
)
import json

app_log_file = Path(__file__).resolve().parent.parent / "logs" / "flask.log"
terraform_log_file = Path(__file__).resolve().parent.parent / "logs" / "terraform.log"

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

API_TOKEN = BOT_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚀 Run Terraform")],
        [KeyboardButton(text="📊 Analyze app logs")],
        [KeyboardButton(text="🧠 Analyze Terraform logs")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Choose an action 👇", reply_markup=main_keyboard)


# --- Run Terraform ---
@dp.message(F.text == "🚀 Run Terraform")
async def run_terraform_handler(message: types.Message):
    await message.answer("Checking Terraform configuration file with AI... ⏳")

    terraform_configuration = read_terraform_config()
    terraform_configuration_report = json.loads(
        send_request_to_yandex_gpt(terraform_configuration, CONFIG_SYSTEM_MESSAGE).strip("```")
    )

    terraform_configuration_code = terraform_configuration_report["answer"]
    terraform_configuration_comment = terraform_configuration_report["comment"]

    if terraform_configuration_code.lower() in ("yes", "да"):
        await message.answer(terraform_configuration_comment)
        await message.answer("Starting run Terraform... ⏳")

        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, run_terraform)

        await message.answer(f"✅ Result applying of Terraform:\n{result}")
    else:
        await message.answer(terraform_configuration_comment)
        await message.answer("❌ Try to fix .tf configuration file before running.")


# --- Analyze Flask logs ---
@dp.message(F.text == "📊 Analyze app logs")
async def analyze_app_logs(message: types.Message):
    await message.answer("Collecting Flask logs... ⏳")

    logs_text = get_clean_flask_logs(app_log_file)

    if logs_text.startswith(("❌", "⚠️")):
        await message.answer(logs_text)
        return

    await message.answer("Analyzing logs with YandexGPT... 🤖")

    try:
        ai_response = send_request_to_yandex_gpt(logs_text, LOGS_SYSTEM_MESSAGE)
        await message.answer(f"📊 AI analysis of logs:\n\n{ai_response}")
    except Exception as e:
        await message.answer(f"⚠️ Error during analysis: {e}")


# --- Analyze Terraform logs ---
@dp.message(F.text == "🧠 Analyze Terraform logs")
async def analyze_terraform_logs(message: types.Message):
    await message.answer("Collecting Terraform logs... ⏳")

    logs_text = get_clean_terraform_logs(terraform_log_file)

    if logs_text.startswith(("❌", "⚠️")):
        await message.answer(logs_text)
        return

    await message.answer("Analyzing logs with YandexGPT... 🤖")

    try:
        ai_response = send_request_to_yandex_gpt(logs_text, LOGS_SYSTEM_MESSAGE)
        await message.answer(f"📊 AI analysis of logs:\n\n{ai_response}")
    except Exception as e:
        await message.answer(f"⚠️ Error during analysis: {e}")


if __name__ == "__main__":
    async def main():
        try:
            await dp.start_polling(bot)
        finally:
            await bot.session.close()

    asyncio.run(main())
