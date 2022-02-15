#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2020, Sean Sullivan <@sean-m-sullivan>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


ANSIBLE_METADATA = {"metadata_version": "1.1", "status": ["preview"], "supported_by": "community"}


DOCUMENTATION = """
---
module: ah_collection_manage
author: "Sean Sullivan (@sean-m-sullivan)"
short_description: update, or destroy Automation Hub Collections.
description:
    - Update, or destroy Automation Hub Collections. See
      U(https://www.ansible.com/) for an overview.
options:
    namespace:
      description:
        - Namespace name. Must be lower case containing only alphanumeric characters and underscores.
      required: True
      type: str
    name:
      description:
        - Collection name. Must be lower case containing only alphanumeric characters and underscores.
      required: True
      type: str
    version:
      description:
        - Collection Version. Must be lower case containing only alphanumeric characters and underscores.
      type: str
    state:
      description:
        - Desired state of the resource.
        - If present will return data on collection.
        - If present with version, will return data on collection version.
        - If absent without version, will delete the collection and all versions.
        - If absent with version, will delete only specified version.
      choices: ["present", "absent"]
      default: "present"
      type: str

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
        namespace=dict(required=True),
        name=dict(required=True),
        version=dict(),
        state=dict(choices=["present", "absent"], default="present"),
    )

    # Create a module for ourselves
    module = AHModule(argument_spec=argument_spec)

    # Extract our parameters
    namespace = module.params.get("namespace")
    name = module.params.get("name")
    version = module.params.get("version")
    state = module.params.get("state")

    new_fields = {}

    # Attempt to look up an existing item based on the provided data
    existing_item = module.get_endpoint("collections/{0}/".format(namespace), name_or_id=name)
    module.fail_json(msg="Unknown perm ({existing_item}) defined".format(existing_item=existing_item))

    if state == "absent":
        # If the state was absent we can let the module delete it if needed, the module will handle exiting from this
        module.delete_if_needed(existing_item)



    # If the state was present and we can let the module build or update the existing item, this will return on its own
    module.create_or_update_if_needed(
        existing_item,
        new_fields,
        endpoint="namespaces",
        item_type="namespaces",
    )


if __name__ == "__main__":
    main()
