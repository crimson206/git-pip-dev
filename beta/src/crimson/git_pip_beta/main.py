from cleo.application import Application
from cleo.commands.completions_command import CompletionsCommand

from crimson.git_pip_beta.commands.install import InstallCommand  # or wherever you place it
from crimson.git_pip_beta.commands.publish import PublishCommand

def main():
    app = Application("git-pip-beta")

    app.add(InstallCommand())
    app.add(PublishCommand())
    app.add(CompletionsCommand())  # ⬅️ 여기에 추가

    app.run()

if __name__ == "__main__":
    main()
