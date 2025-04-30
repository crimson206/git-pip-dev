import subprocess
import json
import re
from typing import List, Dict, Set


def get_all_indices(tags: list[str]) -> Set[str]:
    """
    Extract all unique index values from tags following the pattern gh-pip-{index}-v{version}.
    """
    pattern = re.compile(r"^gh-pip-(?P<index>[^-]+)-v[\w.\-]+$")
    indices = {m.group("index") for tag in tags if (m := pattern.match(tag))}
    return indices


def run_gh_command(command: List[str]) -> str:
    """Run a gh CLI command and return its output."""
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def get_all_release_tags(repo: str = "crimson206/git-pip-dev") -> List[str]:
    """Get all release tags using the GitHub API."""
    output = run_gh_command([
        "gh", "api", f"repos/{repo}/releases",
        "--paginate"
    ])
    data = json.loads(output)
    return [entry["tag_name"] for entry in data if "tag_name" in entry]

def filter_tags(tags: List[str], index: str) -> List[str]:
    """Filter tags that match the gh-pip-{index}-v{version} pattern."""
    pattern = re.compile(rf"^gh-pip-{re.escape(index)}-v[\w\.\-]+$")
    return [tag for tag in tags if pattern.match(tag)]


def get_assets_for_tag(tag: str) -> List[str]:
    """Get asset file names for a given release tag."""
    output = run_gh_command([
        "gh", "release", "view", tag,
        "--json", "assets",
        "--jq", ".assets[].name"
    ])
    return output.splitlines()


def get_tag_asset_map(index: str) -> Dict[str, List[str]]:
    """Return a mapping of filtered tags to their asset file names."""
    tags = get_all_release_tags()
    filtered = filter_tags(tags, index)
    return {tag: get_assets_for_tag(tag) for tag in filtered}

tags = get_all_release_tags()

print(get_all_indices(tags))

print(get_tag_asset_map("dev"))
