## Summary

<!-- What does this PR do? Why? -->

## Type of change

<!-- Your PR title must follow conventional commits format: type(scope): description -->
<!-- Allowed types: feat | fix | docs | style | refactor | perf | test | build | ci | chore | revert -->

- [ ] `feat` – new feature
- [ ] `fix` – bug fix
- [ ] `docs` – documentation only
- [ ] `refactor` – code change with no feature/fix
- [ ] `test` – adding or updating tests
- [ ] `chore` – maintenance (deps, config, etc.)
- [ ] `ci` – CI/CD changes

## How to test

<!-- Steps to verify this works correctly -->

1. 
2. 

## Checklist

- [ ] Tests pass locally (`pytest tests/`)
- [ ] Code is formatted (`black .`)
- [ ] PR title follows `type: description` or `type(scope): description`
- [ ] Relevant docs / README updated (if applicable)


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
