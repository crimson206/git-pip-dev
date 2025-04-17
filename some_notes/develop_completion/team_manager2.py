#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import argparse
import argcomplete
import os
import sys

# 데이터셋 정의
dataset = {
    "teamalpha": {
        "core": ["auth", "db_connector", "api"],
        "utils": ["logger", "validator"]
    },
    "teambeta": {
        "core": ["payment", "notification"],
        "extension": ["analytics", "ads_manager", "notification"],
    },
    "teamgamma": {
        "common": ["security", "cache"],
        "experimental": ["ai_assistant", "data_processor", "cache"]
    }
}

def namespace_completer(prefix, parsed_args, **kwargs):
    """네임스페이스에 대한 자동완성"""
    # 기본 팀 값 또는 사용자가 지정한 팀 값 사용
    team = parsed_args.team if parsed_args.team else "teamalpha"  # 기본값
    
    if team in dataset:
        return [ns for ns in dataset[team].keys() if ns.startswith(prefix)] + ["all"]
    return []

from collections import Counter

def question_duplicated(collections):
    """
    중복된 항목에 '?' 접두사를 붙여 반환합니다.
    
    Args:
        collections: 문자열 리스트
        
    Returns:
        중복 항목에 '?' 접두사가 붙은 고유한 리스트
    """
    # 각 항목의 등장 횟수 계산
    counts = Counter(collections)
    
    # 결과 리스트 생성
    result = []
    seen = set()
    
    for item in collections:
        # 이미 처리한 항목은 건너뜀
        if item in seen:
            continue
        
        # 항목이 중복된 경우 '?' 접두사 추가
        if counts[item] > 1:
            result.append(f"?{item}")
        else:
            result.append(item)
            
        # 처리한 항목으로 표시
        seen.add(item)
    
    return result

def module_completer(prefix, parsed_args, **kwargs):
    """모듈 이름에 대한 자동완성"""
    # 기본 팀 값 또는 사용자가 지정한 팀 값 사용
    team = parsed_args.team if parsed_args.team else "teamalpha"  # 기본값
    
    if parsed_args.namespace == "all":
        # 모든 모듈을 반환
        collections = [mod for ns in dataset[team].values() for mod in ns if mod.startswith(prefix)]
        return question_duplicated(collections)
    elif parsed_args.namespace and team in dataset and parsed_args.namespace in dataset[team]:
        return [mod for mod in dataset[team][parsed_args.namespace] if mod.startswith(prefix)]
    return []

def team_completer(prefix, parsed_args, **kwargs):
    """팀 이름에 대한 자동완성"""
    return [team for team in dataset.keys() if team.startswith(prefix)]

class CustomCompletionFinder(argcomplete.CompletionFinder):
    def _get_completions(self, comp_words, cword_prefix, cword_prequote, last_wordbreak_pos):


        # 기존 처리에서 받아온 자동완성 결과
        completions = super()._get_completions(comp_words, cword_prefix, cword_prequote, last_wordbreak_pos)
        
        # 현재 명령줄 상태 확인
        has_team = any(w in ['-ts', '--team'] or w.startswith('-ts=') or w.startswith('--team=') for w in comp_words)
        has_namespace = any(w in ['-ns', '--namespace'] or w.startswith('-ns=') or w.startswith('--namespace=') for w in comp_words)
        
        # 현재 단어가 옵션인지 확인     
        current_word_is_option = cword_prefix.startswith('-')
        

        filter = []
        # 컨텍스트에 따른 필터링
        filtered_completions = []

        if current_word_is_option:
            if has_team and not has_namespace:
                filter += ['-ts', '--team']
            elif has_namespace and not has_team:
                filter += ['-ns', '--namespace']
            

            filtered_completions = [c for c in completions if not c in filter]

        elif has_team and has_namespace:
            # 옵션이 아닌 경우 필터링
            filtered_completions = [c for c in completions if not c.startswith("-")]
        else:
            # 옵션이 아닌 경우 필터링
            filtered_completions = completions

        return filtered_completions

def main():
    parser = argparse.ArgumentParser(description='Package manager with hierarchical tab completion')
    
    # 옵션 추가 (팀에 기본값 설정)
    team_arg = parser.add_argument('-ts', '--team', help='Team name', default="teamalpha")
    namespace_arg = parser.add_argument('-ns', '--namespace', help='Namespace')
    module_arg = parser.add_argument('module', help='Module name')
    
    # 자동완성 설정
    team_arg.completer = team_completer
    namespace_arg.completer = namespace_completer
    module_arg.completer = module_completer
    
    # 커스텀 자동완성 파인더 생성 및 활성화
    completion_finder = CustomCompletionFinder()
    completion_finder(parser)
    
    # 인자 파싱
    args = parser.parse_args()
    
    # 명령 실행
    print(f"Team: {args.team}")
    print(f"Namespace: {args.namespace}")
    print(f"Module: {args.module}")

if __name__ == "__main__":
    main()