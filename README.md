Lox
===

This repository contains my Python implementation of the Lox interpreter
developed as part of the awesome
[Crafting Interpreters](https://craftinginterpreters.com/) book.

Part of the reason I decided to implement Lox in Python was that
it allowed me to get experience from newish Python features like
[dataclasses](https://docs.python.org/3/library/dataclasses.html),
[walrus](https://docs.python.org/3/reference/expressions.html?highlight=walrus#assignment-expressions)
and [structural pattern matching](https://peps.python.org/pep-0636/)
that I cannot yet use in my day-to-day work.

For an example of the supported syntax see [example.lox](example.lox).
If you clone this repository, you can execute it like this:

    python -m lox example.lox
