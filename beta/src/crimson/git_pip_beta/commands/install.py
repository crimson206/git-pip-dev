import re
from cleo.helpers import argument, option
from cleo.commands.command import Command  # Your customized Command class
from crimson.git_pip_beta.utils.versioning import get_git_pip_tags, resolve_best_tag
from crimson.git_pip_beta.utils.processor import run_shell

def parse_repo_spec(value: str) -> tuple[str, str, str]:
    # e.g. crimson206/git-pip>=0.1.0,<0.2.0
    match = re.match(r"(?P<id>[^/]+)/(?P<repo>[^\s<>=!~]+)(?P<spec>.*)", value)
    if not match:
        raise ValueError("Invalid format. Expected id/repo[<spec>]")
    return match.group("id"), match.group("repo"), match.group("spec") or ""

def git_pip_install(repo: str, github_id: str, value: str):
    github_url = get_repository_url(
        repo=repo,
        github_id=github_id,
        value=value
    )
    pip_url = f"git+{github_url}"
    run_shell(f"pip install {pip_url}")


def get_repository_url(
    repo: str,
    github_id: str,
    value: str
) -> str:
    def is_full_repo_path(val: str) -> bool:
        return "/" in val

    # 1. 우선순위: value > repo
    if is_full_repo_path(value):
        full_repo = value
        version_spec = ""
    else:
        full_repo = f"{github_id}/{repo or value}"
        version_spec = ""

    # 2. 버전 포함 여부 확인 (e.g. repo==1.2.3 or value==1.2.3)
    m = re.match(r"(?P<full>[^<>=!~]+)(?P<spec>[<>=!~].+)?", full_repo)
    if not m:
        raise ValueError("Invalid format for repo and version")

    full_repo = m.group("full").strip("/")
    version_spec = m.group("spec") or ""

    github_id, repo_name = full_repo.split("/")

    tags = get_git_pip_tags(github_id, repo_name)
    tag = resolve_best_tag(tags, version_spec) if version_spec else "main"

    return f"https://github.com/{github_id}/{repo_name}.git@{tag}"


class InstallCommand(Command):
    name = "install"
    description = "Install a package from GitHub."
    help = """\
Install a package from GitHub.

    Case1: git-pip install -i <github-id> <module-name>
    Case2: git-pip install <github-id>/<repo>

If the default GitHub ID is set,

    Case3: git-pip install <module-name>
"""

    arguments = [
        argument("value", description="github_id/repo or your module name.")
    ]

    options = [
        option("repo", "r", flag=False, description="The name of the repository."),
        option("github-id", "i", flag=False, description="The ID of the GitHub user.")
    ]

    def handle(self) -> int:
        git_pip_install(
            value=self.argument("value"),
            repo=self.option("repo") or "",
            github_id=self.option("github-id") or ""
        )
        return 0
