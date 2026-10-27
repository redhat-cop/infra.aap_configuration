
# Contributor's Guidelines

- All YAML files named with '.yml' extension
- Use spaces around jinja variables. {{ var }} over {{var}}
- Variables that are internal to the role should be lowercase
- Keep roles self contained - Roles should avoid including tasks from other roles when possible
- Plays should do nothing more than include a list of roles except where pre_tasks and post_tasks are required when possible
- Separators - Use underscores (e.g. my_role my_playbook) not dashes (my-role)
- Paths - When defining paths, do not include trailing slashes (e.g. my_path: /foo not my_path: /foo/). When concatenating paths, follow the same convention (e.g. {{ my_path }}/bar not {{ my_path }}bar)
- Indentation - Use 2 spaces for each indent
- `vars/` vs `defaults/` - if you have variables that don't need to change or be overridden by user, put those in `vars/` and those that a user would likely override, put those under `defaults/` directory.
- All playbooks/roles should be focused on compatibility with Automation Controller
- YAML files must end with the document-end marker `...`

## Async + check mode

Resource-managing roles that fire modules with `async` / `poll: 0` must support Ansible check mode using this pattern:

1. Set `async: "{{ ansible_check_mode | ternary(0, <timeout>) }}"` so check mode runs the module synchronously (`async: 0`) while normal runs keep fire-and-forget async. Use `1000` for gateway/eda/controller roles, or the role's `*_async_timeout` variable for hub roles.
2. Set `changed_when: (__<register>.changed if ansible_check_mode else false)` so check mode reports the module's real change status, and normal mode defers change reporting to `collect_async_status`.
3. Immediately after the module task, flag failures for dispatch:

   ```yaml
   - name: Flag for errors (check mode only)
     ansible.builtin.set_fact:
       error_flag: true
     when: ansible_check_mode and __<register>.failed is defined and __<register>.failed
   ```

4. Gate `collect_async_status` and async cleanup with `when: not ansible_check_mode` (and `ansible_job_id is defined`).
5. Rely on `dispatch` to fail at the end when `error_flag` is set in check mode.

Do not use bare `async: 1000` (or an unbounded timeout variable) with wait/cleanup skipped in check mode; that orphans async jobs and hides module check-mode results.
