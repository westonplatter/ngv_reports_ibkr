#!/usr/bin/env python
"""Scan changes for real IBKR data that must not reach the repo.

Enforces `docs/ibkr-sample-data.md`: account IDs, contract IDs,
execution/transaction/order IDs must be anonymized in anything committed.
Symbols, exchanges, sec types, prices, and quantities are deliberately NOT
flagged — the prompt keeps those real so examples stay realistic.

Usage:
    uv run python scripts/ibkr_sensitive_data_check.py              # staged changes, else unstaged
    uv run python scripts/ibkr_sensitive_data_check.py --unstaged   # force unstaged diff
    uv run python scripts/ibkr_sensitive_data_check.py --paths a.md src/   # whole files/dirs
    uv run python scripts/ibkr_sensitive_data_check.py --untracked  # include untracked files
    uv run python scripts/ibkr_sensitive_data_check.py --quiet      # result only, no file list

Exits 1 when anything is flagged, so it can gate a commit hook.
"""

from __future__ import annotations

import argparse
import re
import subprocess  # nosec B404 — only ever used by `_run` to shell out to git; see the note there
import sys
from dataclasses import dataclass
from pathlib import Path

# Values the anonymization prompt hands out as examples. Seeing these is the
# desired end state, not a finding.
ALLOWED: frozenset[str] = frozenset(
    {
        "U1234567",
        "U9999999",
        "U8675309",
        "U7654321",
        "123456789",
        "234567890",
        "345678901",
        "400000001",
        "111111111",
        "222222222",
        "333333333",
        "1000000001",
        "1000000002",
        "1000000003",
        "5000000001",
        "5000000002",
        "5000000003",
        "9000000001",
        "9000000002",
        "9000000003",
        "600000001",
        "600000002",
        "600000003",
        # Non-numeric example forms from the same prompt. These are the *target*
        # of anonymization, so they must never be reported — including where they
        # appear as the suggestion strings in this file.
        "0000abcd.12345678.01.01",
        "0000efgh.23456789.01.01",
        "0000ijkl.34567890.01.01",
        "00aabbcc.00ddeeff.11223344.000",
        "00aabbcc.00ddeeff.55667788.999",
        "FLEX-TX-1000000001",
        "permId 8888888",
        "8888888",
        "9999999",
        "7777777",
    }
)


@dataclass(frozen=True)
class Rule:
    category: str
    pattern: re.Pattern[str]
    suggestion: str


RULES: tuple[Rule, ...] = (
    Rule("account_id", re.compile(r"\bU\d{7}\b"), "U1234567"),
    # conIds, trade IDs, transaction IDs, order IDs all live in this width.
    # Bounded by non-word/non-dot so version strings and decimals do not match.
    Rule("numeric_id", re.compile(r"(?<![\w.])\d{9,10}(?![\w.])"), "123456789 (conId) / 1000000001 (tradeID)"),
    Rule("exec_id", re.compile(r"\b[0-9a-fA-F]{8}\.[0-9a-fA-F]{8}\.\d{2}\.\d{2}\b"), "0000abcd.12345678.01.01"),
    Rule("brokerage_order_id", re.compile(r"\b[0-9a-f]{8}\.[0-9a-f]{8}\.[0-9a-f]{8}\.\d{3}\b"), "00aabbcc.00ddeeff.11223344.000"),
    Rule("synthetic_id", re.compile(r"\b(?:FLEX-TX-|SYNTH-)[\w.-]+"), "FLEX-TX-1000000001"),
    Rule("perm_id", re.compile(r"\bpermId\W+\d{6,}"), "permId 8888888"),
)


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    category: str
    value: str
    context: str
    suggestion: str


def _run(args: list[str]) -> str:
    """Run a git command and return stdout, swallowing failures.

    Every caller passes a literal argv list beginning with `git`, and nothing
    is interpolated into a command string, so there is no shell for input to
    escape into. The one caller-supplied value — a path from `--paths` — is
    placed after `--`, which stops git reading it as an option.
    """
    result = subprocess.run(args, capture_output=True, text=True, check=False, shell=False)  # nosec B603 — fixed git argv, no shell
    return result.stdout


def scan_text(path: str, text: str, *, line_offset: int = 0) -> list[Finding]:
    findings: list[Finding] = []
    for idx, line in enumerate(text.splitlines(), start=1 + line_offset):
        for rule in RULES:
            for match in rule.pattern.findall(line):
                value = match if isinstance(match, str) else match[0]
                if value in ALLOWED:
                    continue
                findings.append(
                    Finding(
                        path=path,
                        line=idx,
                        category=rule.category,
                        value=value,
                        context=line.strip()[:120],
                        suggestion=rule.suggestion,
                    )
                )
    return findings


def scan_diff(diff: str) -> list[Finding]:
    """Scan only added lines of a unified diff, tracking the real line numbers."""
    findings: list[Finding] = []
    current = "<unknown>"
    new_line = 0
    for raw in diff.splitlines():
        if raw.startswith("+++ b/"):
            current = raw[6:]
            continue
        if raw.startswith("@@"):
            header = re.search(r"\+(\d+)", raw)
            new_line = int(header.group(1)) if header else 0
            continue
        if raw.startswith("+") and not raw.startswith("+++"):
            findings.extend(scan_text(current, raw[1:], line_offset=new_line - 1))
            new_line += 1
        elif not raw.startswith("-"):
            new_line += 1
    return findings


def _expand_paths(paths: list[str]) -> list[str]:
    """Expand directories into the files under them, deduped and ordered.

    Directories are resolved through git so ignored trees (`.venv/`,
    `node_modules/`, `scripts/data/`) are skipped; both tracked and untracked
    files are included. Falls back to a plain walk outside a git repo.
    """
    expanded: list[str] = []
    seen: set[str] = set()
    for path in paths:
        if Path(path).is_dir():
            listing = _run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "--", path]).split()
            if not listing:
                listing = [str(p) for p in sorted(Path(path).rglob("*")) if p.is_file()]
            candidates = listing
        else:
            candidates = [path]
        for candidate in candidates:
            if candidate not in seen:
                seen.add(candidate)
                expanded.append(candidate)
    return expanded


def _scan_files(paths: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    for path in paths:
        try:
            with open(path, encoding="utf-8") as handle:
                findings.extend(scan_text(path, handle.read()))
        except (OSError, UnicodeDecodeError):
            continue
    return findings


def collect(args: argparse.Namespace) -> tuple[list[Finding], str, list[str]]:
    if args.paths:
        paths = _expand_paths(args.paths)
        return _scan_files(paths), f"{len(paths)} file(s)", paths

    diff_args = ["git", "diff", "--cached"]
    diff = "" if args.unstaged else _run([*diff_args, "--no-color"])
    scanned = "staged changes"
    if not diff.strip():
        diff_args = ["git", "diff"]
        diff = _run([*diff_args, "--no-color"])
        scanned = "unstaged changes"

    files = _run([*diff_args, "--name-only"]).split()
    findings = scan_diff(diff)
    if args.untracked:
        untracked = _run(["git", "ls-files", "--others", "--exclude-standard"]).split()
        findings.extend(_scan_files(untracked))
        files.extend(path for path in untracked if path not in set(files))
        scanned += " + untracked files"
    return findings, scanned, files


def report(findings: list[Finding], scanned: str, files: list[str], quiet: bool = False) -> int:
    print(f"IBKR data check — scanned {scanned}")
    if not quiet:
        for path in files:
            print(f"  · {path}")
        if not files:
            print("  (nothing to scan)")
    if not quiet:
        print()
    if not findings:
        print("OK: no real IBKR account IDs, contract IDs, or execution/order IDs found.")
        return 0

    by_category: dict[str, int] = {}
    for finding in findings:
        by_category[finding.category] = by_category.get(finding.category, 0) + 1
        print(f"  {finding.path}:{finding.line}  {finding.category}  {finding.value}  -> {finding.suggestion}")
        print(f"      {finding.context}")

    print(f"\nFAIL: {len(findings)} finding(s)")
    for category, count in sorted(by_category.items()):
        print(f"  {category}: {count}")
    print("\nSee docs/ibkr-sample-data.md for the anonymization patterns.")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--unstaged", action="store_true", help="scan the unstaged diff instead of staged")
    parser.add_argument("--untracked", action="store_true", help="also scan untracked files in full")
    parser.add_argument(
        "--paths",
        nargs="*",
        default=None,
        help="scan these files/directories in full instead of a diff (directories recurse)",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="suppress the per-file list; print only the header and the result",
    )
    args = parser.parse_args()

    findings, scanned, files = collect(args)
    return report(findings, scanned, files, quiet=args.quiet)


if __name__ == "__main__":
    sys.exit(main())
