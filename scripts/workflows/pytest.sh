#!/usr/bin/env bash
set -e  # 실패 시 즉시 종료
cd beta

# Poetry 설치 (전역 설치가 안된 경우를 위해)
if ! command -v poetry &> /dev/null; then
  echo "[+] Installing Poetry..."
  curl -sSL https://install.python-poetry.org | python3 -
  export PATH="$HOME/.local/bin:$PATH"
fi

poetry install
poetry run pytest
