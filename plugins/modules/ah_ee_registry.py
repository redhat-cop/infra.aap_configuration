#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Tom Page <@Tompage1994>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# You can consult the UI API documentation directly on a running private
# automation hub at https://hub.example.com/pulp/api/v3/docs/


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: ah_ee_registry
short_description: Manage private automation hub execution environment remote registries.
description:
  - Update and delete execution environment remote registries.
  - Grant group access to repositories.
version_added: '0.7.0'
author: Tom Page (@Tompage1994)
options:
  name:
    description:
      - Name of the registry to remove or modify.
    required: true
    type: str
  new_name:
    description:
      - New name for the registry. Setting this option changes the name of the registry which current name is set in C(name).
    type: str
  url:
    description:
      - The URL of the remote registry
    type: str
    required: true
  username:
    description:
      - The username to authenticate to the registry with
  password:
    description:
      - The password to authenticate to the registry with
  tls_validation:
    description:
      - Whether to validate TLS when connecting to the remote registry
  client_key:
    description:
      - A PEM encoded private key file used for authentication.
      - Mutually exclusive with C(client_key_path)
    type: str
  client_cert:
    description:
      - A PEM encoded client certificate used for authentication.
      - Mutually exclusive with C(client_cert_path)
    type: str
  ca_cert:
    description:
      - A PEM encoded CA certificate used for authentication.
      - Mutually exclusive with C(ca_cert_path)
    type: str
  client_key_path:
    description:
      - Path to a PEM encoded private key file used for authentication.
      - Mutually exclusive with C(client_key)
    type: str
  client_cert_path:
    description:
      - Path to a PEM encoded client certificate used for authentication.
      - Mutually exclusive with C(client_cert)
    type: str
  ca_cert_path:
    description:
      - Path to a PEM encoded CA certificate used for authentication.
      - Mutually exclusive with C(ca_cert)
    type: str
  proxy_url:
    description:
      - Proxy URL to use for the connection
    type: str
  proxy_username:
    description:
      - Proxy URL to use for the connection
    type: str
  proxy_password:
    description:
      - Proxy URL to use for the connection
  download_concurrency:
      description:
        - Number of concurrent collections to download.
      type: str
  rate_limit:
      description:
        - Limits total download rate in requests per second.
      type: str
  state:
    description:
      - If C(absent), then the module deletes the registry.
      - The module does not fail if the registry does not exist because the state is already as expected.
      - If C(present), then the module updates the description and README file for the registry.
    type: str
    default: present
    choices: [absent, present]
notes:
  - Supports C(check_mode).
  - Only works with private automation hub v4.4.0 or later.
extends_documentation_fragment: redhat_cop.ah_configuration.auth_ui
"""

EXAMPLES = r"""
- name: Add a remote registry to AH
  redhat_cop.ah_configuration.ah_ee_registry:
    name: my_quayio
    state: present
    url: https://quay.io/my/registry
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Add a remote registry which requires auth to AH
  redhat_cop.ah_configuration.ah_ee_registry:
    name: my_quayio_auth
    state: present
    url: https://quay.io/my/registry
    username: myuser
    password: mypassword
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Remove a remote registry from AH
  redhat_cop.ah_configuration.ah_ee_registry:
    name: examplehub
    state: absent
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t
"""

RETURN = r""" # """

from ..module_utils.ah_api_module import AHAPIModule
from ..module_utils.ah_ui_object import AHUIEERegistry


def main():
    argument_spec = dict(
        name=dict(required=True),
        new_name=dict(),
        url=dict(),
        username=dict(),
        password=dict(),
        tls_validation=dict(type="bool", default=True),
        client_key=dict(no_log="true"),
        client_cert=dict(),
        ca_cert=dict(),
        client_key_path=dict(),
        client_cert_path=dict(),
        ca_cert_path=dict(),
        proxy_url=dict(),
        proxy_username=dict(),
        proxy_password=dict(),
        download_concurrency=dict(),
        rate_limit=dict(),
        state=dict(choices=["present", "absent"], default="present"),
    )

    # Create a module for ourselves
    module = AHAPIModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        mutually_exclusive=[("client_key", "client_key_path"), ("client_cert", "client_cert_path"), ("ca_cert", "ca_cert_path")],
    )

    # Extract our parameters
    name = module.params.get("name")
    new_name = module.params.get("new_name")
    state = module.params.get("state")

    # Authenticate
    module.authenticate()
    registry = AHUIEERegistry(module)

    # Removing the registry
    if state == "absent":
        registry.get_object(name)
        registry.delete()

    # Create the data that gets sent for create and update
    new_fields = {}
    new_fields["name"] = new_name if new_name else (registry.name if (registry and registry.name) else name)
    for field_name in (
        "url",
        "username",
        "password",
        "tls_validation",
        "client_key",
        "client_cert",
        "ca_cert",
        "proxy_url",
        "proxy_username",
        "proxy_password",
        "download_concurrency",
        "rate_limit",
    ):
        field_val = module.params.get(field_name)
        if field_val is not None:
            new_fields[field_name] = field_val

    for field_name in (
        "client_key",
        "client_cert",
        "ca_cert",
    ):
        path_val = module.params.get("{}_path".format(field_name))
        if path_val is not None:
            field_val = module.getFileContent(path_val)
            new_fields[field_name] = field_val

    # API (POST): /api/galaxy/_ui/v1/registry/
    # API (PUT): /api/galaxy/_ui/v1/registry/<PK#>/
    registry.get_object(new_fields["name"])
    registry.create_or_update(new_fields)


if __name__ == "__main__":
    main()
