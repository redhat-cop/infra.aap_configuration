#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Herve Quatremain <hquatrem@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# You can consult the UI API documentation directly on a running private
# automation hub at https://hub.example.com/pulp/api/v3/docs/


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: ah_group
short_description: Manage private automation hub user groups
description:
  - Create and delete groups in private automation hub.
version_added: '0.4.3'
author: Herve Quatremain (@herve4m)
options:
  name:
    description:
      - Name of the group to create or delete.
    required: true
    type: str
  state:
    description:
      - If C(absent), then the module deletes the group.
      - The module does not fail if the group does not exist because the state is already as expected.
      - If C(present), then the module creates the group if it does not already exist.
    type: str
    default: present
    choices: [absent, present]
seealso:
  - module: ansible.automation_hub.ah_group_perm
  - module: ansible.automation_hub.ah_user
notes:
  - Supports C(check_mode).
extends_documentation_fragment: ansible.automation_hub.auth_ui
"""

EXAMPLES = r"""
- name: Ensure the group exists
  ansible.automation_hub.ah_group:
    name: administrators
    state: present
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Ensure the group is removed
  ansible.automation_hub.ah_group:
    name: operators
    state: absent
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t
"""

RETURN = r""" # """

from ..module_utils.ah_api_module import AHAPIModule
from ..module_utils.ah_ui_object import AHUIGroup
from ..module_utils.ah_pulp_object import AHPulpGroups


def main():
    argument_spec = dict(
        name=dict(required=True),
        state=dict(choices=["present", "absent"], default="present"),
    )

    # Create a module for ourselves
    module = AHAPIModule(argument_spec=argument_spec, supports_check_mode=True)

    # Extract our parameters
    name = module.params.get("name")
    state = module.params.get("state")
    # Authenticate
    module.authenticate()
    vers = module.get_server_version()

    # Use Pulp with newer versions
    if vers > "4.7.0":
        group = AHPulpGroups(module)
        group.get_object(name)
    else:
        group = AHUIGroup(module)
        group.get_object(name, vers)
    # Removing the group
    if state == "absent":
        group.delete()

    # Creating the group.
    group.create_or_update({"name": name})


if __name__ == "__main__":
    main()
