# SWE-bench Verified

- [SWE-bench Verified](penguinharness-benchmark-swe-bench-verified/), 500 tasks.
- [SWE-bench Verified held-out 100](penguinharness-benchmark-swe-bench-verified-heldout-100/), 100 tasks.

## Prepare tasks

Check out the data revision linked in the Case. From this repository root, prepare one instance or omit the instance ID to prepare every task in the selected directory. The first invocation downloads the official split from Hugging Face.

```sh
uv run prepare.py penguinharness-benchmark-swe-bench-verified astropy__astropy-12907
```

For the [500-task batch](penguinharness-benchmark-swe-bench-verified/README.md), prepare the entire split with `uv run prepare.py penguinharness-benchmark-swe-bench-verified`.

Use the `ADAPTER_DIR` supplied by the evaluator when running the Case from this checkout. See the [dataset provenance](penguinharness-benchmark-swe-bench-verified/SOURCE.md) and [notices](THIRD_PARTY_NOTICES.md).
