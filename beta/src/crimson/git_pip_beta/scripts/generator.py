from jinja2 import Template
import toml
from pathlib import Path

DIRECTORY = Path(__file__).resolve().parent
TEMPLATE_PATH = DIRECTORY / "publish.sh.j2"
template_str = TEMPLATE_PATH.read_text(encoding="utf-8")

def find_pyproject_toml(start: Path = Path.cwd()) -> Path:
    """
    start 디렉토리부터 하위 모든 폴더를 탐색하여 pyproject.toml을 찾는다.
    """
    for path in start.rglob("pyproject.toml"):
        if path.is_file():
            return str(path)
    raise FileNotFoundError("pyproject.toml not found in any subdirectory")

    raise FileNotFoundError("pyproject.toml not found")

def get_version_from_pyproject(pyproject_path: Path) -> str:
    pyproject = toml.load(pyproject_path)
    return pyproject["project"]["version"]

def render_publish_script(index: str, version: str) -> str:
    template = Template(template_str)
    return template.render(index=index, version=version)

toml_path = find_pyproject_toml()

version = get_version_from_pyproject(toml_path)

rendered_script = render_publish_script(index="dev", version=version)

open(f"{DIRECTORY}/publish.sh", "w").write(rendered_script)
