# ngv_reports_ibkr

Python package that pulls trade and position data from Interactive Brokers (Flex Web
Service and TWS realtime) and turns it into reports.

## Commits

Write every commit as a Conventional Commit so release-please can version and changelog it. Format: `<type>(<scope>): <imperative description>`.

Types (must match `release-please-config.json` `changelog-sections`): `feat`, `fix`, `docs`, `refactor`, `chore`, `perf`, `test`, `ci`, `build`, `style`.

Scope is optional — a short area word like `flex`, `trades`, `schemas`, `docs`, `deps`. Use `BREAKING CHANGE:` in the body (or `!` after type/scope) for breaking changes.

Rules: lowercase type/scope, imperative mood, no capital after the colon, keep the subject under ~70 chars. Apply this to **each** commit, not just PR titles.

Examples: `feat(flex): implement version 3 with custom start/end dates`, `fix(schemas): allow nullable exec ids`, `docs: cross-check docs against codebase`.

## Pull Requests

### Pull Request Title

The PR title becomes the squash-merge commit subject, so it must be a Conventional Commit (see **Commits** above): `<type>(<scope>): <imperative description>`. release-please parses it to version and changelog the release.

- Use a valid type (`feat`, `fix`, `docs`, `refactor`, `chore`, `perf`, `test`, `ci`, `build`, `style`); optional scope.
- Lowercase type/scope, imperative mood, no capital after the colon, subject under ~70 chars.

### Pull Request Description

When opening or updating pull requests, include the following write-up in the PR body.

- Summary (required). Less than 100 words. What changed and why (not a file list)
- Features (optional). Bullet list of new behavior/capabilities, or "N/A".
- Refactoring (optional). Explain what changed and why. Describe new code structure and patterns.
- Fixes (optional). Bullet list of bugs corrected/remediation, or "N/A".
- Documentation (required if behavior changed)
- Additional notes (when applicable). Link issue(s) or external resources.

## Docs Style

Compact, high signal to noise — write descriptions optimized for an engineer-to-engineer dialogue.

- Be concise. Prefer short sentences and direct statements.
- Focus on actionable information. Avoid filler, marketing, and verbosity.
- Use plain language and concrete terms.
- Keep sections small; remove anything nonessential.
- Use bullets for quick scanning; avoid long paragraphs.
- Favor commands/examples over prose.
- Avoid redundancy.
