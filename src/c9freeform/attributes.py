"""``Attributes::toHtmlTagArray()`` before and after commit 5f75553.

Citations are real ``cat -n`` lines of the upstream diff of 5f75553 (not
in this repo; see sources/diffs.tsv and tests/test_citations.py):
  5f755532:L9      post adds a constant listing the keys value, name, id
  5f755532:L16     every key is rendered as a Twig template (both versions)
  5f755532:L17     pre: every non-empty value is rendered
  5f755532:L19-21  post: a non-empty value is rendered only when its key is
                   not in that list (strict, case-sensitive in_array)
Only this loop is modelled; how Freeform builds the final HTML is not.
"""
from __future__ import annotations

from . import twig

EXCLUDED_TWIG_ATTRIBUTES = ("value", "name", "id")


def php_empty(value) -> bool:
    """PHP ``empty()`` for the scalar types attributes can hold."""
    return value in (None, False, "", "0", 0, 0.0) or value == []


def to_html_tag_array(version: str, attrs: list, props: dict) -> list:
    """attrs: list of (key, value) pairs in order. Returns a list of
    (key, value, decision) or raises twig.TwigError."""
    if version not in ("pre", "post"):
        raise ValueError(version)
    out = []
    for key, value in attrs:
        key = twig.render(key, props)  # 5f755532:L16, both versions
        if version == "pre":
            render = not php_empty(value)  # 5f755532:L17
            rule = "5f755532:L17"
        else:
            # 5f755532:L19: in_array(..., true) is a strict, case-sensitive match
            render = not php_empty(value) and key not in EXCLUDED_TWIG_ATTRIBUTES
            rule = "5f755532:L19-21"
        if render:
            new = twig.render(value, props)
            out.append((key, new, f"RENDERED:{rule}"))
        else:
            out.append((key, value, f"LITERAL:{rule}"))
    return out


def evaluate(version: str, attrs: list, props: dict) -> tuple:
    """(label, rendered pairs). Labels: TWIG_EVALUATED (some value changed
    by rendering), LITERAL (no value changed), TWIG_ERROR."""
    try:
        rows = to_html_tag_array(version, attrs, props)
    except twig.TwigError as exc:
        return "TWIG_ERROR", str(exc)
    changed = any(new != old for (_k, new, _d), (_k0, old) in
                  zip(rows, attrs, strict=True))
    return ("TWIG_EVALUATED" if changed else "LITERAL"), rows
