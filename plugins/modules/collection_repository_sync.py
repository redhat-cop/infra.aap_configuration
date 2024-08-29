#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Sean Sullivan <@sean-m-sullivan>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: collection_repository_sync
author: Sean Sullivan (@sean-m-sullivan)
short_description: Sync an Automation Hub collection repository
description:
    - Sync an Automation Hub collection repository.
options:
    name:
      description:
        - Collection repository name. Probably one of community or rh-certified.
      required: True
      type: str
    wait:
      description:
        - Wait for the collection repository to finish syncing before returning.
      required: false
      default: True
      type: bool
    interval:
      description:
        - The interval to request an update from Automation Hub.
      required: False
      default: 1
      type: float
    timeout:
      description:
        - If waiting for the repository to update this will abort after this
          amount of seconds.
      type: int
extends_documentation_fragment: galaxy.galaxy.auth_ui
"""


EXAMPLES = """
- name: Sync rh-certified repo without waiting
  collection_repository_sync:
    name: rh-certified
    wait: false

- name: Sync community repo and wait up to 60 seconds
  collection_repository_sync:
    name: community
    wait: true
    timeout: 60
"""

from ..module_utils.ah_api_module import AHAPIModule
from ..module_utils.ah_pulp_object import AHPulpAnsibleRepository


def main():
    # Any additional arguments that are not fields of the item can be added here
    argument_spec = dict(
        name=dict(required=True),
        wait=dict(default=True, type="bool"),
        interval=dict(default=1.0, type="float"),
        timeout=dict(default=None, type="int"),
    )

    # Create a module for ourselves
    module = AHAPIModule(argument_spec=argument_spec, supports_check_mode=True)

    # Extract our parameters
    name = module.params.get("name")
    wait = module.params.get("wait")
    interval = module.params.get("interval")
    timeout = module.params.get("timeout")
    check_mode = module.params.get("check_mode")

    # Get the ansible_repository
    ansible_repository = AHPulpAnsibleRepository(module)
    ansible_repository.get_object(name=name)
    if not ansible_repository.exists:
        module.fail_json(msg="The container registry with name: {name}, was not found.".format(name=name))

    if check_mode:
        module.exit_json(changed=True, msg="Would have synced collection repository: {name}".format(name=name))
    else:
        ansible_repository.sync(wait, interval, timeout)

    module.exit_json(**module.json_output)


if __name__ == "__main__":
    main()
