"""A tiny, inert stand-in for Freeform's isolated Twig renderer.

Supports ``{{ expr }}`` with integer and string literals, variables from the
render properties, ``constant('NAME')`` (looked up in a fixed table of
placeholder strings, never in a real PHP runtime), ``+ - *`` on integers and
``~`` concatenation. ``{% %}``/``{# #}`` and anything else raise
``TwigError``, the model's version of a render error. Nothing is evaluated.
"""
from __future__ import annotations

import re

# Placeholder values only. The advisory lists these constants as reachable
# (GHSA "Details"); the values here are not real versions or paths.
CONSTANTS = {
    "PHP_VERSION": "<PHP_VERSION>",
    "PHP_OS": "<PHP_OS>",
    "CRAFT_BASE_PATH": "<CRAFT_BASE_PATH>",
    "CRAFT_VENDOR_PATH": "<CRAFT_VENDOR_PATH>",
}
MAX_LEN = 4096


class TwigError(Exception):
    pass


_TOK = re.compile(r"\s*(?:(?P<int>\d{1,9})|(?P<str>'[^'\\]*')|"
                  r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)|(?P<op>[-+*~(),]))")


def _tokens(src: str) -> list:
    out, pos = [], 0
    src = src.strip()
    while pos < len(src):
        m = _TOK.match(src, pos)
        if not m or m.end() == pos:
            raise TwigError(f"unexpected character at {pos}")
        out.append((m.lastgroup, m.group(m.lastgroup)))
        pos = m.end()
    if not out:
        raise TwigError("empty expression")
    return out


class _Parser:
    def __init__(self, toks, props):
        self.toks, self.i, self.props = toks, 0, props

    def peek(self):
        return self.toks[self.i] if self.i < len(self.toks) else (None, None)

    def take(self):
        tok = self.peek()
        self.i += 1
        return tok

    def parse(self):
        val = self.concat()
        if self.i != len(self.toks):
            raise TwigError("trailing tokens")
        return val

    def concat(self):
        val = self.additive()
        while self.peek() == ("op", "~"):
            self.take()
            val = _to_str(val) + _to_str(self.additive())
        return val

    def additive(self):
        val = self.term()
        while self.peek() in (("op", "+"), ("op", "-")):
            op = self.take()[1]
            rhs = self.term()
            _ints(val, rhs)
            val = val + rhs if op == "+" else val - rhs
        return val

    def term(self):
        val = self.atom()
        while self.peek() == ("op", "*"):
            self.take()
            rhs = self.atom()
            _ints(val, rhs)
            val = val * rhs
        return val

    def atom(self):
        kind, text = self.take()
        if kind == "int":
            return int(text)
        if kind == "str":
            return text[1:-1]
        if kind == "name":
            if self.peek() == ("op", "("):
                return self.call(text)
            if text not in self.props:
                raise TwigError(f"variable {text} does not exist")
            return self.props[text]
        if (kind, text) == ("op", "("):
            val = self.concat()
            if self.take() != ("op", ")"):
                raise TwigError("unclosed parenthesis")
            return val
        raise TwigError(f"unexpected {text}")

    def call(self, name):
        self.take()  # (
        if name != "constant":
            raise TwigError(f"unknown function {name}")
        kind, text = self.take()
        if kind != "str" or self.take() != ("op", ")"):
            raise TwigError("constant() takes one string literal")
        const = text[1:-1]
        if const not in CONSTANTS:
            raise TwigError(f"constant {const} is not in the model table")
        return CONSTANTS[const]


def _ints(a, b):
    if not (isinstance(a, int) and isinstance(b, int)):
        raise TwigError("arithmetic on non-integers is not modelled")
    if max(abs(a), abs(b)) > 10**9:
        raise TwigError("integer too large for the model")


def _to_str(v) -> str:
    return str(v)


_BLOCK = re.compile(r"\{\{(.*?)\}\}", re.S)


def render(src: str, props: dict) -> str:
    if not isinstance(src, str) or len(src) > MAX_LEN:
        raise TwigError("template type or size")
    if "{%" in src or "{#" in src:
        raise TwigError("statements and comments are not modelled")
    out, pos = [], 0
    for m in _BLOCK.finditer(src):
        out.append(src[pos:m.start()])
        out.append(_to_str(_Parser(_tokens(m.group(1)), props).parse()))
        pos = m.end()
    tail = src[pos:]
    if "{{" in tail or "}}" in tail:
        raise TwigError("unclosed or stray delimiter")
    out.append(tail)
    return "".join(out)
