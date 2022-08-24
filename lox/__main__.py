from pathlib import Path
import sys

from .lox import Lox


match sys.argv[1:]:
    case []:
        Lox().run_prompt()
    case [script]:
        Lox().run_script(Path(script))
    case _:
        sys.exit('Usage: lox [script]')
