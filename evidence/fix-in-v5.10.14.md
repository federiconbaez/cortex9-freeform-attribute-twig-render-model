# Is commit 5f75553 in Freeform 5.10.14?

Checked before building, as required. Answer: **yes**.

## 1. Saved sources (`security-research-45/sources/cve2026/`)

- `ghsa_rec/CVE-2026-73858.json` (sha256 437bcd4d5d7f199a460a9e0be2c61161aca7a4bd524514d421ffb359d0e16bd5):
  `vulnerable_version_range` ">= 5.0.0, <= 5.10.13", `first_patched_version`
  "5.10.14"; references both
  `commit/5f7555320635f1cd3b4c478aa0b58e8c3144313b` and `releases/tag/v5.10.14`.
- `nvd/CVE-2026-73858.json` (sha256 5c86980965aca0624dc3f224a301a68cf528a55acd2a60068c923c45a754085d):
  "This issue is fixed in version 5.10.14"; same two references.
- `commit_meta.txt`: 5f75553 dated 2025-05-13T19:34:10Z, 1 file, +5/-1,
  "fix(SFT-2065): fixed a vulnerability issue where isolated twig is being
  parsed in attributes (#1986)".

These name the commit and the release together but do not, on their own,
prove that the tag contains the commit.

## 2. Ancestry, read-only GitHub API, 2026-11-09 (ART)

Raw responses kept outside the repo (they contain upstream committer
e-mail addresses); only the fields used are copied here.

| Request | Field | Value | SHA-256 of raw response |
|---|---|---|---|
| `GET /repos/solspace/craft-freeform/compare/5f7555320635f1cd3b4c478aa0b58e8c3144313b...v5.10.14` | status / ahead_by / behind_by | `ahead` / 1 / 0 | f06a101701ac887d36db56b710b6336dff47c3cdd08cf1a8a87dc616018de73e |
| same | merge_base_commit | 5f7555320635f1cd3b4c478aa0b58e8c3144313b | |
| same | the 1 commit | d0c0da40ae34b9e0963d9c7a3e7ba0f0fc6bbdf0 "v5.10.14", 2025-05-13T19:41:41Z, parent 5f75553 | |
| `GET /repos/solspace/craft-freeform/releases/tags/v5.10.14` | published_at / target | 2025-05-13T19:42:39Z / `v5` | 4c504952706262a9c9d29a73612fb9ca8790002541d9ede2fd253361739c9569 |
| same | body, "Security" | "Fixed a vulnerability allowing isolated Twig template rendering in default field values." | |

`behind_by = 0` with merge base equal to 5f75553 means the tag v5.10.14
contains the fix; its tag commit has 5f75553 as its only parent.

## 3. Independent audit

`security-research-45/review/cve2026-audit-sentinel.md` (sha256
38e45892cc42d5ca39ecbd049f35cea0147b70b3a4c3e7f6aba35025a5418d9a), section
3.2, reaches the same result independently (v5.10.14 contains 5f75553;
v5.10.13 does not) and concludes the 2026 CVE was assigned to a fix released
in May 2025.

Not verified here: that v5.10.13 lacks the fix (taken from the audit only).
