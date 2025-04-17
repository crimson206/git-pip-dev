import subprocess
import sys

def install_from_git(username, repo_name, version):
    """
    GitHub 저장소에서 특정 버전의 파이썬 패키지를 설치합니다.
    
    Args:
        username (str): GitHub 사용자 이름
        repo_name (str): 저장소 이름
        version (str): 설치할 태그 버전 (예: "0.1.1")
    """
    git_url = f"git+https://github.com/{username}/{repo_name}.git@{version}"
    
    print(f"Installing {repo_name} from {username}'s repository at version {version}...")
    
    try:
        # pip를 사용하여 직접 git 저장소에서 설치
        subprocess.check_call([sys.executable, "-m", "pip", "install", git_url])
        print(f"Successfully installed {repo_name} version {version}")
    
    except subprocess.CalledProcessError as e:
        print(f"Error installing package: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise