import json
import unittest

from c9freeform import cases


class FixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = cases.load()
        cls.expected = {}
        lines = (cases.ROOT / "fixtures/expected.tsv").read_text(
            encoding="utf-8").splitlines()[1:]
        for line in lines:
            cid, ver, res = line.split("\t")
            cls.expected[(cid, ver)] = json.loads(res)

    def test_expected_covers_every_case(self):
        self.assertEqual(len(self.expected), 2 * len(self.cases))

    def test_model_matches_derivation_and_hand(self):
        for c in self.cases:
            for ver in ("pre", "post"):
                with self.subTest(case=c["id"], version=ver):
                    _label, res = cases.run(c, ver)
                    self.assertEqual(res, self.expected[(c["id"], ver)])
                    self.assertEqual(res, c["hand"][ver])

    def test_acceptance_positive_evaluated_before_literal_after(self):
        for c in self.cases:
            if c["class"] == "pos":
                with self.subTest(case=c["id"]):
                    self.assertIn(cases.run(c, "pre")[0],
                                  ("TWIG_EVALUATED", "TWIG_ERROR"))
                    self.assertEqual(cases.run(c, "post")[0], "LITERAL")

    def test_acceptance_negatives_unchanged(self):
        for c in self.cases:
            if c["class"] == "neg":
                with self.subTest(case=c["id"]):
                    self.assertEqual(cases.run(c, "pre"), cases.run(c, "post"))

    def test_p01_49_before_literal_after(self):
        c = next(x for x in self.cases if x["id"] == "p01_value_arith")
        self.assertEqual(cases.run(c, "pre")[1], [["value", "49"]])
        self.assertEqual(cases.run(c, "post")[1], [["value", "{{ 7*7 }}"]])


if __name__ == "__main__":
    unittest.main()
