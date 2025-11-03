import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TERRAFORM_DIR = BASE_DIR / "terraform"
LOG_FILE = BASE_DIR / "logs" / "terraform.log"

def run_terraform():
    env = {
        **subprocess.os.environ,
        "TF_LOG": "DEBUG",
        "TF_LOG_PATH": str(LOG_FILE)
    }

    commands = [
        ["terraform", "init"],
        ["terraform", "plan"],
        ["terraform", "apply", "-auto-approve"]
    ]

    for cmd in commands:
        result = subprocess.run(cmd, env=env, cwd=TERRAFORM_DIR, capture_output=True, text=True)
        if result.returncode != 0:
            return f"Command {' '.join(cmd)} failed:\n{result.stderr}"
    return "Terraform applied successfully!"
