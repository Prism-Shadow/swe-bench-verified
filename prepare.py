# /// script
# requires-python = ">=3.10"
# dependencies = ["pyarrow>=14"]
# ///
"""Materialize the official SWE-bench issue and grading files for one package."""
import argparse
import json
import os
import shutil
import tempfile
import urllib.request
from pathlib import Path

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent
DATASET = "Verified"
REVISION = "78f471bf655a3137b2e8a75af1501690ec009ec3"
URL = (f"https://huggingface.co/datasets/SWE-bench/SWE-bench_{DATASET}/resolve/"
       f"{REVISION}/data/test-00000-of-00001.parquet")


def download():
    directory = ROOT / ".cache"
    directory.mkdir(exist_ok=True)
    target = directory / f"{REVISION}.parquet"
    if target.is_file():
        return target
    with tempfile.NamedTemporaryFile(dir=directory, delete=False) as temporary:
        name = Path(temporary.name)
        try:
            with urllib.request.urlopen(URL, timeout=120) as response:
                shutil.copyfileobj(response, temporary)
            temporary.flush()
            pq.read_schema(name)
            os.replace(name, target)
        finally:
            name.unlink(missing_ok=True)
    return target


def write_task(directory, row):
    base = row["base_commit"]
    header = (f"# {row['repo']} at {base}\n\n"
              "The repository is checked out in `/testbed`. Work there. Changes are collected from the "
              f"final working tree against `{base}`; committing is optional. Do not edit "
              "test files: the verifier restores them before running the official tests.\n\n## Issue\n\n")
    tests = {}
    for key in ("FAIL_TO_PASS", "PASS_TO_PASS"):
        value = row[key]
        tests[key] = json.loads(value) if isinstance(value, str) else value
    if DATASET == "Lite":
        row.pop("difficulty", None)
    files = {"instruction.md": header + row["problem_statement"] + "\n",
             "solution/gold.patch": row["patch"],
             "tests/eval.sh": row["eval_script"],
             "tests/tests.json": json.dumps(tests, indent=2 if DATASET == "Verified" else None),
             "tests/instance.json": json.dumps(row, indent=2, sort_keys=True) + "\n"}
    for relative, content in files.items():
        target = directory / relative
        with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as temporary:
            name = Path(temporary.name)
            try:
                temporary.write(content.encode())
                temporary.flush()
                name.chmod(0o755 if relative == "tests/eval.sh" else 0o644)
                os.replace(name, target)
            finally:
                name.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    packages = sorted(p.name for p in ROOT.glob("penguinharness-benchmark-*") if (p / "tasks").is_dir())
    parser.add_argument("package", choices=packages)
    parser.add_argument("task", nargs="?", help="instance ID; omit to prepare the whole package")
    parser.add_argument("--parquet", type=Path, help="local copy of the pinned official split")
    args = parser.parse_args()
    tasks = ROOT / args.package / "tasks"
    selected = {p.name for p in tasks.iterdir() if (p / "task.toml").is_file()}
    if args.task:
        if args.task not in selected:
            parser.error(f"unknown task in {args.package}: {args.task}")
        selected = {args.task}
    data = pq.read_table(args.parquet or download(), filters=[("instance_id", "in", sorted(selected))])
    rows = data.to_pylist()
    if len(rows) != len(selected) or {r["instance_id"] for r in rows} != selected:
        parser.error("the official split does not contain exactly one row per selected task")
    for row in rows:
        write_task(tasks / row["instance_id"], row)
    print(f"Prepared {len(rows)} Harbor task(s) in {args.package}.")


if __name__ == "__main__":
    main()
