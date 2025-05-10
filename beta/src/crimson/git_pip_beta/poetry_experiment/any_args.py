from cleo.application import Application
from cleo.commands.command import Command
from cleo.helpers import argument, option


class MyCommand(Command):
    name = "my-command"

    arguments = [argument("value", description="github_id/repo or your module name.")]

    def configure(self):
        self

    # 공식 옵션 정의
    options = [
        option("my-op", flag=True, description="Verbose mode"),
    ]

    def handle(self) -> int:
        self.line("MyCommand 실행됨")

        # 등록된 옵션 처리
        if self.option("my-op"):
            self.line("✅ Verbose 모드가 활성화되었습니다", "info")

        # 미등록 옵션 출력 (디버깅용)
        tokens = self.io.input._tokens
        self.line(f"Raw tokens: {tokens}", "comment")

        return 0


def main():
    app = Application()
    app.add(MyCommand())
    app.run()


if __name__ == "__main__":
    main()
