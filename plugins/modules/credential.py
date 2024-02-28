#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2024, Derek Waters <dwaters@redhat.com>
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
module: credential
author: "Derek Waters (@derekwaters)"
short_description: Manage a Credential in EDA Controller
description:
    - Create, update and delete credentials in EDA Controller
options:
    name:
      description:
        - The name of the credential.
      required: True
      type: str
    new_name:
      description:
        - Setting this option will change the existing name (looked up via the name field).
      type: str
    description:
      description:
        - The description of the credential.
      required: False
      type: str
    username:
      description:
        - The username used to access the project repository.
      required: True
      type: str
    secret:
      description:
        - The secret associated with the credential (either a password or access token).
      required: True
      type: str
    credential_type:
      description:
        - The type of the credential.
      choices: ["GitHub Personal Access Token", "GitLab Personal Access Token", "Container Registry"]
      default: "GitHub Personal Access Token"
      type: str
    state:
      description:
        - Desired state of the resource.
      choices: ["present", "absent"]
      default: "present"
      type: str

extends_documentation_fragment: infra.eda_configuration.auth
"""


EXAMPLES = """
- name: Create eda credential
  infra.eda_configuration.credential:
    name: my_credential
    description: my github access credential
    username: derekwaters
    secret: this_is_not_a_real_token
    credential_type: "GitHub Personal Access Token"
    state: present
    eda_host: eda.example.com
    eda_username: admin
    eda_password: Sup3r53cr3t

"""

from ..module_utils.eda_module import EDAModule


def main():
    # Any additional arguments that are not fields of the item can be added here
    argument_spec = dict(
        name=dict(required=True),
        new_name=dict(),
        description=dict(),
        username=dict(required=True),
        secret=dict(required=True, no_log=True),
        credential_type=dict(choices=["GitHub Personal Access Token",
                                      "GitLab Personal Access Token",
                                      "Container Registry"],
                             default="GitHub Personal Access Token"),
        state=dict(choices=["present", "absent"], default="present"),
    )

    # Create a module for ourselves
    module = EDAModule(argument_spec=argument_spec)

    # Extract our parameters
    name = module.params.get("name")
    new_name = module.params.get("new_name")
    state = module.params.get("state")

    new_fields = {}

    # Attempt to look up an existing item based on the provided data
    existing_item = module.get_one("credentials", name_or_id=name, key="req_url")

    if state == "absent":
        # If the state was absent we can let the module delete it if needed, the module will handle exiting from this
        module.delete_if_needed(existing_item, key="req_url")

    # Create the data that gets sent for create and update
    # Remove these two comments for final
    # Check that Links and groups works with this.
    new_fields["name"] = new_name if new_name else (module.get_item_name(existing_item) if existing_item else name)
    for field_name in (
        "description",
        "credential_type",
        "username",
        "secret",
    ):
        field_val = module.params.get(field_name)
        if field_val is not None:
            new_fields[field_name] = field_val

    # If the state was present and we can let the module build or update the existing item, this will return on its own
    module.create_or_update_if_needed(
        existing_item,
        new_fields,
        endpoint="credentials",
        item_type="credentials",
        key="req_url",
    )


if __name__ == "__main__":
    main()
