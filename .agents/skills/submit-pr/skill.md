# Submit PR

name: submit-pr
description: Prepare and submit a pull request for the infra.aap_configuration Ansible Collection. Syncs with upstream, creates a feature branch, runs pre-commit and linting checks (ansible-lint, yamllint), updates documentation and changelogs as needed, commits with conventional commits, then creates the PR via gh against redhat-cop/infra.aap_configuration. Use when the user asks to submit, create, or open a pull request, or says "submit PR", "open PR", "create PR".

Submit PR

## Repository configuration

This skill is scoped to **infra.aap_configuration**:

| Setting | Value |
|---------|-------|
| Upstream repo | `redhat-cop/infra.aap_configuration` |
| Base branch | `devel` |
| Fork (`origin`) | Your GitHub fork of `infra.aap_configuration` |
| Upstream remote | `upstream` → `https://github.com/redhat-cop/infra.aap_configuration.git` |

Ensure remotes are configured:

```bash
git remote -v
# origin   git@github.com:YOUR_GITHUB_USER/infra.aap_configuration.git
# upstream https://github.com/redhat-cop/infra.aap_configuration.git
```

If `upstream` is missing:

```bash
git remote add upstream https://github.com/redhat-cop/infra.aap_configuration.git
```

Workflow

Step 1: Sync with upstream and create a feature branch

Always start from the latest upstream devel:

```bash
git fetch upstream
git checkout -b YOUR_BRANCH_NAME upstream/devel
```

Use a descriptive branch name (e.g., feat/add-new-module, fix/nginx-role-idempotency).

If changes already exist on the current branch (e.g., from an in-progress session), cherry-pick or rebase them onto the new branch.

Step 2: Run pre-commit and linting checks

If the repository uses pre-commit:

pre-commit run --all-files

If pre-commit is not installed, fall back to standard Ansible collection checks:

ansible-lint
yamllint .
ansible-test sanity

All checks must pass cleanly. If the branch has pre-existing violations (e.g., from an old base), rebase onto `upstream/devel` first. Manually fix any violations and re-run until clean.

Step 3: Update documentation

Check whether your changes affect areas covered by existing docs. Update any that apply:

Doc Location

When to update

README.md

High-level collection description, requirements, dependencies.

docs/

Detailed user guides, setup instructions, or architectural choices.

plugins/**/*.py

Update inline DOCUMENTATION, EXAMPLES, and RETURN blocks for modules/plugins.

roles/*/README.md

Role-specific variables, dependencies, and usage examples.

roles/*/meta/main.yml

Galaxy metadata, supported platforms, role dependencies.

Step 4: Add Changelog Fragments

Ansible collections typically use changelog fragments to generate release notes (often via antsibull-changelog). If your change is user-facing or affects behavior:

Create a new YAML file in changelogs/fragments/ (e.g., changelogs/fragments/issue-123-fix-timeout.yml).

Follow the repository's required schema (usually containing keys like minor_changes, major_changes, bugfixes, or breaking_changes).

Step 5: Commit with conventional commits

Use the Conventional Commits format:

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Common types for Ansible collections:

Type

When to use

feat

New feature (new module, role, plugin, or significant role capability).

fix

Bug fix (resolving idempotency issues, syntax errors, etc.).

docs

Documentation only (README updates, module docstring updates).

style

Formatting (yamllint fixes, trailing spaces).

refactor

Code restructuring (no feature or fix).

test

Adding or updating Molecule or ansible-test scenarios.

ci

CI/CD configuration (GitHub Actions, GitLab CI).

chore

Maintenance tasks (dependency updates, galaxy.yml bumps).

Scopes reflect collection areas: module, role, plugin, inventory, filter, docs, tests.

Examples:

feat(module): add custom_firewall_rule module

fix(role): correct default template path in webserver role

ci: update github actions to test against ansible-core 2.16

docs: add execution environment requirements to README

Step 6: Push and create the pull request

Push the branch to the fork (`origin`):

```bash
git push -u origin HEAD
```

**Always** open the PR against the upstream repository, not the fork. Resolve your GitHub username from `origin` (or `gh api user -q .login`) for the `--head` value:

```bash
FORK_OWNER="$(gh api user -q .login)"

gh pr create \
  --repo redhat-cop/infra.aap_configuration \
  --head "${FORK_OWNER}:YOUR_BRANCH_NAME" \
  --base devel \
  --title "conventional commit style title" \
  --body "$(cat <<'EOF'
## Summary

- Concise description of what changed and why

## Changes

- List of notable changes (e.g., new variables, deprecated modules)

## Test plan

- [ ] `ansible-lint` passes
- [ ] `ansible-test sanity` passes
- [ ] Molecule / Integration tests pass
- [ ] Documentation / docstrings updated
- [ ] Changelog fragment added (if applicable)
EOF
)"
```

Replace `YOUR_BRANCH_NAME` with the actual branch name. Do **not** run `gh pr create` without `--repo redhat-cop/infra.aap_configuration` — that creates a PR on the fork instead of upstream.

Return the upstream PR URL to the user (e.g. `https://github.com/redhat-cop/infra.aap_configuration/pull/NNNN`).

Maintaining the PR

When pushing additional commits to an existing PR, always update the PR body to reflect the new changes. Use `--repo redhat-cop/infra.aap_configuration` for all `gh pr` commands:

```bash
gh pr edit PR_NUMBER --repo redhat-cop/infra.aap_configuration --body "$(cat <<'EOF'
...updated body...
EOF
)"
```

The Summary, Changes, and Test plan sections must stay current with all commits on the branch, not just the initial one.
