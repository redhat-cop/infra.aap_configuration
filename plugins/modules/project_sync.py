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
module: project_sync
author: "Tom Page (@Tompage1994)"
short_description: Sync a project in EDA Controller
description:
    - Sync projects in EDA Controller
options:
    name:
      description:
        - The name of the project.
      required: True
      type: str
    wait:
      description:
        - Wait for the project to finish syncing before returning.
      required: false
      default: True
      type: bool
    interval:
      description:
        - The interval to request an update from EDA Controller.
      required: False
      default: 1
      type: float
    timeout:
      description:
        - If waiting for the project to update this will abort after this
          amount of seconds
      type: int

extends_documentation_fragment: infra.eda_configuration.auth
"""


EXAMPLES = """
- name: Create eda project
  infra.eda_configuration.project:
    name: my_project
    wait: true
    interval: 5
    timeout: 60
    eda_host: eda.example.com
    eda_username: admin
    eda_password: Sup3r53cr3t

"""

from ..module_utils.eda_module import EDAModule


def main():
    # Any additional arguments that are not fields of the item can be added here
    argument_spec = dict(
        name=dict(required=True),
        wait=dict(default=True, type="bool"),
        interval=dict(default=1.0, type="float"),
        timeout=dict(default=None, type="int"),
    )

    # Create a module for ourselves
    module = EDAModule(argument_spec=argument_spec)

    # Extract our parameters
    name = module.params.get("name")
    wait = module.params.get("wait")
    interval = module.params.get("interval")
    timeout = module.params.get("timeout")

    # Attempt to look up an existing item based on the provided data
    project = module.get_one("projects", name_or_id=name, key="req_url", allow_none=False)

    module.sync_project(project["id"], wait, interval, timeout)


if __name__ == "__main__":
    main()
