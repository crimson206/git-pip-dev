# Install Poetry if not already installed
if ! command -v poetry &> /dev/null; then
  echo "[+] Installing Poetry..."
  curl -sSL https://install.python-poetry.org | python3 -

  # 🔥 Manually export Poetry's path
  export PATH="$HOME/.local/bin:$PATH"
  export PATH="$APPDATA/Python/Scripts:$PATH"  # <-- Windows 환경 대응 추가
fi

poetry install
poetry run pytest
