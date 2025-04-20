from pathlib import Path
import subprocess
import tomllib
import tomli_w
from cleo.commands.command import Command
from cleo.helpers import option
from ..processor import run_shell

class PublishCommand(Command):
    name = "publish"
    description = "Publish the current version by tagging and pushing to Git."

    options = [
        option("version", "v", flag=False, description="Override version to publish."),
    ]

    def handle(self) -> int:
        pyproject_path = Path("pyproject.toml")

        if not pyproject_path.exists():
            self.line_error("pyproject.toml not found.")
            return 1

        # Parse pyproject.toml
        with pyproject_path.open("rb") as f:
            pyproject = tomllib.load(f)

        version_override = self.option("version")

        if version_override:
            self.line(f"🔧 Overriding version to {version_override}")
            pyproject["project"]["version"] = version_override
            with pyproject_path.open("wb") as f:
                tomli_w.dump(pyproject, f)

            # Auto-commit version bump
            run_shell("git add pyproject.toml", check=True)
            run_shell(f"git commit -m 'chore: set version to {version_override}'", check=True)

        try:
            version = pyproject["project"]["version"]
        except KeyError:
            self.line_error("Version not found in pyproject.toml.")
            return 1

        tag = f"v{version}"

        # Check for uncommitted changes
        status = run_shell("git status --porcelain", capture_output=True, text=True)
        if status.stdout.strip():
            self.line_error("Uncommitted changes exist. Commit first.")
            return 1

        # Create and push tag
        run_shell(f"git tag {tag}", check=True)
        run_shell(f"git push origin {tag}", check=True)

        self.line(f"📦 Published version {tag}")
        return 0
