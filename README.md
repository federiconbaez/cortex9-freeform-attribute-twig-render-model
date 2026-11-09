# cortex9-freeform-attribute-twig-render-model

Offline, inert model of **CVE-2026-73858** (GHSA-gxrg-x694-283w, CWE-1336):
in Solspace Freeform for Craft CMS 5.0.0-5.10.13,
`Attributes::toHtmlTagArray()` passed **every** non-empty attribute value
through Freeform's isolated Twig renderer, including `value`, `name` and
`id`, which can carry submitted field values. A `{{ ... }}` typed into a
public form was evaluated (the advisory confirms PHP/OS/path constants).
The fix, commit `5f7555320635f1cd3b4c478aa0b58e8c3144313b`, skips Twig for
those three keys. It is in **5.10.14** (released 2025-05-13; the CVE was
published 2026-09-23). That containment was checked before building:
[evidence/fix-in-v5.10.14.md](evidence/fix-in-v5.10.14.md).

Spanish: [README.es.md](README.es.md). Exercises: [PRACTICE.md](PRACTICE.md).

## The model

- `src/c9freeform/attributes.py`: the loop of `toHtmlTagArray()` before
  (diff L300) and after (L17, L302-304). Keys are always rendered (L299);
  PHP `empty()` (so `""` and `"0"` are never rendered); strict, case-sensitive
  `in_array`.
- `src/c9freeform/twig.py`: a tiny Twig stand-in (`{{ }}`, int/str literals,
  props, `+ - *`, `~`, `constant('NAME')`). `constant()` returns fixed
  **placeholders** such as `<PHP_VERSION>`; there is no PHP, no Twig, no
  Craft. Anything else is a `TwigError` (the model's render error).

## Differential evidence (`results/summary.csv`)

| Class | n | pre | post |
|---|---|---|---|
| pos | 6 | 5 `TWIG_EVALUATED`, 1 `TWIG_ERROR` | 6 `LITERAL` |
| neg | 5 | 2 evaluated (admin `class`/`data-*`), 3 literal | identical to pre |
| observation | 1 | `Value` (capital V) evaluated | still evaluated |

`p01`: `value = "{{ 7*7 }}"` gives `49` before and stays literal after.
`p06`: a key that *renders to* `value` is excluded too, because the key is
rendered before the check. `o01` is an **unverified model observation**
(strict `in_array` is case-sensitive); nothing shows Freeform ever passes
submitted data under such a key.

## Run

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 scripts/derive_expected.py | diff - fixtures/expected.tsv
python3 scripts/gen_results.py /tmp/r && diff -r results /tmp/r
```

`fixtures/expected.tsv` comes from `scripts/derive_expected.py`, an
independent derivation (restricted `ast` walk, no `eval`) that does not
import `src/`. Python 3.10+ standard library only.

A model is not a finding. See [LIMITATIONS.md](LIMITATIONS.md) and
[SOURCES.md](SOURCES.md). License: Apache-2.0.
