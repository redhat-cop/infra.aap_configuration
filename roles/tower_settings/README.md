tower_configuration.tower_settings
==================

Role to apply/modify tower settings.

Requirements
------------

This role uses awx.awx collection is required.

Example Playbook
----------------

```yaml
---
- name: Test playbook for local testing
  hosts: localhost
  connection: local
  vars:
    tower_hostname: "https://tower.example.com"
    validate_certs: false
    tower_username: "admin"
    tower_password: "test-branch"
    tower_settings:
      - name: TOWER_URL_BASE
        value: "https://localhost"
      - name: AWX_TASK_ENV
        value: {'GIT_SSL_NO_VERIFY': 'false'}
      - name: AUTH_LDAP_SERVER_URI
        value: "ldap://ldap.example.com"
  roles:
    - tower_settings
```


Author Information
------------------

[Kedar Kulkarni](https://github.com/kedark3)
