import os


class Config:
    """
    프로젝트 설정 관리 클래스
    """

    def __init__(self, config_filename="gh_pip.yaml", start_dir=None):
        """
        Config 클래스 초기화

        Args:
            config_filename (str): 설정 파일 이름 (기본값: gh_pip.yaml)
            start_dir (str, optional): 검색 시작 디렉토리. None인 경우 현재 작업 디렉토리 사용
        """
        # 루트 디렉토리 찾기
        self.root_dir = self.find_root(config_filename, start_dir)
        self.config_path = os.path.join(self.root_dir, config_filename)

    def find_root(self, config_filename="gh_pip.yaml", start_dir=None):
        """
        설정 파일이 있는 루트 디렉토리를 찾습니다.

        Args:
            config_filename (str): 설정 파일 이름
            start_dir (str, optional): 검색 시작 디렉토리

        Returns:
            str: 설정 파일이 있는 디렉토리 경로
        """
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
                return current_dir

            # 상위 디렉토리로 이동
            parent_dir = os.path.dirname(current_dir)

            # 루트 디렉토리에 도달했는지 확인 (상위 디렉토리가 현재 디렉토리와 같을 때)
            if parent_dir == current_dir:
                raise FileNotFoundError(f"{config_filename} 파일을 찾을 수 없습니다.")

            # 상위 디렉토리로 이동
            current_dir = parent_dir

    @property
    def config_file_path(self):
        """설정 파일의 절대 경로"""
        return self.config_path

    @property
    def pyproject_path(self):
        """pyproject.toml 파일의 절대 경로"""
        return os.path.join(self.root_dir, "pyproject.toml")

    @property
    def dist_dir(self):
        """dist 디렉토리의 절대 경로"""
        return os.path.join(self.root_dir, "dist")


# 싱글톤 인스턴스 생성 (필요한 경우에만 초기화됨)
_config_instance = None


def get_config(config_filename="gh_pip.yaml", start_dir=None):
    """
    Config 인스턴스를 가져옵니다 (싱글톤 패턴).

    Args:
        config_filename (str): 설정 파일 이름
        start_dir (str, optional): 검색 시작 디렉토리

    Returns:
        Config: Config 인스턴스
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_filename, start_dir)
    return _config_instance
