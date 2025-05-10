import os


def find_root(config_filename="gh_pip.yaml", start_dir=None):
    # 검색 시작 디렉토리 설정
    if start_dir is None:
        start_dir = os.getcwd()

    # 절대 경로로 변환
    current_dir = os.path.abspath(start_dir)

    # 파일 시스템의 루트 디렉토리에 도달할 때까지 올라가면서 검색
    while True:
        # 현재 디렉토리에서 config_filename 확인
        config_path = os.path.join(current_dir, config_filename)
        if os.path.isfile(config_path):
            print(f"설정 파일을 찾았습니다: {config_path}")
            return os.path.dirname(config_path)

        # 상위 디렉토리로 이동
        parent_dir = os.path.dirname(current_dir)

        # 루트 디렉토리에 도달했는지 확인 (상위 디렉토리가 현재 디렉토리와 같을 때)
        if parent_dir == current_dir:
            raise FileNotFoundError(f"{config_filename} 파일을 찾을 수 없습니다.")

        # 상위 디렉토리로 이동
        current_dir = parent_dir
