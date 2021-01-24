from typing import Optional, Set, Tuple, Union
from rich.console import Console, ConsoleOptions, RenderResult
from rich.syntax import Syntax, SyntaxTheme


class ActiveSyntax(Syntax):
    def __init__(
        self,
        code: str,
        lexer_name: str,
        *,
        theme: Union[str, SyntaxTheme],
        dedent: bool,
        line_numbers: bool,
        start_line: int,
        line_range: Tuple[int, int],
        highlight_lines: Set[int],
        code_width: Optional[int],
        tab_size: int,
        word_wrap: bool,
        background_color: str,
        indent_guides: bool
    ) -> None:
        super().__init__(
            code,
            lexer_name,
            theme=theme,
            dedent=dedent,
            line_numbers=line_numbers,
            start_line=start_line,
            line_range=line_range,
            highlight_lines=highlight_lines,
            code_width=code_width,
            tab_size=tab_size,
            word_wrap=word_wrap,
            background_color=background_color,
            indent_guides=indent_guides,
        )

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        return super().__rich_console__(console, options)