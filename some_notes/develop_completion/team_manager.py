#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import argparse
import argcomplete

# 데이터셋 정의
dataset = {
    "teamalpha": {
        "core": ["auth", "db_connector", "api"],
        "utils": ["logger", "validator"]
    },
    "teambeta": {
        "core": ["payment", "notification"],
        "extension": ["analytics", "ads_manager"]
    },
    "teamgamma": {
        "common": ["security", "cache"],
        "experimental": ["ai_assistant", "data_processor"]
    }
}

def team_completer(prefix, parsed_args, **kwargs):
    """팀 이름에 대한 자동완성"""

    open("team.log", "a").write(f"Team: {parsed_args.team}\n")

    return [team for team in dataset.keys() if team.startswith(prefix)]

def namespace_completer(prefix, parsed_args, **kwargs):
    """네임스페이스에 대한 자동완성"""
    if parsed_args.team and parsed_args.team in dataset:
        return [ns for ns in dataset[parsed_args.team].keys() if ns.startswith(prefix)]
    return []

def module_completer(prefix, parsed_args, **kwargs):
    """모듈 이름에 대한 자동완성"""

    if (parsed_args.team and parsed_args.namespace and 
        parsed_args.team in dataset and 
        parsed_args.namespace in dataset[parsed_args.team]):
        return [mod for mod in dataset[parsed_args.team][parsed_args.namespace] if mod.startswith(prefix)]
    return []

def main():
    parser = argparse.ArgumentParser(description='Package manager with hierarchical tab completion')
    
    # 옵션 추가
    team_arg = parser.add_argument('-ts', '--team', help='Team name')
    namespace_arg = parser.add_argument('-ns', '--namespace', help='Namespace')
    module_arg = parser.add_argument('module', help='Module name')
    
    # 자동완성 설정
    team_arg.completer = team_completer
    namespace_arg.completer = namespace_completer
    module_arg.completer = module_completer

        # argcomplete 활성화
    argcomplete.autocomplete(parser)

    # 인자 파싱
    args = parser.parse_args()
    
    # 명령 실행
    print(f"Team: {args.team}")
    print(f"Namespace: {args.namespace}")
    print(f"Module: {args.module}")

if __name__ == "__main__":
    main()