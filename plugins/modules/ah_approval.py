#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2020, Tom Page <@Tompage1994>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


ANSIBLE_METADATA = {"metadata_version": "1.1", "status": ["preview"], "supported_by": "community"}


DOCUMENTATION = """
---
module: ah_approval
author: "Tom Page (@Tompage1994)"
short_description: Approve a collection in Automation Hub.
description:
    - Approve a collection in Automation Hub. See
      U(https://www.ansible.com/) for an overview.
options:
    namespace:
      description:
        - The namespace the collection will reside in.
      required: True
      type: str
    name:
      description:
        - The name of the collection.
      required: True
      type: str
    version:
      description:
        - The version of the collection.
      required: True
      type: str

extends_documentation_fragment: redhat_cop.ah_configuration.auth
"""


EXAMPLES = """
- name: Approve redhat_cop.ah_configuration:v1.0.0
  ah_approval:
    namespace: redhat_cop
    name: ah_configuration
    version: v1.0.0

"""

from ..module_utils.ah_module import AHModule


def main():
    # Any additional arguments that are not fields of the item can be added here
    argument_spec = dict(
        namespace=dict(required=True),
        name=dict(required=True),
        version=dict(required=True),
    )

    # Create a module for ourselves
    module = AHModule(argument_spec=argument_spec)

    # Extract our parameters
    namespace = module.params.get("namespace")
    name = module.params.get("name")
    version = module.params.get("version")

    endpoint = "collections/{0}/{1}/versions/{2}".format(namespace, name, version)

    # Attempt to look up an existing item based on the provided data
    existing_item = module.get_endpoint(endpoint, **{"return_none_on_404": True})

    # If the item exists then it doesn't need to be approved so we can say changed=False
    if existing_item:
        module.exit_json(**{"changed": False})

    module.approve(
        endpoint=endpoint,
    )


if __name__ == "__main__":
    main()
