import argparse
from rich_argparse import RawTextRichHelpFormatter
from .install import git_pip_install

def main():
    parser = argparse.ArgumentParser(description="git-pip CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_parser = subparsers.add_parser(
        "install", 
        help="Install a package from GitHub.",
        description="""\
Install a package from GitHub.

    Case1: git-pip install -gi <github-id> <module-name>
    Case2: git-pip install <github-id>/<repo>

If the default GitHub ID is set,

    Case3: git-pip install <module-name>

""",
    formatter_class=RawTextRichHelpFormatter
)               

    install_parser.add_argument("--repo", "-r", default="", type=str, help="The name of the repository.")
    install_parser.add_argument("--github-id", "-gi", default="", type=str, help="The ID of the GitHub user.")
    install_parser.add_argument("value", default="", type=str, help="github_id/repo or your module name.")

    install_parser.set_defaults()

    args = parser.parse_args()

    git_pip_install(**vars(args))

if __name__ == "__main__":
    main()
