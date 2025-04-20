import platform
from crimson.git_pip_beta.processor import run_shell
import pytest


def test_run_shell_basic():
    result = run_shell("echo hello", capture_output=True)
    assert "hello" in result.stdout

@pytest.mark.skipif(platform.system().lower() != "darwin", reason="zsh only on macOS")
def test_run_shell_zsh():
    result = run_shell("echo zsh", shell_preference="zsh", capture_output=True)
    assert "zsh" in result.stdout
