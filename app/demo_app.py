from flask import Flask
import logging, random, threading, time
import os

os.makedirs("../logs", exist_ok=True)

app = Flask(__name__)

app_logger = logging.getLogger("app_logger")
app_logger.setLevel(logging.INFO)
app_logger.propagate = False

file_handler = logging.FileHandler("../logs/flask.log")
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)
app_logger.addHandler(file_handler)


# ------------------------------------------------------

def generate_logs():
    levels = [logging.INFO, logging.WARNING, logging.ERROR]
    messages = [
        "User logged in",
        "File not found",
        "Database connection failed",
        "Server overload",
        "Unauthorized access"
    ]
    while True:
        level = random.choice(levels)
        message = random.choice(messages)
        app_logger.log(level, message)
        time.sleep(5)


threading.Thread(target=generate_logs, daemon=True).start()


@app.route("/")
def home():
    return "Flask log generator is running!"


@app.route("/simulate")
def simulate():
    level = random.choice([logging.INFO, logging.WARNING, logging.ERROR])
    message = f"Simulated log: {level}"
    app_logger.log(level, message)
    return f"Logged: {message}"


if __name__ == "__main__":
    log = logging.getLogger('werkzeug')
    log.disabled = True

    app.run(host="0.0.0.0", port=5000)
