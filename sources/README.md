# sources/

The upstream diff behind every line citation is **not** in this repo: it
belongs to solspace/craft-freeform (Copyright © Solspace, Inc.) and is under that project's license (Solspace license, LICENSE.md), not this
repo's Apache-2.0. This directory only holds `diffs.tsv`: tag, file name,
SHA-256 and upstream URL of the diff.

Fetch it read-only and run the content check:

```sh
curl -fsSL -o /tmp/CVE-2026-73858_craft-freeform_5f7555320635.diff https://github.com/solspace/craft-freeform/commit/5f7555320635f1cd3b4c478aa0b58e8c3144313b.diff
sha256sum /tmp/CVE-2026-73858_craft-freeform_5f7555320635.diff   # must be 4f851340fff0d2f88179a1df084530be0415ba8702651a5f50db885bcb6d2c8f
C9_DIFF=/tmp/CVE-2026-73858_craft-freeform_5f7555320635.diff PYTHONPATH=src python3 -m unittest -v tests.test_citations
```

The URL above returned a byte-identical file (same SHA-256) on 2026-11-09.
Range hashes in `../citations.tsv` use this normalisation: lines
`start`..`end` of the diff exactly as stored (no `cat -n` prefix, nothing
stripped), joined with `\n`, no final newline, UTF-8 bytes, SHA-256.
