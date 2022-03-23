# Red Hat Communities of Practice Controller Configuration Collection

![Ansible Lint](https://github.com/redhat-cop/controller_configuration/workflows/Ansible%20Lint/badge.svg)
![Galaxy Release](https://github.com/redhat-cop/controller_configuration/workflows/galaxy-release/badge.svg)
<!-- Further CI badges go here as above -->

This Ansible collection allows for easy interaction with an AWX or Ansible Controller server via Ansible roles using the AWX/Controller collection modules.

## REQUIREMENTS

The AWX.AWX OR ANSIBLE.CONTROLLER collections MUST be installed in order for this collection to work. It is recommended they be invoked in the playbook in the following way.

```yaml
---
- name: Playbook to configure ansible controller post installation
  hosts: localhost
  connection: local
  vars:
    controller_validate_certs: false
  collections:
    - awx.awx
```

## Included content

Click the `Content` button to see the list of content included in this collection.

## Installing this collection

You can install the redhat_cop controller_configuration collection with the Ansible Galaxy CLI:

```console
ansible-galaxy collection install redhat_cop.controller_configuration
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: redhat_cop.controller_configuration
    # If you need a specific version of the collection, you can specify like this:
    # version: ...
```

## Conversion from tower_configuration

If you were using a version of redhat_cop.tower_configuration, please refer to our Conversion Guide here: [Conversion Guide](docs/CONVERSION_GUIDE.md)

## Using this collection

The awx.awx or ansible.controller collection must be invoked in the playbook in order for ansible to pick up the correct modules to use.

The following command will invoke the playbook with the awx collection

```console
ansible-playbook redhat_cop.controller_configuration.configure_awx.yml
```

The following command will invoke the playbook with the ansible.controller collection

```console
ansible-playbook redhat_cop.controller_configuration.configure_controller.yml
```

Otherwise it will look for the modules only in your base installation. If there are errors complaining about "couldn't resolve module/action" this is the most likely cause.

```yaml
- name: Playbook to configure ansible controller post installation
  hosts: localhost
  connection: local
  vars:
    controller_validate_certs: false
  collections:
    - awx.awx
```

Define following vars here, or in `controller_configs/controller_auth.yml`
`controller_hostname: ansible-controller-web-svc-test-project.example.com`

You can also specify authentication by a combination of either:

- `controller_hostname`, `controller_username`, `controller_password`
- `controller_hostname`, `controller_oauthtoken`

The OAuth2 token is the preferred method. You can obtain the token through the preferred `controller_token` module, or through the
AWX CLI [login](https://docs.ansible.com/automation-controller/latest/html/controllercli/authentication.html)
command.

These can be specified via (from highest to lowest precedence):

- direct role variables as mentioned above
- environment variables (most useful when running against localhost)
- a config file path specified by the `controller_config_file` parameter
- a config file at `~/.controller_cli.cfg`
- a config file at `/etc/controller/controller_cli.cfg`

Config file syntax looks like this:

```ini
[general]
host = https://localhost:8043
verify_ssl = true
oauth_token = LEdCpKVKc4znzffcpQL5vLG8oyeku6
```

Controller token module would be invoked with this code:

```yaml
    - name: Create a new token using controller username/password
      awx.awx.token:
        description: 'Creating token to test controller jobs'
        scope: "write"
        state: present
        controller_host: "{{ controller_hostname }}"
        controller_username: "{{ controller_username }}"
        controller_password: "{{ controller_password }}"

```

### Controller Export

The awx command line can export json that is compatible with this collection.
More details can be found [here](examples/configs_export_model/README.md)

### See Also

- [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Release and Upgrade Notes

For details on changes between versions, please see [the changelog for this collection](CHANGELOG.rst).

## Roadmap

Adding the ability to use direct output from the awx export command in the roles along with the current data model.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Controller Configuration collection repository](https://github.com/redhat-cop/controller_configuration).
More information about contributing can be found in our [Contribution Guidelines.](https://github.com/redhat-cop/controller_configuration/blob/devel/.github/CONTRIBUTING.md)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
