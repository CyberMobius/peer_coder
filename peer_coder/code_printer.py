from typing import List, Iterator
from rich.syntax import Syntax
from rich.console import Console, RenderResult
import os
import glob
import random
import ast


def get_python_files_from_repo(dir_path: str) -> Iterator[str]:
    """Given a path to a directory, return an iterator of all python files nested in
    that repository.

    Parameters
    ----------
    dir_path : str
        A path to a directory of code

    Returns
    -------
    List[str]
        An iterator of file paths to python files
    """
    return glob.iglob(net_x_path + r"/**/*.py", recursive=True)


def pick_defs_from_string(code: str) -> List[ast.FunctionDef]:
    parse_tree = ast.parse(code)

    functions: List[ast.FunctionDef]
    functions = [node for node in ast.walk(parse_tree) if type(node) == ast.FunctionDef]
    return functions


def pick_defs_from_file(file_path: str) -> List[ast.FunctionDef]:
    if not os.path.exists(file_path):
        return None

    with open(file_path) as f:
        code = f.read()

    return pick_defs_from_string(code)


def turn_def_token_to_code(token: ast.FunctionDef) -> Syntax:
    code = ast.unparse(token)
    syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
    return syntax


def random_def_syntax_from_file(file_name: str):
    def_tokens = pick_defs_from_file(file_name)
    return turn_def_token_to_code(random.choice(def_tokens))


def pretty_print_syntax(syntax: Syntax) -> None:
    class _SimpleSyntax:
        def __init__(self, result: RenderResult):
            self.result = result

        def __rich_console__(self, a, b):
            return self.result

    console = Console()
    # for line in syntax.__rich_console__(console, console.options):
    #     # print(line)
    #     console.print(_SimpleSyntax(line))

    console.print(syntax, end="")


if __name__ == "__main__":
    net_x_path = os.path.join(
        "..", "networkx", "networkx", "algorithms", "tree", "mst.py"
    )
    net_x_path = os.path.abspath(net_x_path)
    # print(net_x_path)

    # path_gen = get_python_files_from_repo(net_x_path)
    # path = next(path_gen)
    my_syntax = random_def_syntax_from_file(net_x_path)
    pretty_print_syntax(my_syntax)
