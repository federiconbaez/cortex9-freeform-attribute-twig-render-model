"""``Attributes::toHtmlTagArray()`` before and after commit 5f75553.

Diff lines (``cat -n`` of the saved diff):
  L17 (+)  EXCLUDED_TWIG_ATTRIBUTES = ['value', 'name', 'id']
  L299     $key = $twig->render($key, $properties);
  L300 (-) $value = !empty($value) ? $twig->render($value, $properties) : $value;
  L302-304 (+) if (!empty($value) && !\\in_array($key, EXCLUDED, true)) { render }
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
        key = twig.render(key, props)  # L299, both versions
        if version == "pre":
            render = not php_empty(value)  # L300
            rule = "L300"
        else:
            # L302: in_array(..., true) is a strict, case-sensitive match
            render = not php_empty(value) and key not in EXCLUDED_TWIG_ATTRIBUTES
            rule = "L302-304"
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
