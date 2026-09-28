# doctoc — AI assistant context

A Python CLI (`doctoc`) that generates and maintains a Table of Contents block inside Markdown
files, with optional hyperlink validation. Published to PyPI as `doctoc`.

## Layout

- `doctoc/cli.py` — Click CLI entry point (`main()`), argument parsing, per-file error handling,
  link-check orchestration.
- `doctoc/core.py` — `modify_and_write()`: finds the existing `TOC_START_TAG`/`TOC_END_TAG` markers
  and rewrites content between them, or inserts a fresh TOC block at the top of the file if no
  markers exist yet.
- `doctoc/markdown.py` — `headers()` (fenced-code-block-aware heading scanner), `as_link()` (slug
  generator — see "Known correctness gap" below), `toc()` (nested bullet-list builder, dedupes
  repeated headers), `get_links()` (inline-link extractor), `escape()`.
- `tests/test_doctoc.py` — one file covering all of the above.

## Commands

```bash
pip install -e .
pip install -r requirements.txt

pytest tests/                  # run tests
black .                        # format (CI checks this — run before opening a PR)
```

## CLI surface (as of v1.1.1)

`doctoc [OPTIONS] MARKDOWN_FILES...` — accepts multiple paths and/or glob patterns, each processed
independently (no cross-file combining today).

- `-o, --outfile PATH` — write to a separate file (single-file input only)
- `-cl, --check-links` — validate hyperlinks (internal `#anchor` and `http(s)://`)
- `-t, --title TEXT` — custom TOC header line
- `-d, --max-depth INT` — cap TOC to headings at or above this depth

## Known correctness gap — read before touching `as_link()`

`as_link()` in `markdown.py` silently strips periods instead of converting them to hyphens, so a
numbered heading like `1.1 My first header` produces the slug `11-my-first-header` instead of
GitHub's actual `1-1-my-first-header`. This is a confirmed, real bug (issue #21) with a real user
report — several other open issues (`#10` custom link generation) are downstream of this same
function. Any fix must also handle the edge case where naively converting periods to hyphens
produces a double-hyphen (`1. My first header` → `1--my-first-header`).

## Conventions

- **Formatting**: Black only, enforced by CI (`.github/workflows/ci.yaml`, Python 3.9–3.12 matrix).
- **Commit types** (`contribution.md`): `feat`, `fix`, `hotfix`, `refactor`, `docs`, `style`, `test`,
  `chore`, `perf`, `ci`, `build` — enforced on PR titles by `pr-title.yaml`
  (`amannn/action-semantic-pull-request`).
- **Branch naming**: `feature/your-feature-name` per `contribution.md` — align the branch's implied
  type with the eventual PR title type for consistency, though (same as our other repos) the actual
  version bump comes from the PR title / squash-merge commit, not the branch name.
- **Releases**: fully automated — `release.yaml` runs `release-please` on every push to `main`,
  driven entirely by PR-title conventional-commit types (`feat`→minor, `fix`→patch, `!`→major,
  everything else→no release). Confirmed working from `CHANGELOG.md` history (1.1.0→1.1.1). Don't
  hand-edit `CHANGELOG.md`. `publish.yaml` then publishes to PyPI automatically when a GitHub
  Release is published.
- **Dependencies**: Dependabot handles `pip` and `github-actions` version bumps weekly — don't open
  PRs that just bump a dependency.
- **Tests required**: every change needs a test. For a bug fix, the test must fail before the fix
  and pass after — never claim a bug exists without a reproducing test.
- **No AI attribution.** Never add a `Co-Authored-By: Claude …` trailer to a commit, never add
  "Generated with Claude Code" (or any mention of Claude/Anthropic/an AI tool) to a commit message
  or PR description, and never include a `claude.ai/code/session_…` link.

## Issue-based backlog (no agent-backlog.md here)

Unlike some of our other repos, this one uses **GitHub Issues directly** as the backlog, not a
markdown file — it already had a real issue tracker in active use. Labels:

- `type:bug` / `type:enhancement` / `type:docs` / `type:question` / `type:wontfix`
- `priority:high` / `priority:medium` / `priority:low`
- `status:blocked` (waiting on something external) / `status:needs-info` (waiting on the reporter)
- `agent-ready` — curated by a human as well-scoped enough for an automated routine to pick up
  unattended. **Only issues with this label should be picked up automatically** — an open issue
  without it may still need human discussion first, even if it looks simple.

If you're an automated routine working this repo: query open issues filtered to `agent-ready`,
implement exactly what the issue describes (its acceptance criteria, if present, are the definition
of done), open a PR referencing the issue (`Closes #N`), and let the PR's merge close the issue —
don't close it yourself before the fix is actually merged.
