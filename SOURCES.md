# Sources

Local copies under `security-research-45/sources/cve2026/` (not in this
repo), fetched read-only on 2026-11-09. SHA-256 re-verified against
`sources/cve2026/SHA256SUMS` when this repo was built. Line citations: see
"Line citations" below.

| Source | URL | Used for | SHA-256 of copy |
|---|---|---|---|
| Fix commit 5f7555320635f1cd3b4c478aa0b58e8c3144313b (2025-05-13, PR #1986) as `diffs/CVE-2026-73858_craft-freeform_5f7555320635.diff` | https://github.com/solspace/craft-freeform/commit/5f7555320635f1cd3b4c478aa0b58e8c3144313b | `EXCLUDED_TWIG_ATTRIBUTES` (5f755532:L9), key render (5f755532:L16), old value render (5f755532:L17), new guarded render (5f755532:L19-21) | 4f851340fff0d2f88179a1df084530be0415ba8702651a5f50db885bcb6d2c8f |
| GHSA-gxrg-x694-283w (`ghsa_rec/CVE-2026-73858.json`) | https://github.com/solspace/craft-freeform/security/advisories/GHSA-gxrg-x694-283w | affected 5.0.0-5.10.13, patched 5.10.14, CWE-1336, the constants named in "Details" | 437bcd4d5d7f199a460a9e0be2c61161aca7a4bd524514d421ffb359d0e16bd5 |
| NVD CVE-2026-73858 (`nvd/CVE-2026-73858.json`, status Awaiting Analysis) | https://nvd.nist.gov/vuln/detail/CVE-2026-73858 | the CVE ID exists; "fixed in version 5.10.14" | 5c86980965aca0624dc3f224a301a68cf528a55acd2a60068c923c45a754085d |
| Release v5.10.14 and compare 5f75553...v5.10.14 (GitHub API, read-only, 2026-11-09) | https://github.com/solspace/craft-freeform/releases/tag/v5.10.14 | the fix is in 5.10.14; see `evidence/fix-in-v5.10.14.md` | raw responses: see that file |

## Line citations (diff not in this repo)

Every line citation has the form `<tag>:L<n>` or `<tag>:L<n>-<m>`: the real
`cat -n` line(s) of the upstream fix diff. The diff is **not** included in
this repo (upstream license: Solspace license, LICENSE.md); `sources/diffs.tsv` names it:

- `5f755532` → `CVE-2026-73858_craft-freeform_5f7555320635.diff`, SHA-256 `4f851340fff0d2f88179a1df084530be0415ba8702651a5f50db885bcb6d2c8f`,
  https://github.com/solspace/craft-freeform/commit/5f7555320635f1cd3b4c478aa0b58e8c3144313b.diff

`citations.tsv` is the single table of cited ranges; for each range it
stores the SHA-256 of the cited text (lines `start`..`end` of the diff file
exactly as stored, joined with `\n`, no final newline, UTF-8; shell:
`sed -n "${start},${end}p" "$C9_DIFF" | head -c -1 | sha256sum`).

```sh
curl -fsSL -o /tmp/CVE-2026-73858_craft-freeform_5f7555320635.diff https://github.com/solspace/craft-freeform/commit/5f7555320635f1cd3b4c478aa0b58e8c3144313b.diff
sha256sum /tmp/CVE-2026-73858_craft-freeform_5f7555320635.diff   # must be 4f851340fff0d2f88179a1df084530be0415ba8702651a5f50db885bcb6d2c8f
C9_DIFF=/tmp/CVE-2026-73858_craft-freeform_5f7555320635.diff PYTHONPATH=src python3 -m unittest -v tests.test_citations
```

Without `C9_DIFF` (as in CI) `tests/test_citations.py` checks the table
format, that every citation in the repo is in the table and that none lacks
a tag, and reports the content check as an explicit **skip**.

