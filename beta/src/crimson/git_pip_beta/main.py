from cleo.application import Application
from cleo.commands.completions_command import CompletionsCommand
from crimson.git_pip_beta.commands.install import (
    InstallCommand,
)  # or wherever you place it
from crimson.git_pip_beta.commands.publish import PublishCommand
from crimson.git_pip_beta.commands.completion import AutoCompletionCommand


def main():
    app = Application("git-pip-beta", version="0.1.0")

    app.add(InstallCommand())
    app.add(PublishCommand())
    app.add(CompletionsCommand())
    app.add(AutoCompletionCommand())

    app.run()


if __name__ == "__main__":
    main()
