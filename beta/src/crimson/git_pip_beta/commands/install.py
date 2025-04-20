from cleo.helpers import argument, option
from cleo.commands.command import Command  # Your customized Command class
from ..processor import run_shell

def git_pip_install(
    repo: str= str(),
    github_id: str=str(),
    value: str=str(),
    **_
):
    github_url = get_repository_url(
        repo=repo,
        github_id=github_id,
        value=value
    )

    pip_url = f"git+{github_url}.git"

    run_shell(f"pip install {pip_url}")


def get_repository_url(
    repo:str,
    github_id:str,
    value:str
):

    def check_repository_full_name(value:str) -> bool:
        if "/" in value:
            return True
        else:
            return False

    if check_repository_full_name(value):
        return f"https://github.com/{value}"
    else:
        module_name = value

    github_url = "https://github.com/{id}/{repo}"

    if repo and value:
        raise ValueError(
            f"Both repo and module_name are provided. Please provide only one."
        )
    elif github_id:
        if module_name:
            repo_from_db = "get from db."
            github_url = github_url.format(id=github_id, repo=repo_from_db)
        elif repo:
            github_url = github_url.format(id=github_id, repo=repo)
        else:
            raise ValueError(
                f"Neither repo nor module_name is provided. Please provide one."
            )
    else:
        raise ValueError(
            f"Github_id is required."
        )

    return github_url


class InstallCommand(Command):
    name = "install"
    description = "Install a package from GitHub."
    help = """\
Install a package from GitHub.

    Case1: git-pip install -gi <github-id> <module-name>
    Case2: git-pip install <github-id>/<repo>

If the default GitHub ID is set,

    Case3: git-pip install <module-name>
"""

    arguments = [
        argument("value", description="github_id/repo or your module name.")
    ]

    options = [
        option("repo", "r", flag=False, description="The name of the repository."),
        option("github-id", "gi", flag=False, description="The ID of the GitHub user.")
    ]

    def handle(self) -> int:
        git_pip_install(
            command="install",
            value=self.argument("value"),
            repo=self.option("repo") or "",
            github_id=self.option("github-id") or ""
        )
        return 0
