import ast
import glob
import os
import random
from time import sleep
from typing import Iterator, List

from rich.console import Console, RenderResult
from rich.segment import Segment
from rich.syntax import Syntax

WORDS_PER_MINUTE = 80
CHARS_PER_WORD = 5
CHAR_RATE = 60 / (CHARS_PER_WORD * WORDS_PER_MINUTE)


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
    return glob.iglob(test_path + r"/**/*.py", recursive=True)


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
    console = Console()

    class _RevealingSyntax:
        def __init__(self, result: RenderResult):
            self.result = [i for i in result]

            self.progress = 0
            self.length = sum(len(i.text) for i in self.result if not i.text.isspace())

        def __rich_console__(self, a, b):
            self.progress += 1
            current_partial_segment = None

            current_char_index = 0
            i: Segment
            for index, i in enumerate(self.result):
                if i.text.isspace():
                    continue

                if current_char_index + len(i.text) < self.progress:
                    current_char_index += len(i.text)

                elif current_char_index + len(i.text) == self.progress:
                    yield from self.result[: index + 1]
                    return

                else:
                    partial_length = self.progress - current_char_index
                    current_partial_segment = Segment(
                        i.text[:partial_length], i.style, i.is_control
                    )
                    yield from self.result[:index] + [current_partial_segment]
                    return
            return

        def __len__(self):
            return self.length

    code = _RevealingSyntax(syntax.__rich_console__(console, console.options))

    for _ in range(len(code)):
        console.clear()
        console.print(code)
        sleep(CHAR_RATE)


if __name__ == "__main__":
    test_path = os.path.join(".", "peer_coder", "test.py")
    test_path = os.path.abspath(test_path)
    # print(net_x_path)

    # path_gen = get_python_files_from_repo(net_x_path)
    # path = next(path_gen)
    my_syntax = random_def_syntax_from_file(test_path)
    pretty_print_syntax(my_syntax)
