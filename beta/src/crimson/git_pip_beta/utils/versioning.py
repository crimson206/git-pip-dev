from typing import List
from crimson.git_pip_beta.utils.processor import run_shell

from packaging.version import Version, InvalidVersion
from packaging.specifiers import SpecifierSet
from typing import List, Optional
import json

TAG_PREFIX = "git-pip-v"


def get_git_pip_tags(user: str, repo: str) -> List[str]:
    cmd = f"gh api repos/{user}/{repo}/tags"
    result = run_shell(cmd, capture_output=True, text=True, check=True)

    tags = json.loads(result.stdout)
    return [tag["name"] for tag in tags if tag["name"].startswith("git-pip-v")]

def extract_version(tag: str) -> Optional[Version]:
    if tag.startswith(TAG_PREFIX):
        try:
            return Version(tag[len(TAG_PREFIX):])
        except InvalidVersion:
            return None
    return None


def filter_versions_by_spec(
    tags: List[str],
    spec: str
) -> List[str]:
    specifier = SpecifierSet(spec)
    valid = []

    for tag in tags:
        version = extract_version(tag)
        if version and version in specifier:
            valid.append((version, tag))

    return [tag for _, tag in sorted(valid, key=lambda x: x[0], reverse=True)]


def resolve_best_tag(tags: List[str], spec: str) -> Optional[str]:
    matches = filter_versions_by_spec(tags, spec)
    return matches[0] if matches else None
