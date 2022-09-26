# Redhat Communties of Practice Automation Hub Configuration Collection

![Ansible Lint](https://github.com/redhat-cop/ah_configuration/workflows/Yaml%20and%20Ansible%20Lint/badge.svg)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Code style: flake8](https://img.shields.io/badge/Code%20style-flake8-orange)
<!-- Further CI badges go here as above -->

This Ansible collection allows for easy interaction with an Ansible Automation Hub or Galaxy NG server via Ansible playbooks.

## Included content

Click the `Content` button to see the list of content included in this collection.

## Installing this collection

You can install the redhat_cop ah_configuration collection with the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install redhat_cop.ah_configuration
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: redhat_cop.ah_configuration
    # If you need a specific version of the collection, you can specify like this:
    # version: ...
```

## Using this collection

Define following vars here, or in `galaxy_configs/galaxy_auth.yml`
`galaxy_server: ansible-galaxy-web-svc-test-project.example.com`

You can also specify authentication by setting the following variables:

- `galaxy_server`, `galaxy_oauthtoken`, `ah_token`

The OAuth2 token is the only method. You can obtain the token through through the web interface. If you only pass a username and password to galaxy API roles/modules a new OAUTH2 token will be generated, invalidating the previous user token. To ensure this doesn't occur always set the ah_token variable to the users OAUTH2 token before executing automation. This does not affect pulp API calls.

Galaxy API calls

- group
- namespace
- publish
- repository
- repository_sync
- user

These can be specified via (from highest to lowest precedence):

- direct role variables as mentioned above

### See Also

- [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Release and Upgrade Notes

For details on changes between versions, please see [the changelog for this collection](CHANGELOG.rst).

## Roadmap

Add more roles and modules for endpoints on the Automation Hub.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Automation Hub Configuration collection repository](https://github.com/redhat-cop/ah_configuration).
More information about contributing can be found in our [Contribution Guidelines.](https://github.com/redhat-cop/ah_configuration/blob/devel/.github/CONTRIBUTING.md)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

All content in this folder is licensed under the same license as Ansible,
which is the same as license that applied before when the base for this
code was derived form the [AWX.AWX](https://galaxy.ansible.com/awx/awx) collection.

## Documentation

Documentation for Automation hub URI can be found at
[Documentation for Automation hub URI.](https://github.com/ansible/galaxy_ng/wiki/Automating-Collection-Uploads)
