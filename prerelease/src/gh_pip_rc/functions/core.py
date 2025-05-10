import os
from github import Github
from gh_pip_rc.functions.utils import ( 
    load_github_token, 
    get_repository_info, 
    read_version_from_pyproject, 
    get_distribution_files
)
from gh_pip_rc.config.core import get_config


def publish(config_filename="gh_pip.yaml", start_dir=None):
    """
    GitHub 릴리스를 생성하고 배포 파일을 업로드합니다.

    Args:
        config_filename (str): 설정 파일 이름
        start_dir (str, optional): 검색 시작 디렉토리

    Returns:
        str: 생성된 릴리스의 URL
    """
    # Config 인스턴스 가져오기
    config = get_config(config_filename, start_dir)

    # GitHub 토큰 로드
    github_token = load_github_token(config.config_file_path)

    # 저장소 정보 가져오기
    repo_info = get_repository_info(config.root_dir)
    repository_name = repo_info["name"]

    # 버전 정보 가져오기
    version = read_version_from_pyproject(config.pyproject_path)

    # 태그 이름 생성
    tag_name = f"gh-pip-v{version}"

    # GitHub 연결 초기화
    g = Github(github_token)
    repo = g.get_repo(repository_name)

    # 태그가 이미 존재하는지 확인
    try:
        repo.get_git_ref(f"tags/{tag_name}")
        print(f"태그 {tag_name}이(가) 이미 존재합니다. 태그 생성을 건너뜁니다.")
        create_tag = False
    except:
        create_tag = True

    # 태그가 존재하지 않는 경우 생성하고 푸시
    if create_tag:
        # 마지막 커밋 가져오기
        commit = repo.get_commits()[0]

        # 태그 참조 생성
        ref = f"refs/tags/{tag_name}"
        repo.create_git_ref(ref=ref, sha=commit.sha)
        print(f"태그 {tag_name}을(를) 생성했습니다.")

    # 릴리스가 이미 존재하는지 확인
    try:
        release = repo.get_release(tag_name)
        print(f"{tag_name}에 대한 릴리스가 이미 존재합니다.")
    except:
        # 릴리스 생성
        release = repo.create_git_release(
            tag=tag_name,
            name=f"Release v{version}",
            message=f"Automated release for version {version}",
            draft=False,
            prerelease=False,
        )
        print(f"{tag_name}에 대한 릴리스를 생성했습니다.")

    # dist 디렉토리의 파일들을 릴리스 자산으로 업로드
    dist_files = get_distribution_files(config.dist_dir)
    for file_path in dist_files:
        file_name = os.path.basename(file_path)

        # 자산이 이미 존재하는지 확인
        skip_upload = False
        for asset in release.get_assets():
            if asset.name == file_name:
                print(f"자산 {file_name}이(가) 이미 존재합니다. 업로드를 건너뜁니다.")
                skip_upload = True
                break

        if not skip_upload:
            with open(file_path, "rb") as file:
                release.upload_asset(
                    path=file_path,
                    content_type="application/octet-stream",
                    name=file_name,
                )
            print(f"{file_name}을(를) 릴리스 {tag_name}에 업로드했습니다.")

    print(f"배포 완료: {release.html_url}")
    return release.html_url
