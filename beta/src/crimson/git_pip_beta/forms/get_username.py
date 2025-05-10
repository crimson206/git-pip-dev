import subprocess
import json
from pathlib import Path

DIRECTORY = Path(__file__).resolve().parent


def get_github_username():
    result = subprocess.run(
        [f"{DIRECTORY}/get_username.sh"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {result.stderr.strip()}")

    data = json.loads(result.stdout)
    return data.get("login")


if __name__ == "__main__":
    username = get_github_username()
    print(f"GitHub username: {username}")
