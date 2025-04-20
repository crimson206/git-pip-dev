import os
import shutil
import subprocess

def git_pip_install(
    repo: str= str(),
    github_id: str=str(),
    value: str=str(),
    **_
):
    github_url = get_repository(
        repo=repo,
        github_id=github_id,
        value=value
    )

    pip_url = f"git+{github_url}.git"

    subprocess.run(["bash", "-i", "-c", f"pip install {pip_url}"])


def get_repository(
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
