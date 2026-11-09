# Limitations

- **One loop only.** Only the `foreach` of `toHtmlTagArray()` shown in the
  diff is modelled. How Freeform escapes and assembles the final HTML, what
  `EXCLUDED_ATTRIBUTES = ['tag']` does, and which attributes carry submitted
  data are not visible in the diff and are not modelled.
- **Not Twig.** `twig.py` is a small stand-in; real Twig syntax, filters,
  the isolated environment's function list and its sandbox limits are not
  modelled (not verified). `constant()` returns placeholders, never real
  versions or paths.
- **Other attributes.** After the fix, every key other than
  `value`/`name`/`id` is still rendered. Whether submitted values can reach
  another key (or a key differing only in case, `o01`) is **not verified**;
  it is a model observation, not a finding.
- **Release note wording.** The 5.10.14 release says "default field
  values" while the GHSA says "submitted field values"; the model follows
  the diff.
- **Version claims** rely on the GHSA, NVD and the ancestry check in
  `evidence/fix-in-v5.10.14.md`; that 5.10.13 lacks the fix comes only from
  the independent audit.
- This is not a finding and not an exploit.
