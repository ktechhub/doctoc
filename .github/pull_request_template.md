## Description

<!-- What does this PR do? Why? -->

## Changes

<!-- Bullet list of what changed -->

## Testing

<!-- How was this tested? Any edge cases covered? -->

---

> **PR title format** — the title drives the release version bump via [Conventional Commits](https://www.conventionalcommits.org/):
>
> | Prefix | Effect | Example |
> |---|---|---|
> | `feat:` | minor bump (1.**x**.0) | `feat: add --max-depth option` |
> | `fix:` | patch bump (1.0.**x**) | `fix: skip headers in code fences` |
> | `feat!:` / `fix!:` | major bump (**x**.0.0) | `feat!: remove setup.py support` |
> | `chore:` / `docs:` / `refactor:` | no release | `docs: update README` |
>
> release-please reads the squashed commit message (= PR title) from `main` to decide the next version and update `pyproject.toml` automatically.
