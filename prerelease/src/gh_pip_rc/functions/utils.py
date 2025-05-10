from gh_pip_rc.config.core import get_config
import yaml
import subprocess
import toml
import glob


def load_github_token(yaml_path=None):
    """
    gh_pip.yaml 파일에서 GitHub 토큰을 로드합니다.

    Args:
        yaml_path (str, optional): 토큰이 포함된 YAML 파일 경로. None인 경우 Config에서 경로 가져옴

    Returns:
        str: GitHub 토큰
    """
    if yaml_path is None:
        config = get_config()
        yaml_path = config.config_file_path

    try:
        with open(yaml_path, "r") as file:
            config_data = yaml.safe_load(file)

        if "GITHUB_TOKEN" not in config_data:
            raise ValueError(f"GITHUB_TOKEN 필드가 {yaml_path} 파일에 없습니다.")

        return config_data["GITHUB_TOKEN"]
    except FileNotFoundError:
        raise FileNotFoundError(f"{yaml_path} 파일을 찾을 수 없습니다.")
    except yaml.YAMLError as e:
        raise ValueError(f"YAML 파일 파싱 오류: {e}")


def get_repository_info(root_dir=None):
    """
    git 저장소의 정보를 가져옵니다.

    Args:
        root_dir (str, optional): 저장소 루트 디렉토리. None인 경우 Config에서 경로 가져옴

    Returns:
        dict: 저장소 정보를 포함하는 딕셔너리
            - name: 저장소 이름 (사용자명/저장소)
            - url: 저장소 URL
            - user: 사용자명
            - repo: 저장소명
    """
    if root_dir is None:
        config = get_config()
        root_dir = config.root_dir

    try:
        # 원격 저장소 URL 가져오기
        remote_url = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"],
            universal_newlines=True,
            cwd=root_dir,
        ).strip()

        # URL에서 사용자명/저장소 형식 파싱
        user = None
        repo = None

        if remote_url.startswith("https://"):
            # https://github.com/username/repo.git
            parts = remote_url.split("/")
            user = parts[-2]
            repo = parts[-1]
            if repo.endswith(".git"):
                repo = repo[:-4]
        elif remote_url.startswith("git@"):
            # git@github.com:username/repo.git
            parts = remote_url.split(":")
            user_repo = parts[1]
            if user_repo.endswith(".git"):
                user_repo = user_repo[:-4]
            user, repo = user_repo.split("/")
        else:
            raise ValueError(f"알 수 없는 원격 저장소 URL 형식: {remote_url}")

        return {"name": f"{user}/{repo}", "url": remote_url, "user": user, "repo": repo}
    except subprocess.CalledProcessError:
        raise ValueError("Git 저장소가 아니거나 원격 저장소가 설정되지 않았습니다.")


def read_version_from_pyproject(pyproject_path=None):
    """
    pyproject.toml 파일에서 버전 정보를 읽어옵니다.

    Args:
        pyproject_path (str, optional): pyproject.toml 파일 경로. None인 경우 Config에서 경로 가져옴

    Returns:
        str: 패키지 버전
    """
    if pyproject_path is None:
        config = get_config()
        pyproject_path = config.pyproject_path

    try:
        pyproject_data = toml.load(pyproject_path)

        # 버전 정보 찾기 (project.version 또는 tool.poetry.version)
        if "project" in pyproject_data and "version" in pyproject_data["project"]:
            return pyproject_data["project"]["version"]
        elif (
            "tool" in pyproject_data
            and "poetry" in pyproject_data["tool"]
            and "version" in pyproject_data["tool"]["poetry"]
        ):
            return pyproject_data["tool"]["poetry"]["version"]
        else:
            raise KeyError(f"{pyproject_path}에서 버전 정보를 찾을 수 없습니다.")
    except FileNotFoundError:
        raise FileNotFoundError(f"{pyproject_path} 파일을 찾을 수 없습니다.")
    except Exception as e:
        raise ValueError(f"{pyproject_path} 파일 파싱 오류: {e}")


def get_distribution_files(dist_dir=None):
    """
    dist 디렉토리의 배포 파일들을 찾습니다.

    Args:
        dist_dir (str, optional): dist 디렉토리 경로. None인 경우 Config에서 경로 가져옴

    Returns:
        list: 배포 파일 경로 목록
    """
    if dist_dir is None:
        config = get_config()
        dist_dir = config.dist_dir

    dist_files = glob.glob(f"{dist_dir}/*")
    if not dist_files:
        raise ValueError(
            f"{dist_dir} 디렉토리에 배포 파일이 없습니다. 빌드를 먼저 실행하세요."
        )
    return dist_files
