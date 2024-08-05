#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2020, Tom Page <@Tompage1994> original this was based on
# (c) 2023, Sean Sullivan <@sean-m-sullivan>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}


DOCUMENTATION = """
---
module: collection_remote
author: Tom Page (@Tompage1994)
short_description: Configure a collection remote repository.
description:
    - Configure an Automation Hub collection remote repository. See
      U(https://www.ansible.com/) for an overview.
    - Requires AAP 2.4 or Galaxy 4.7.1 or Later
options:
  name:
    description:
      - Remote Repository name. Probably one of community validated, or rh-certified.
    required: True
    type: str
  url:
    description:
      - Remote URL for the repository.
    required: True
    type: str
  auth_url:
    description:
      - Remote URL for the repository authentication if separate.
    type: str
  token:
    description:
      - Token to authenticate to the remote repository.
    type: str
  policy:
    description:
      - The policy to use when downloading content.
    choices: ["immediate", "When syncing, download all metadata and content now."]
    default: "immediate"
    type: str
  requirements:
    description:
      - Requirements to download from remote.
    type: list
    elements: str
  requirements_file:
    description:
      - A yaml requirements file to download from remote.
    type: str
  username:
    description:
      - Username to authenticate to the remote repository.
    type: str
  password:
    description:
      - Password to authenticate to the remote repository.
    type: str
  tls_validation:
    description:
      - Whether to use TLS validation against the remote repository.
    type: bool
    default: True
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
  download_concurrency:
    description:
      - Number of concurrent collections to download.
    type: int
    default: 10
  max_retries:
    description:
      - Retries to use when running sync. Default is 0 which does not limit.
    type: int
    default: 0
  rate_limit:
    description:
      - Limits total download rate in requests per second.
    type: int
    default: 8
  signed_only:
    description:
      - Whether to only download signed collections
    type: bool
    default: False
  sync_dependencies:
    description:
      - Whether to download depenencies when syncing collections.
    type: bool
    default: True
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
    type: str
  state:
    description:
      - If C(absent), then the module deletes the remote repository.
      - The module does not fail if the remote repository does not exist because the state is already as expected.
      - If C(present), then the module updates the description and README file for the remote repository.
    type: str
    default: present
    choices: [present, absent]
extends_documentation_fragment: galaxy.galaxy.auth_ui
"""


EXAMPLES = """
- name: Configure rh-certified collection_remote
  collection_remote:
    name: rh-certified
    url: https://cloud.redhat.com/api/automation-hub/
    token: aabbcc
    auth_url: https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token

- name: Configure community collection_remote
  collection_remote:
    name: community
    url: https://galaxy.ansible.com/api/
    requirements:
      - galaxy.galaxy
      - infra.controller_configuration

- name: Configure community collection_remote from a file
  collection_remote:
    name: community
    url: https://galaxy.ansible.com/api/
    requirements_file: "/tmp/requirements.yml"
"""

from ..module_utils.ah_api_module import AHAPIModule
from ..module_utils.ah_pulp_object import AHPulpAnsibleRemote


def main():
    # Any additional arguments that are not fields of the item can be added here
    argument_spec = dict(
        name=dict(required=True),
        url=dict(required=True),
        auth_url=dict(),
        token=dict(no_log=True),
        policy=dict(choices=['immediate', 'When syncing, download all metadata and content now.'], default='immediate'),
        requirements=dict(type="list", elements="str"),
        requirements_file=dict(),
        username=dict(),
        password=dict(no_log=True),
        tls_validation=dict(type="bool", default=True),
        client_key=dict(no_log=True),
        client_cert=dict(),
        ca_cert=dict(),
        client_key_path=dict(no_log=False),
        client_cert_path=dict(),
        ca_cert_path=dict(),
        download_concurrency=dict(type='int', default=10),
        max_retries=dict(type='int', default=0),
        rate_limit=dict(type='int', default=8),
        signed_only=dict(type="bool", default=False),
        sync_dependencies=dict(type="bool", default=True),
        proxy_url=dict(),
        proxy_username=dict(),
        proxy_password=dict(no_log=True),
        state=dict(choices=['present', 'absent'], default='present'),
    )

    # Create a module for ourselves
    module = AHAPIModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        mutually_exclusive=[
            ("requirements", "requirements_file"),
            ("client_key", "client_key_path"),
            ("client_cert", "client_cert_path"),
            ("ca_cert", "ca_cert_path"),
        ],
        required_if=[
            ['state', 'present', ('url', 'name')]
        ]
    )

    # Extract our parameters
    name = module.params.get("name")
    state = module.params.get("state")
    new_fields = {}

    requirements = module.params.get("requirements")
    if requirements is not None:
        if len(requirements):
            requirements_content = "\n  - ".join(requirements)
            new_fields["requirements_file"] = "---\ncollections:\n  - " + requirements_content
        else:
            new_fields["requirements_file"] = None

    requirements_file = module.params.get("requirements_file")
    if requirements_file:
        new_fields["requirements_file"] = module.getFileContent(requirements_file)

    for field_name in (
        "name",
        "url",
        "auth_url",
        "token",
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
        "max_retries",
        "rate_limit",
        "signed_only",
        "sync_dependencies",
    ):
        field_val = module.params.get(field_name)
        if field_val is not None:
            new_fields[field_name] = field_val

    if new_fields["max_retries"] == 0:
        new_fields["max_retries"] = None

    for field_name in (
        "client_key",
        "client_cert",
        "ca_cert",
    ):
        path_val = module.params.get("{0}_path".format(field_name))
        if path_val is not None:
            field_val = module.getFileContent(path_val)
            new_fields[field_name] = field_val

    remote = AHPulpAnsibleRemote(module)
    # Removing the registry
    if state == "absent":
        remote.get_object(name)
        remote.delete()

    remote.get_object(new_fields["name"])
    remote.create_or_update(new_fields)


if __name__ == "__main__":
    main()
