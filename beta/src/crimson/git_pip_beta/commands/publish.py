from pathlib import Path
import subprocess
import tomllib  # Python 3.11+
from cleo.commands.command import Command
from ..processor import run_shell

class PublishCommand(Command):
    name = "publish"
    description = "Publish the current version by tagging and pushing to Git."

    def handle(self) -> int:
        pyproject_path = Path("pyproject.toml")

        if not pyproject_path.exists():
            self.line_error("pyproject.toml not found.")
            return 1

        # Parse version
        with pyproject_path.open("rb") as f:
            pyproject = tomllib.load(f)

        try:
            version = pyproject["project"]["version"]
        except KeyError:
            self.line_error("Version not found in pyproject.toml.")
            return 1

        tag = f"v{version}"

        # Ensure clean commit state
        
        status = run_shell("git status --porcelain", capture_output=True, text=True)
        if status.stdout.strip():
            self.line_error("Uncommitted changes exist. Commit first.")
            return 1

        # Create tag
        run_shell(f"git tag {tag}", check=True)
        run_shell(f"git push origin {tag}", check=True)

        self.line(f"📦 Published version {tag}")
        return 0
