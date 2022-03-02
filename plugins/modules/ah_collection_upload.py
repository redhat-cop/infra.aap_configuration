#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2020, Tom Page <@Tompage1994>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


ANSIBLE_METADATA = {"metadata_version": "1.1", "status": ["preview"], "supported_by": "community"}


DOCUMENTATION = """
---
module: ah_collection_upload
author: "Tom Page (@Tompage1994)"
short_description: Upload a collection artifact to Automation Hub.
description:
    - Upload a collection artifact to Automation Hub. See
      U(https://www.ansible.com/) for an overview.
options:
    path:
      description:
        - Collection artifact file path.
        - Can be a URL
      required: True
      type: str
    wait:
      description:
        - Wait for the collection to be uploaded.
      default: False
      type: bool

extends_documentation_fragment: redhat_cop.ah_configuration.auth
"""


EXAMPLES = """
- name: Upload collection to automation hub
  ah_collection_upload:
    path: /var/tmp/collections/awx_awx-15.0.0.tar.gz

- name: Upload collection to automation hub from galaxy
  ah_collection_upload:
    path: https://galaxy.ansible.com/download/theforeman-foreman-3.2.0.tar.gz

"""

from ..module_utils.ah_module import AHModule


def main():
    # Any additional arguments that are not fields of the item can be added here
    argument_spec = dict(
        path=dict(required=True),
        wait=dict(type="bool", default=True),
    )

    # Create a module for ourselves
    module = AHModule(argument_spec=argument_spec)

    # Extract our parameters
    path = module.params.get("path")
    wait = module.params.get("wait")

    module.upload(path, "artifacts/collections", wait, item_type="collections")


if __name__ == "__main__":
    main()
