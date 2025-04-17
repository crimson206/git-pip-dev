import sys
import argparse
import re
from crimson.git_pip.git_operations import install_from_git
from crimson.git_pip.completion import print_completion_script

def main():
    parser = argparse.ArgumentParser(description='Install Python packages from git repositories')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # install 명령어
    install_parser = subparsers.add_parser('install', help='Install a package from a git repository')
    install_parser.add_argument('repo_with_version', help='Repository in format username/repo==version')
    
    # completion 명령어
    completion_parser = subparsers.add_parser('completion', help='Output shell completion script')
    
    # 다른 명령어들도 추가 가능
    
    args = parser.parse_args()
    
    if args.command == 'install':
        repo_pattern = r'^([^/]+)/([^=]+)==(.+)$'
        match = re.match(repo_pattern, args.repo_with_version)
        
        if not match:
            print("Error: Repository format should be 'username/repo==version'")
            sys.exit(1)
            
        username, repo, version = match.groups()
        print(f"Installing {repo} from {username}'s repository at version {version}...")
        install_from_git(username, repo, version)
    
    elif args.command == 'completion':
        
        print_completion_script()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()