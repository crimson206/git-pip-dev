import subprocess
import json
import re
from typing import List, Dict, Set
from pathlib import Path

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


def generate_index_html_for_index(index: str, repo: str, output_dir: str) -> None:
    """
    Generate an index.html file for a given index (e.g., dev, test) and save it under output_dir/index/index.html.
    """
    tag_asset_map = get_tag_asset_map(index)
    output_path = Path(output_dir) / index / "index.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    html_lines = [
        "<!DOCTYPE html>",
        "<html>",
        f"<head><title>{index} package index</title></head>",
        "<body>",
        f"<h1>{index} packages</h1>",
        "<ul>"
    ]

    for tag, assets in tag_asset_map.items():
        version = tag.removeprefix(f"gh-pip-{index}-v")
        for asset in assets:
            url = f"https://github.com/{repo}/releases/download/{tag}/{asset}"
            html_lines.append(f'  <li><a href="{url}">{version} - {asset}</a></li>')

    html_lines += ["</ul>", "</body>", "</html>"]

    output_path.write_text("\n".join(html_lines), encoding="utf-8")


generate_index_html_for_index("dev", "crimson206/git-pip-dev", Path("simple"))