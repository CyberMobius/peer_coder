from rich.console import Console


def test():
    console = Console()
    console.print("123")
    console.print("abc")
    console.clear()
    console.print("456")


test()