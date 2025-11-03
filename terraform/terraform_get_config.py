from pathlib import Path

def read_terraform_config() -> str:
    terraform_file = Path(__file__).resolve().parent.parent / "terraform" / "main.tf"

    if not terraform_file.exists():
        raise FileNotFoundError(f"Configuration .tf file is not found: {terraform_file}")

    with open(terraform_file, "r", encoding="utf-8") as f:
        content = f.read()

    return content

