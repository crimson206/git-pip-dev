from cleo import Application, Command
from cleo.helpers import argument, option
from typing import Any, Dict

# Import your installation function
# from .install import git_pip_install

# Fix for the add function (not directly related to the Cleo conversion)
def add(a: int, b: int) -> int:
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError(f"Both arguments must be integers, received {type(a).__name__} and {type(b).__name__}")
    return a + b

class InstallCommand(Command):
    name = "install"
    description = "Install a package from GitHub."
    help = """Install a package from GitHub.

Case1: git-pip install -gi <github-id> <module-name>
Case2: git-pip install <github-id>/<repo>

If the default GitHub ID is set,

Case3: git-pip install <module-name>
"""

    arguments = [
        argument(
            "value",
            description="GitHub ID/repo or your module name.",
        )
    ]

    options = [
        option(
            "repo", "r",
            description="The name of the repository.",
            default="",
        ),
        option(
            "github-id", "gi",
            description="The ID of the GitHub user.",
            default="",
        )
    ]

    def handle(self) -> int:
        # Convert command arguments to a dictionary similar to argparse's vars(args)
        args_dict = {
            "command": "install",
            "value": self.argument("value"),
            "repo": self.option("repo"),
            "github_id": self.option("github-id"),
        }
        
        # Call the original installation function
        # git_pip_install(**args_dict)
        
        # For demonstration, just print the arguments
        self.line(f"<info>Installing with arguments:</info> {args_dict}")
        
        return 0

def main():
    application = Application("git-pip", "1.0.0")
    application.add(InstallCommand())
    application.run()

if __name__ == "__main__":
    main()