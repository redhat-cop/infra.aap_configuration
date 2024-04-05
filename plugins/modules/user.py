#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2023, Tom Page <@Tompage1994>
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
module: user
author: "Tom Page (@Tompage1994)"
short_description: Manage a user in EDA Controller
description:
    - Create, update and delete users in EDA Controller
options:
    username:
      description:
        - Name of the user to create, remove, or modify.
      required: true
      type: str
    new_username:
      description:
        - Setting this option will change the existing username (looked up via the name field).
      type: str
    first_name:
      description:
        - User's first name.
      type: str
    last_name:
      description:
        - User's last name.
      type: str
    email:
      description:
        - User's email address. That address must be correctly formed.
      type: str
    password:
      description:
        - User's password as a clear string.
      type: str
    update_secrets:
      description:
        - C(true) will always change password if user specifies password.
        - C(false) will only set the password if other values change too.
      type: bool
      default: true
    roles:
      description:
        - The roles the user is provided with.
        - Current values are C(Viewer), C(Auditor), C(Editor), C(Contributor), C(Operator), C(Admin)
      type: list
      elements: str
    state:
      description:
        - Desired state of the resource.
      choices: ["present", "absent"]
      default: "present"
      type: str

extends_documentation_fragment: infra.eda_configuration.auth
"""


EXAMPLES = """
- name: Create eda user
  infra.eda_configuration.user:
    username: john_smith
    first_name: john
    last_name: smith
    email: jsmith@example.com
    password: my_p455word
    roles:
      - Viewer
      - Auditor
      - Contributor
    state: present
    eda_host: eda.example.com
    eda_username: admin
    eda_password: Sup3r53cr3t

"""

from ..module_utils.eda_module import EDAModule


def main():
    # Any additional arguments that are not fields of the item can be added here
    argument_spec = dict(
        username=dict(required=True),
        new_username=dict(),
        first_name=dict(),
        last_name=dict(),
        email=dict(),
        password=dict(no_log=True),
        update_secrets=dict(type='bool', default=True, no_log=False),
        roles=dict(type="list", elements="str"),
        state=dict(choices=["present", "absent"], default="present"),
    )

    # Create a module for ourselves
    module = EDAModule(argument_spec=argument_spec)

    # Extract our parameters
    username = module.params.get("username")
    new_username = module.params.get("new_username")
    state = module.params.get("state")

    new_fields = {}

    # Attempt to look up an existing item based on the provided data
    existing_item = module.get_one("users", name_or_id=username, key="req_url")

    if state == "absent":
        # If the state was absent we can let the module delete it if needed, the module will handle exiting from this
        module.delete_if_needed(existing_item, key="req_url")

    # Create the data that gets sent for create and update
    # Remove these two comments for final
    # Check that Links and groups works with this.
    new_fields["username"] = new_username if new_username else (existing_item["username"] if existing_item else username)
    for field_name in (
        "first_name",
        "last_name",
        "email",
        "password",
    ):
        field_val = module.params.get(field_name)
        if field_val is not None:
            new_fields[field_name] = field_val

    if module.params.get("roles") is not None:
        roles = module.params.get("roles")
        new_fields["roles"] = list(map(lambda role: module.resolve_name_to_id("roles", role), roles))

    # If the state was present and we can let the module build or update the existing item, this will return on its own
    module.create_or_update_if_needed(
        existing_item,
        new_fields,
        endpoint="users",
        item_type="users",
        key="req_url",
    )


if __name__ == "__main__":
    main()
