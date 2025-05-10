#!/usr/bin/env python3

"""
범용 VSCode launch.json 생성 함수

어떤 명령어든 디버깅할 수 있는 간단한 launch.json 문자열 생성기
"""

import json
import os
import sys
import shlex


def create_debug_json(command, name=None, cwd=None, env_vars=None):
    """
    명령어 디버깅을 위한 VSCode launch.json 문자열 생성

    Args:
        command (str): 전체 명령어 문자열 (예: "pip install --gh-pip hi package-name")
        name (str, optional): 디버그 설정 이름
        cwd (str, optional): 작업 디렉토리 (기본값: 현재 디렉토리)
        env_vars (dict, optional): 환경 변수 딕셔너리

    Returns:
        str: 생성된 launch.json 문자열
    """
    # 명령어를 단어로 분할
    args = shlex.split(command)
    if not args:
        raise ValueError("명령어를 입력해야 합니다.")

    # 명령어 이름 추출
    cmd_name = args[0]
    cmd_args = args[1:] if len(args) > 1 else []

    # 디버그 설정 이름 설정
    if not name:
        name = f"Debug {command}"

    # 작업 디렉토리 설정
    if not cwd:
        cwd = os.getcwd()

    # 환경 변수 설정
    env = env_vars or {}

    if cmd_name in ["python", "python3", sys.executable]:
        program = args[0]
        program_args = args[1:]
    else:
        # 일반 명령어는 시스템 python을 통해 -m 옵션으로 실행
        program = sys.executable
        program_args = [cmd_name] + cmd_args

    # 디버그 설정 생성
    debug_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": name,
                "type": "python",
                "request": "launch",
                "program": program,
                "args": program_args,
                "cwd": cwd,
                "justMyCode": True,
                "console": "integratedTerminal",
            }
        ],
    }

    # 환경 변수가 있는 경우 추가
    if env:
        debug_config["configurations"][0]["env"] = env

    # JSON 문자열로 변환하여 반환
    return json.dumps(debug_config, indent=4)


def save_launch_json(json_str, output_path=None):
    """
    launch.json 파일 저장

    Args:
        json_str (str): launch.json 문자열
        output_path (str, optional): 저장 경로 (기본값: .vscode/launch.json)

    Returns:
        str: 저장된 파일 경로
    """
    if not output_path:
        output_path = os.path.join(os.getcwd(), ".vscode", "launch.json")

    # 디렉토리가 없으면 생성
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 파일 저장
    with open(output_path, "w") as f:
        f.write(json_str)

    return output_path


# 간단한 사용 예제
if __name__ == "__main__":
    # 예제: pip install --gh-pip hi crimson-file-loader
    cmd = "pip install --gh-pip hi crimson-file-loader"

    # launch.json 문자열 생성
    launch_json = create_debug_json(command=cmd, name="Debug pip with gh-pip")

    # 출력
    print(launch_json)

    # 저장 (선택 사항)
    # save_launch_json(launch_json)
