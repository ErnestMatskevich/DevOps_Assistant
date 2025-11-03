# Telegram Terraform & Flask Bot

This project is a Telegram bot that allows you to:

- Deploy a Flask application using Terraform.
- Analyze Flask application logs and Terraform logs using YandexGPT AI.
- Interact with Terraform deployments directly from Telegram.

---

## Features

1. **Run Terraform**  
   Deploys your Flask app containerized with Docker using Terraform.

2. **Analyze Logs**  
   - Analyze Flask app logs (`flask.log`) using AI.  
   - Analyze Terraform logs (`terraform.log`) using AI.  

3. **Easy-to-use Reply Keyboard**  
   Commands are accessible via always-visible buttons in the chat.

---

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your credentials:

```
BOT_TOKEN=your_telegram_bot_token
KEY=your_yandex_api_key
ID_KEY=your_yandex_folder_id
```

4. Make sure Docker is running and Terraform is installed.

---

## Usage

Start the bot:

```bash
python bot/main.py
```

### Bot commands:

- **Run Terraform**: Deploys the Flask app.
- **Analyze app logs**: Sends Flask logs to YandexGPT for analysis.
- **Analyze Terraform logs**: Sends Terraform logs to YandexGPT for analysis.

---

## Notes

- All logs are stored in the `logs/` folder.
- The bot uses YandexGPT API to analyze logs, so an API key and folder ID are required.
- `.terraform.lock.hcl`, `.tfstate` files, logs, and secrets are ignored via `.gitignore`.
