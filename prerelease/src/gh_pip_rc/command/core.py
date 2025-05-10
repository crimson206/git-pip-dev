
import argparse
from gh_pip_rc.functions.core import publish


def main():
    parser = argparse.ArgumentParser(
        description="Publish a Python package to GitHub releases"
    )
    parser.add_argument(
        "--token",
        "-t",
        help="GitHub personal access token (if not provided, uses GITHUB_TOKEN env variable)",
    )
    parser.add_argument(
        "--repo", "-r", required=True, help="Repository name in format username/repo"
    )

    args = parser.parse_args()

    try:
        url = publish(github_token=args.token, repository_name=args.repo)
        print(f"Success! Release available at: {url}")
    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
