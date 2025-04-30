from cleo.commands.command import Command
from pathlib import Path
import os
import subprocess
from crimson.git_pip_beta.utils.processor import run_shell

class AutoCompletionCommand(Command):
    name = "auto-completion"
    description = "Automatically enable shell auto-completion (script + config)."

    def handle(self) -> int:
        shell_path = os.getenv("SHELL")
        if not shell_path:
            self.line("<error>Could not determine shell (SHELL env not set).</error>")
            return 1

        shell_type = Path(shell_path).name
        script_name = self._io.input.script_name or "git-pip-beta"

        if shell_type == "bash":
            script_path = Path.home() / f".{script_name}-completion.sh"
            config_file = Path.home() / ".bashrc"
            source_line = f"source {script_path}"
        elif shell_type == "zsh":
            script_path = Path.home() / f".{script_name}-completion.zsh"
            config_file = Path.home() / ".zshrc"
            source_line = f"source {script_path}"
        elif shell_type == "fish":
            script_path = Path.home() / f".config/fish/completions/{script_name}.fish"
            config_file = None  # fish는 따로 등록 불필요
            source_line = None
        else:
            self.line(f"<error>Unsupported shell: {shell_type}</error>")
            return 1

        # 🔁 run completions command: git-pip-beta completions <shell>
        result = run_shell(f"git-pip-beta completions {shell_type}", check=True, capture_output=True, text=True)

        if result.returncode != 0:
            self.line(f"<error>Failed to generate completions: {result.stderr.strip()}</error>")
            return 1

        completion_script = result.stdout
        script_path.parent.mkdir(parents=True, exist_ok=True)
        script_path.write_text(completion_script)
        self.line(f"<info>Completion script written to:</info> {script_path}")

        if config_file and config_file.exists():
            lines = config_file.read_text().splitlines()
            if not any(source_line in line for line in lines):
                with config_file.open("a") as f:
                    f.write(f"\n# Enable {script_name} completion\n{source_line}\n")
                self.line(f"<info>Added to:</info> {config_file}")
            else:
                self.line(f"<comment>Already added to:</comment> {config_file}")

        self.line("<info>✅ Auto-completion setup complete. Restart your shell or run 'source' manually.</info>")
        return 0
