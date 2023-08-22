#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2023, Chris Renwick <@crenwick93>
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
module: project
author: "Chris Renwick (@crenwick93)"
short_description: Manage a project in EDA Controller
description:
    - Create, update and delete projects in EDA Controller
options:
    name:
      description:
        - The name of the project.
      required: True
      type: str
    new_name:
      description:
        - Setting this option will change the existing name (looked up via the name field).
      type: str
    description:
      description:
        - The description of the project.
      required: False
      type: str
    url:
      description:
        - A URL to a remote archive, such as a Github Release or a build artifact stored in Artifactory and unpacks it into the project path for use.
      required: True
      type: str
      aliases: ['scm_url']
    credential:
      description:
        - The token needed to utilize the SCM URL.
      required: False
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
- name: Create eda project
  infra.eda_configuration.project:
    name: my_project
    description: my awesome project
    url: https://github.com/ansible/ansible-rulebook.git
    credential: test_token
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
        url=dict(required=True, aliases=["scm_url"]),
        credential=dict(),
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
    existing_item = module.get_one("projects", name_or_id=name, key="req_url")

    if state == "absent":
        # If the state was absent we can let the module delete it if needed, the module will handle exiting from this
        module.delete_if_needed(existing_item, key="req_url")

    # Create the data that gets sent for create and update
    # Remove these two comments for final
    # Check that Links and groups works with this.
    new_fields["name"] = new_name if new_name else (module.get_item_name(existing_item) if existing_item else name)
    for field_name in (
        "description",
        "url",
    ):
        field_val = module.params.get(field_name)
        if field_val is not None:
            new_fields[field_name] = field_val

    if module.params.get("credential") is not None:
        new_fields["credential_id"] = module.resolve_name_to_id("credentials", module.params.get("credential"))

    # If the state was present and we can let the module build or update the existing item, this will return on its own
    module.create_or_update_if_needed(
        existing_item,
        new_fields,
        endpoint="projects",
        item_type="projects",
        key="req_url",
    )


if __name__ == "__main__":
    main()
