#!/usr/bin/env python3
"""Independent derivation of fixtures/expected.tsv (does not import src/).

From the saved diff of commit 5f75553: keys are always rendered
(5f755532:L16); before, every non-empty value was rendered (5f755532:L17);
after, values under the keys value/name/id (strict in_array, 5f755532:L9 +
5f755532:L19) are left as written. Twig
is re-derived with Python's ast module restricted to int/str constants,
+ - * and a whitelisted constant() call, after mapping `~` to `+` on
strings. It never calls eval.
"""
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONST = {"PHP_VERSION", "PHP_OS", "CRAFT_BASE_PATH", "CRAFT_VENDOR_PATH"}


class Bad(Exception):
    pass


def ev(node, props):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, str)):
        return node.value
    if isinstance(node, ast.Name):
        if node.id not in props:
            raise Bad(node.id)
        return props[node.id]
    ops = (ast.Add, ast.Sub, ast.Mult)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ops):
        a, b = ev(node.left, props), ev(node.right, props)
        if isinstance(node.op, ast.Add) and isinstance(a, str):
            return a + str(b)
        if not (isinstance(a, int) and isinstance(b, int)):
            raise Bad("types")
        return {ast.Add: a + b, ast.Sub: a - b, ast.Mult: a * b}[type(node.op)]
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id == "constant" and len(node.args) == 1
            and isinstance(node.args[0], ast.Constant)
            and node.args[0].value in CONST):
        return f"<{node.args[0].value}>"
    raise Bad(ast.dump(node))


def twig(text, props):
    def one(m):
        expr = m.group(1).strip()
        # `~` is Twig concatenation; make its operands strings first.
        if "~" in expr:
            parts = [p.strip() for p in expr.split("~")]
            vals = (ev(ast.parse(p, mode="eval").body, props) for p in parts)
            return "".join(str(v) for v in vals)
        try:
            tree = ast.parse(expr, mode="eval")
        except SyntaxError as exc:
            raise Bad("syntax") from exc
        return str(ev(tree.body, props))
    out = re.sub(r"\{\{(.*?)\}\}", one, text)
    if "{{" in out or "}}" in out:
        raise Bad("delimiter")
    return out


def run(ver, attrs, props):
    rows = []
    try:
        for key, value in attrs:
            key = twig(key, props)
            empty = value in ("", "0")
            skip = empty or (ver == "post" and key in ("value", "name", "id"))
            rows.append([key, value if skip else twig(value, props)])
    except Bad:
        return "TWIG_ERROR"
    return rows


def main():
    data = json.loads((ROOT / "fixtures/cases.json").read_text(encoding="utf-8"))
    out = ["id\tversion\tresult"]
    for c in data["cases"]:
        for ver in ("pre", "post"):
            res = json.dumps(run(ver, c["attrs"], c["props"]))
            out.append(f"{c['id']}\t{ver}\t{res}")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
