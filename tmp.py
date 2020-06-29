from gluepy.commands import call_command, Command


class HelloCommand(Command):
    label = "hello"

    def handle(self, **kwargs):
        print(kwargs)

    def add_arguments(self, parser):
        """Hook to add additional arguments to the parser"""
        parser.add_argument("x")
        parser.add_argument("y")
        parser.add_argument("--foo", "-f", type=str, help="foo", required=True)
        parser.add_argument("--bar", action="store_true", help="bar")


if __name__ == "__main__":
    call_command()
