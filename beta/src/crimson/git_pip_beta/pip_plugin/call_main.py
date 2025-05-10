#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path


RESET = "\033[0m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RED = "\033[31m"


def color(msg, code):
    return f"{code}{msg}{RESET}"


def wrap_pip():
    local_bin = Path.home() / ".local" / "bin"
    local_bin.mkdir(parents=True, exist_ok=True)

    pip_shim = local_bin / "pip"
    if pip_shim.exists():
        print(color("[gh-pip] 이미 shim이 존재합니다.", YELLOW))
        return 1

    shim_script = """#!/usr/bin/env bash
export GH_PIP_SHIM_ACTIVE=1
gh-pip "$@"
"""

    pip_shim.write_text(shim_script)
    pip_shim.chmod(0o755)

    print(color(f"[gh-pip] pip shim 설치됨 → {pip_shim}", GREEN))

    print(color("[gh-pip] 'hash -r'를 실행하거나 새 셸을 여세요", YELLOW))

    return 0


def unwrap_pip():
    pip_shim = Path.home() / ".local" / "bin" / "pip"

    if not pip_shim.exists():
        print(color("[gh-pip] shim이 존재하지 않습니다.", YELLOW))
        return 1

    pip_shim.unlink()
    print(color("[gh-pip] pip shim 제거 완료", GREEN))

    print(color("[gh-pip] 'hash -r'를 실행하거나 새 셸을 여세요", YELLOW))

    return 0


def run_pip(cleaned_args, gh_pip_message=None):
    if gh_pip_message:
        print(color(f"[gh-pip] 메시지 받음: {gh_pip_message}", GREEN))
        print(color(f"[gh-pip] 실행할 pip 명령: pip {' '.join(cleaned_args)}", YELLOW))

    print(cleaned_args)

    if os.environ.get("GH_PIP_SHIM_ACTIVE"):
        # 내부 pip 호출 시 shim을 피함
        return subprocess.call([sys.executable, "-m", "pip"] + cleaned_args)
    else:
        pip_real = "pip"

    # pip_real = shutil.which("pip.real") or shutil.which("pip")
    if not pip_real:
        print(color("pip 실행 파일을 찾을 수 없습니다.", RED), file=sys.stderr)
        return 1

    return subprocess.call([sys.executable, "-m", "pip"] + cleaned_args)


def main():
    args = sys.argv[1:]

    if args[:1] == ["wrap"]:
        return wrap_pip()
    elif args[:1] == ["unwrap"]:
        return unwrap_pip()

    # parse --gh-pip
    gh_pip_message = None
    cleaned_args = []
    i = 0
    while i < len(args):
        if args[i] == "--gh-pip" and i + 1 < len(args):
            gh_pip_message = args[i + 1]
            i += 2
        elif args[i].startswith("--gh-pip="):
            gh_pip_message = args[i].split("=", 1)[1]
            i += 1
        else:
            cleaned_args.append(args[i])
            i += 1

    return run_pip(cleaned_args, gh_pip_message)


if __name__ == "__main__":
    sys.exit(main())
