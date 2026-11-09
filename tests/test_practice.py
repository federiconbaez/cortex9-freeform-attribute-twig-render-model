"""Answers to PRACTICE.md, one test per level."""
import unittest

from c9freeform import attributes as a


def both(attrs, props=None):
    return [a.evaluate(v, attrs, props or {})[1] for v in ("pre", "post")]


class Practice(unittest.TestCase):
    def test_level_1_admin_template(self):
        self.assertEqual(both([("class", "f-{{ h }}")], {"h": "x"})[1][0][1], "f-x")

    def test_level_2_value_rendered_before(self):
        self.assertEqual(both([("value", "{{ 7*7 }}")])[0][0][1], "49")

    def test_level_3_value_literal_after(self):
        self.assertEqual(both([("value", "{{ 7*7 }}")])[1][0][1], "{{ 7*7 }}")

    def test_level_4_constant(self):
        pre, post = both([("value", "{{ constant('PHP_OS') }}")])
        self.assertEqual(pre[0][1], "<PHP_OS>")
        self.assertEqual(post[0][1], "{{ constant('PHP_OS') }}")

    def test_level_5_render_error(self):
        self.assertEqual(a.evaluate("pre", [("value", "{{ 7*")], {})[0], "TWIG_ERROR")

    def test_level_6_php_empty(self):
        self.assertEqual(both([("value", "0")]),
                         [[("value", "0", "LITERAL:5f755532:L17")],
                          [("value", "0", "LITERAL:5f755532:L19-21")]])

    def test_level_7_other_keys(self):
        self.assertEqual(both([("data-n", "{{ 7*7 }}")])[1][0][1], "49")


if __name__ == "__main__":
    unittest.main()
