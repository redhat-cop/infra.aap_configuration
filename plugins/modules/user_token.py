#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2024, Derek Waters <@derekwaters>
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
module: user_token
author: "Derek Waters (@derekwaters)"
short_description: Manage the user tokens of the current user in EDA Controller
description:
    - Create, update and delete user tokens in EDA Controller
options:
    name:
      description:
        - The name of the token.
      required: True
      type: str
    new_name:
      description:
        - Setting this option will change the existing name (looked up via the name field).
      type: str
    description:
      description:
        - The description of the token.
      required: False
      type: str
    token:
      description:
        - The token data to set for the user.
      required: True
      type: str

extends_documentation_fragment: infra.eda_configuration.auth
"""


EXAMPLES = """
- name: Create eda user token
  infra.eda_configuration.user_token:
    name: my_user_token
    description: my user token for accessing AAP
    token: SOMETOKENDATA
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
        token=dict(required=True, no_log=True),
    )

    # Create a module for ourselves
    module = EDAModule(argument_spec=argument_spec)

    # Extract our parameters
    name = module.params.get("name")
    new_name = module.params.get("new_name")

    new_fields = {}

    # There is no way (that I can find) to search for an existing token
    # based on name. This module can only attempt to create new tokens
    # and fail safe if the token already exists (there is no way to patch
    # an existing token)

    # Create the data that gets sent for create and update
    # Remove these two comments for final
    # Check that Links and groups works with this.
    new_fields["name"] = new_name if new_name else name
    for field_name in (
        "description",
        "token",
    ):
        field_val = module.params.get(field_name)
        if field_val is not None:
            new_fields[field_name] = field_val

    module.create_if_needed(
        None,
        new_fields,
        endpoint="users/me/awx-tokens",
        item_type="awx-tokens",
        treat_conflict_as_unchanged=True
    )


if __name__ == "__main__":
    main()
