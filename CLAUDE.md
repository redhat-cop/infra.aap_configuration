# CLAUDE.md — infra.aap_configuration

## Project Overview

This is the `infra.aap_configuration` Ansible Collection, maintained by the Red Hat Communities of Practice. It provides Ansible roles for managing Ansible Automation Platform (AAP) 2.5+ resources as code, including Automation Controller, Event-Driven Ansible (EDA), Automation Hub, and the AAP Gateway.

- **Collection FQCN:** `infra.aap_configuration`
- **Upstream repo:** `redhat-cop/infra.aap_configuration`
- **License:** GPL-3.0-or-later
- **Minimum Ansible version:** 2.16.0

## Repository Structure

```text
├── galaxy.yml                  # Collection metadata, version, dependencies
├── roles/                      # ~80 Ansible roles (the core of this collection)
│   ├── dispatch/               # Meta-role that orchestrates all other roles in order
│   ├── global_vars/            # Shared variables (operation_translate, etc.)
│   ├── collect_async_status/   # Helper role for async task result collection
│   ├── meta_dependency_check/  # Dependency validation helper
│   ├── controller_*/           # Automation Controller resource roles
│   ├── gateway_*/              # AAP Gateway resource roles
│   ├── hub_*/                  # Automation Hub resource roles
│   └── eda_*/                  # Event-Driven Ansible resource roles
├── playbooks/                  # Collection playbooks (configure_aap.yml, etc.)
├── tests/                      # Integration test playbooks and config data
│   ├── configs/                # Test variable files organized by component
│   ├── configure_controller.yml
│   └── configure_platform.yml
├── changelogs/                 # antsibull-changelog managed (fragments/ dir)
├── docs/                       # STANDARDS.md, GETTING_STARTED.md, CONVERSION_GUIDE.md
├── meta/runtime.yml            # Collection runtime metadata
└── .github/                    # CI, templates, contributing guide
```

## Key Dependencies

Declared in `galaxy.yml`:

- `ansible.platform` >= 2.5.0
- `ansible.hub` >= 1.0.0
- `ansible.controller` >= 4.6.0
- `ansible.eda` >= 2.5.0

## Architecture & Patterns

### Role Structure

Every resource role follows a consistent pattern:

- `defaults/main.yml` — Default variables (empty list for the resource, async/logging/delay settings)
- `tasks/main.yml` — Async block pattern: create resources → collect async status → cleanup
- `meta/main.yml` — Galaxy metadata, depends on `global_vars` and `meta_dependency_check`
- `meta/argument_specs.yml` — Ansible role argument specifications
- `README.md` — Role-specific documentation with variable tables and examples
- `tests/` — Per-role test playbook and config data

### Async Task Pattern

All resource-managing roles use the same async pattern:

1. Loop over the resource list with `async` and `poll: 0`
2. Register the async job results
3. Include `collect_async_status` role to wait and gather results
4. Always block cleans up async result files
5. Check mode is handled with `ansible_check_mode | ternary(0, 1000)` for async value

### The Dispatch Role

The `dispatch` role is the primary entry point. It includes all other roles in dependency order via `aap_configuration_dispatcher_roles`, which combines:

- `gateway_configuration_dispatcher_roles`
- `hub_configuration_dispatcher_roles`
- `controller_configuration_dispatcher_roles`
- `eda_configuration_dispatcher_roles`

Users can exclude roles via `aap_configuration_dispatcher_exclude_roles`.

### Variable Naming Conventions

- Resource lists use component-prefixed names: `controller_*`, `gateway_*`, `hub_*`, `eda_*`
- Some gateway-managed resources use `aap_` prefix (e.g., `aap_organizations`, `aap_teams`, `aap_user_accounts`)
- Global settings use `aap_configuration_*` prefix
- Role-specific overrides use `<role_name>_*` prefix (e.g., `controller_configuration_organizations_async_delay`)
- Authentication: `aap_hostname`, `aap_username`, `aap_password`, `aap_token`, `aap_validate_certs`
- Internal loop variables are double-underscore prefixed: `__controller_organizations_item`

### State Management

- `platform_state` sets the default state for all objects (default: `present`)
- Individual items can override with a `state` field
- `operation_translate` dict in `global_vars` maps states to verb/action labels

### Error Handling

- `aap_configuration_collect_logs: true` enables collecting all async failures instead of failing fast
- Errors accumulate in `aap_configuration_role_errors` dict keyed by resource type
- The `dispatch` role displays collected errors and fails at the end

## Coding Standards

From `docs/STANDARDS.md` and linter configs:

- All YAML files use `.yml` extension (not `.yaml`)
- YAML files must end with `...` (document-end marker)
- Use 2-space indentation
- Use spaces around Jinja variables: `{{ var }}` not `{{var}}`
- Use underscores for separators: `my_role` not `my-role`
- No trailing slashes in paths
- Internal role variables must be lowercase
- Roles should be self-contained
- Variable naming pattern: `^[a-z_][a-z0-9_]*$`
- Loop variable prefix pattern: `^(__|{role}_)`
- Task name prefix pattern: `"{stem} | "`
- `ansible-lint` profile: `production`
- Python: `black` (line length 160), `flake8` (line length 160)
- Markdown: `markdownlint-cli2` with ATX headings, fenced code blocks

## Linting & Pre-commit

Pre-commit hooks (`.pre-commit-config.yaml`):

1. `end-of-file-fixer` and `trailing-whitespace`
2. `ansible-lint` with `--profile=production`
3. `markdownlint-cli2`
4. `black` (Python formatting check)
5. `flake8` (Python linting)
6. `changelog` and `galaxy-importer` (custom hooks)

Run locally:

```bash
pip install pre-commit
pre-commit install --install-hooks -c .pre-commit-config.yaml
pre-commit run --all -c .pre-commit-config.yaml
```

## Changelogs

Uses `antsibull-changelog` with fragments in `changelogs/fragments/`. Fragment categories:

- `major_changes`, `minor_changes`, `breaking_changes`, `deprecated_features`
- `removed_features`, `security_fixes`, `bugfixes`, `known_issues`

Every PR that adds features or fixes bugs must include a changelog fragment.

## Testing

- Tests live in `tests/` with config data in `tests/configs/{controller,gateway,hub,eda}/`
- Each role also has its own `tests/` subdirectory with a standalone test playbook
- Integration tests run against a live AAP instance
- `tests/configure_controller.yml` is the main controller integration test playbook

## CI/CD

GitHub Actions workflows in `.github/workflows/`:

- `pre-commit.yml` — Runs pre-commit hooks on PRs
- `release_auto.yml` — Automated release pipeline
- `office-hours-issue.yml` — Community meeting issue automation
- Issue management workflows (inactive issue detection, labeling, closing)

## Common Tasks When Contributing

### Adding a New Role

1. Create role directory under `roles/` following the naming convention (`controller_*`, `gateway_*`, `hub_*`, or `eda_*`)
2. Include standard files: `defaults/main.yml`, `tasks/main.yml`, `meta/main.yml`, `meta/argument_specs.yml`, `README.md`, `tests/`
3. Follow the async task pattern from existing roles
4. Add `global_vars` and `meta_dependency_check` as role dependencies in `meta/main.yml`
5. Add the role to the appropriate dispatcher list in `roles/dispatch/defaults/main.yml`
6. Add test data in `tests/configs/` and a role entry in the appropriate test playbook
7. Add a changelog fragment in `changelogs/fragments/`

### Modifying an Existing Role

1. Update `tasks/main.yml` for behavior changes
2. Update `defaults/main.yml` for new/changed variables
3. Update `meta/argument_specs.yml` to match
4. Update `README.md` variable tables and examples
5. Add a changelog fragment
6. Update test data if needed

## Important Notes

- The `ansible.controller` collection uses `controller_*` parameter names for auth (`controller_host`, `controller_username`, etc.), while `ansible.platform` uses `gateway_*` names
- Gateway roles (`gateway_*`) manage platform-level resources that span controller/hub/eda
- Organizations and teams are managed via `gateway_organizations`/`gateway_teams` roles even when dispatched from the controller dispatcher list
- The `ansible-lint` config runs in offline mode (`offline: true`)
