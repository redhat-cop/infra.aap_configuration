# AGENTS.md — infra.aap_configuration

## Context

This repository is an Ansible Collection (`infra.aap_configuration`) that provides roles for managing Ansible Automation Platform 2.5+ resources as code. It targets four AAP components: Automation Controller, Event-Driven Ansible, Automation Hub, and the AAP Gateway.

## Code Review Guidelines

When reviewing pull requests to this collection, verify the following:

### Role Structure Compliance

- New roles must follow the established directory layout: `defaults/main.yml`, `tasks/main.yml`, `meta/main.yml`, `meta/argument_specs.yml`, `README.md`, and `tests/`
- `meta/main.yml` must declare dependencies on `global_vars` and `meta_dependency_check`
- `defaults/main.yml` must initialize the resource list to `[]` and include standard variables for secure logging, async retries, async delay, loop delay, enforce defaults, and `aap_configuration_async_dir`
- Role naming must use the correct component prefix: `controller_*`, `gateway_*`, `hub_*`, or `eda_*`

### Async Task Pattern

All resource roles must follow the async block pattern:

1. A block with `ansible_async_dir` and `no_log` set
2. The module task loops over the resource list with `async` and `poll: 0`
3. A "Flag for errors (check mode only)" task using `ansible.builtin.set_fact` to set `error_flag`
4. An `include_role` of `infra.aap_configuration.collect_async_status` to wait for results, passing `cas_async_delay`, `cas_async_retries`, `cas_secure_logging`, `cas_job_async_results_item`, `cas_register_subvar`, `cas_error_list_var_name`, and `cas_object_label`
5. An `always` block that cleans up async result files via `ansible.builtin.async_status` with `mode: cleanup`

### Variable Naming

- Internal loop variables use double-underscore prefix: `__<role_name>_item`
- Async result variables follow: `__<role_name>_job_async` and `__<role_name>_job_async_results_item`
- Variable names must match pattern `^[a-z_][a-z0-9_]*$`
- Loop variable prefix must match `^(__|{role}_)`

### Task Naming

- Task names must follow the `"{stem} | "` prefix pattern enforced by ansible-lint
- Example: `"Managing Organizations"` for an organizations role task

### Authentication Parameters

- Controller roles (`controller_*`) must use: `controller_host`, `controller_username`, `controller_password`, `controller_oauthtoken`, `request_timeout`, `validate_certs`
- Gateway roles (`gateway_*`) must use: `gateway_hostname`, `gateway_username`, `gateway_password`, `gateway_token`, `gateway_request_timeout`, `gateway_validate_certs`
- All auth params should use `aap_hostname`, `aap_username`, `aap_password`, `aap_token` variables with `default(omit, true)` fallbacks

### Dispatch Integration

- New roles must be added to the appropriate dispatcher list in `roles/dispatch/defaults/main.yml`
- The entry must specify `role`, `var`, and `tags` at minimum

### Documentation

- `README.md` must include: description, variable tables (with defaults, required flag, description, example), data structure documentation with both JSON and YAML examples, and a license link
- `meta/argument_specs.yml` must fully describe all role options with types and defaults

### Changelog

- Every feature or bugfix PR must include a changelog fragment in `changelogs/fragments/`
- Fragment file must be valid YAML with `...` document end marker
- Use appropriate category: `minor_changes`, `major_changes`, `bugfixes`, `breaking_changes`, etc.

### Testing

- New roles should include test data in `roles/<role>/tests/configs/` and a `test.yml` playbook
- For controller roles, add corresponding test data to `tests/configs/controller/` and include the role in `tests/configure_controller.yml`

### Linting Standards

- YAML files must use `.yml` extension
- YAML files must end with `...` (document-end marker)
- 2-space indentation, no trailing whitespace
- Jinja2 variables must have spaces: `{{ var }}` not `{{var}}`
- ansible-lint profile: `production`
- Python code: `black` formatting (line length 160), `flake8` compliance

## PR Submission

When submitting PRs:

1. Run `pre-commit run --all -c .pre-commit-config.yaml` before pushing
2. Include a changelog fragment in `changelogs/fragments/`
3. Fill out the PR template completely (what, how to test, related issue)
4. Ensure all CI checks pass (pre-commit workflow)

## Issue Triage

- Bug reports should reference the specific role and AAP version
- Feature requests for new roles should specify the target AAP module (`ansible.controller.*`, `ansible.platform.*`, `ansible.hub.*`, or `ansible.eda.*`)
- Issues inactive for extended periods are automatically labeled and eventually closed by GitHub Actions
