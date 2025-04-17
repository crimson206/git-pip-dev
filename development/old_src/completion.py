def print_completion_script():
    """Bash 자동완성 스크립트 출력"""
    print("""
# git-pip 자동완성 스크립트
_git_pip_completions()
{
    local cur prev
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # 기본 명령어들
    commands="install uninstall list search completion"
    
    # 첫번째 인자일 경우 명령어 자동완성
    if [[ ${COMP_CWORD} -eq 1 ]] ; then
        COMPREPLY=( $(compgen -W "${commands}" -- ${cur}) )
        return 0
    fi
    
    # 특정 명령어 다음의 인자 자동완성
    case "${prev}" in
        install)
            # 자주 사용하는 레포지토리 제안
            COMPREPLY=( $(compgen -W "crimson206/git-pip user/other-repo" -- ${cur}) )
            ;;
        # 다른 명령어에 대한 자동완성도 추가 가능
    esac
}

complete -F _git_pip_completions git-pip
""")