# Submit PR

name: submit-pr
description: Prepare and submit a pull request for an Ansible Collection repository. Syncs with upstream, creates a feature branch, runs pre-commit and linting checks (ansible-lint, yamllint), updates documentation and changelogs as needed, commits with conventional commits, then creates the PR via gh. Use when the user asks to submit, create, or open a pull request, or says "submit PR", "open PR", "create PR".

Submit PR

Workflow

Step 1: Sync with upstream and create a feature branch

Always start from the latest upstream main/master:

git fetch upstream
git checkout -b YOUR_BRANCH_NAME upstream/main

Use a descriptive branch name (e.g., feat/add-new-module, fix/nginx-role-idempotency).

If changes already exist on the current branch (e.g., from an in-progress session), cherry-pick or rebase them onto the new branch.

Step 2: Run pre-commit and linting checks

If the repository uses pre-commit:

pre-commit run --all-files

If pre-commit is not installed, fall back to standard Ansible collection checks:

ansible-lint
yamllint .
ansible-test sanity

All checks must pass cleanly. If the branch has pre-existing violations (e.g., from an old base), rebase onto upstream/main first. Manually fix any violations and re-run until clean.

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

git push -u origin HEAD

gh pr create --repo upstream-owner/repo --title "conventional commit style title" --body "$(cat <<'EOF'

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

The PR targets upstream's main/master branch from the fork. Return the PR URL to the user.

Maintaining the PR

When pushing additional commits to an existing PR, always update the PR body to reflect the new changes:

gh pr edit PR_NUMBER --body "$(cat <<'EOF'
...updated body...
EOF
)"

The Summary, Changes, and Test plan sections must stay current with all commits on the branch, not just the initial one.
