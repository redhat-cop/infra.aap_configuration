#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2020, Sean Sullivan <@sean-m-sullivan>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


ANSIBLE_METADATA = {"metadata_version": "1.1", "status": ["preview"], "supported_by": "community"}


DOCUMENTATION = """
---
module: ah_namespace
author: "Sean Sullivan (@sean-m-sullivan)"
short_description: create, update, or destroy Automation Hub Namespace.
description:
    - Create, update, or destroy Automation Hub Namespace. See
      U(https://www.ansible.com/) for an overview.
options:
    name:
      description:
        - Namespace name. Must be lower case containing only alphanumeric characters and underscores.
      required: True
      type: str
    new_name:
      description:
        - Setting this option will change the existing name (looked up via the name field.
      type: str
    description:
      description:
        - Description to use for the Namespace.
      type: str
    company:
      description:
        - Namespace owner company name.
      type: str
    email:
      description:
        - Namespace contact email.
      type: str
    avatar_url:
      description:
        - Namespace logo URL.
      type: str
    resources:
      description:
        - Namespace resource page in Markdown format.
      type: str
    state:
      description:
        - Desired state of the resource.
      choices: ["present", "absent"]
      default: "present"
      type: str
    links:
      description:
        - A list of dictionaries of Name and url values for links related the Namespace.
      type: list
      elements: dict
      suboptions:
        name:
          description:
            - Link Text.
          type: str
          required: True
        url:
          description:
            - Link URL.
          type: str
          required: True
    groups:
      description:
        - A list of dictionaries of the Names and object_permissions values for groups that control the Namespace.
      type: list
      elements: dict
      default: []
      suboptions:
        name:
          description:
            - Group Name or ID.
          type: str
          required: True
        object_permissions:
          description:
            - List of Permisions granted to the group.
          choices: ["change_namespace", "upload_to_namespace"]
          type: list
          required: True

extends_documentation_fragment: redhat_cop.ah_configuration.auth
"""


EXAMPLES = """
- name: Create Tower Ping job template
  ah_namespace:
    name: Redhat
    company: Redhat
    email: user@example.com
    avatar_url: https://pnt.redhat.com/pnt/d-11633955/LogoRedHatHatColorRGB.png
    description: This is the Redhat Namespace
    links:
      - name: "homepage"
        url: "http://www.redhat.com"
    groups:
      - name: system:partner-engineers
        object_permissions:
          - "change_namespace"
          - "upload_to_namespace"

"""

from ..module_utils.ah_module import AHModule


def main():
    # Any additional arguments that are not fields of the item can be added here
    argument_spec = dict(
        name=dict(required=True),
        new_name=dict(),
        description=dict(),
        company=dict(),
        email=dict(),
        avatar_url=dict(),
        resources=dict(),
        links=dict(type="list", elements="dict"),
        groups=dict(type="list", elements="dict", default=[]),
        state=dict(choices=["present", "absent"], default="present"),
    )

    # Create a module for ourselves
    module = AHModule(argument_spec=argument_spec)

    # Extract our parameters
    name = module.params.get("name")
    new_name = module.params.get("new_name")
    state = module.params.get("state")

    new_fields = {}

    # Attempt to look up an existing item based on the provided data
    existing_item = module.get_one("namespaces", name_or_id=name)

    if state == "absent":
        # If the state was absent we can let the module delete it if needed, the module will handle exiting from this
        module.delete_if_needed(existing_item)

    # Create the data that gets sent for create and update
    # Remove these two comments for final
    # Check that Links and groups works with this.
    new_fields["name"] = new_name if new_name else (module.get_item_name(existing_item) if existing_item else name)
    for field_name in (
        "description",
        "company",
        "email",
        "avatar_url",
        "resources",
        "links",
        "groups",
    ):
        field_val = module.params.get(field_name)
        if field_val is not None:
            new_fields[field_name] = field_val

    # If the state was present and we can let the module build or update the existing item, this will return on its own
    module.create_or_update_if_needed(
        existing_item,
        new_fields,
        endpoint="namespaces",
        item_type="namespaces",
    )


if __name__ == "__main__":
    main()
