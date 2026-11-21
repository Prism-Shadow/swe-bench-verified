# SWE-bench Verified

- [SWE-bench Verified](penguinharness-benchmark-swe-bench-verified/), 500 tasks.
- [SWE-bench Verified held-out 100](penguinharness-benchmark-swe-bench-verified-heldout-100/), 100 tasks.

## Prepare tasks

Check out the data revision linked in the Case. From this repository root, prepare one instance or omit the instance ID to prepare every task in the selected directory. The first invocation downloads the official split from Hugging Face.

```sh
uv run prepare.py penguinharness-benchmark-swe-bench-verified astropy__astropy-12907
```

For the [500-task batch](penguinharness-benchmark-swe-bench-verified/README.md), prepare the entire split with `uv run prepare.py penguinharness-benchmark-swe-bench-verified`.

For each run, check out the [shared adapter](https://github.com/Prism-Shadow/penguin-harness-benchmark/tree/496175abb179dd094fe59e7e12e0e11699a523e2/agents) at the revision in the Case and set `ADAPTER_DIR` to the absolute path of its `agents/` directory. Run the Harbor command in the Case from this checkout. See the [dataset provenance](penguinharness-benchmark-swe-bench-verified/SOURCE.md) and [notices](THIRD_PARTY_NOTICES.md).
