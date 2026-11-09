import ast
import unittest
from pathlib import Path

from c9freeform import attributes, twig

SRC = Path(__file__).resolve().parent.parent / "src" / "c9freeform"


def post(attrs, props=None):
    return attributes.evaluate("post", attrs, props or {})


class Inert(unittest.TestCase):
    def test_no_eval_exec_or_process(self):
        banned = {"eval", "exec", "compile", "__import__", "system", "popen",
                  "Popen", "getenv", "environ"}
        for f in SRC.glob("*.py"):
            for node in ast.walk(ast.parse(f.read_text(encoding="utf-8"))):
                name = (node.id if isinstance(node, ast.Name) else
                        node.attr if isinstance(node, ast.Attribute) and not (
                            isinstance(node.value, ast.Name) and node.value.id == "re")
                        else None)
                self.assertNotIn(name, banned, f.name)

    def test_constants_are_placeholders(self):
        for v in twig.CONSTANTS.values():
            self.assertRegex(v, r"^<[A-Z_]+>$")


class TwigEdges(unittest.TestCase):
    def test_unknown_constant_and_function_error(self):
        for src in ("{{ constant('DB_PASSWORD') }}", "{{ getenv('X') }}",
                    "{{ craft.app }}", "{% set a = 1 %}", "{# c #}", "{{ }}",
                    "}}", "{{ 'a' * 2 }}", "{{ 9999999999 * 9 }}"):
            with self.subTest(src=src), self.assertRaises(twig.TwigError):
                twig.render(src, {})

    def test_size_limit(self):
        with self.assertRaises(twig.TwigError):
            twig.render("x" * (twig.MAX_LEN + 1), {})

    def test_precedence_and_concat(self):
        self.assertEqual(twig.render("{{ 1 + 2 * 3 }}", {}), "7")
        self.assertEqual(twig.render("{{ (1 + 2) * 3 }}", {}), "9")
        self.assertEqual(twig.render("{{ 'a' ~ 1 + 1 }}", {}), "a2")


class ExclusionEdges(unittest.TestCase):
    def test_exclusion_is_case_sensitive(self):
        # strict in_array (5f755532:L19): "Value" is not excluded. Observation
        # about the model only; HTML attribute names are case-insensitive.
        self.assertEqual(post([("Value", "{{ 7*7 }}")])[1][0][1], "49")

    def test_key_with_spaces_is_not_excluded(self):
        self.assertEqual(post([(" value", "{{ 7*7 }}")])[1][0][1], "49")

    def test_empty_values_never_rendered(self):
        for v in ("", "0"):
            self.assertEqual(attributes.evaluate("pre", [("class", v)], {})[0],
                             "LITERAL")

    def test_malformed_value_in_post_is_left_alone(self):
        self.assertEqual(post([("name", "{{ broken")])[0], "LITERAL")

    def test_malformed_key_still_errors_in_post(self):
        self.assertEqual(post([("{{ x", "1")])[0], "TWIG_ERROR")

    def test_bad_version(self):
        with self.assertRaises(ValueError):
            attributes.to_html_tag_array("v9", [], {})


if __name__ == "__main__":
    unittest.main()
