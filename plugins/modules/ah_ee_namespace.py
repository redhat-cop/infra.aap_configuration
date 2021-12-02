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
module: ah_ee_namespace
short_description: Manage private automation hub execution environment namespaces
description:
  - Create and delete execution environment namespaces.
  - Grant group access to namespaces.
version_added: '0.4.3'
author: Herve Quatremain (@herve4m)
options:
  name:
    description:
      - Name of the namespace to create, remove, or modify.
    required: true
    type: str
  groups:
    description:
      - List of the groups to grant or remove access to the namespace.
        When set to an empty list (C([])), the module revokes access for all groups.
    type: list
    elements: str
  append:
    description:
      - If C(yes), then grant access to the additionnal groups specified in C(groups).
      - If C(no), then the module only grants access to the groups specified in C(groups), revoking the access for all other groups.
    type: bool
    default: yes
  state:
    description:
      - If C(absent), then the module deletes the namespace.
      - The module does not fail if the namespace does not exist because the state is already as expected.
      - If C(present), then the module creates the namespace if it does not already exist.
        If the namespace already exists, then the module updates its state.
    type: str
    default: present
    choices: [absent, present]
notes:
  - Supports C(check_mode).
  - Only works with private automation hub v4.3.2 or later.
  - When the module creates a namespace, the private automation hub web UI does not display that new namespace.
    You must first create a repository in the namespace, with C(podman push) for example, for the web UI to show the namespace.
  - When the module grants access to a group, the permissions associated to that group apply.
extends_documentation_fragment: redhat_cop.ah_configuration.auth_ui
"""

EXAMPLES = r"""
- name: Ensure the namespace exists
  redhat_cop.ah_configuration.ah_ee_namespace:
    name: ansible-automation-platform-20-early-access
    state: present
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Ensure the namespace is removed
  redhat_cop.ah_configuration.ah_ee_namespace:
    name: custom-ee-01
    state: absent
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Ensure only the operators group can manage the namespace
  redhat_cop.ah_configuration.ah_ee_namespace:
    name: ansible-automation-platform-20-early-access
    state: present
    groups:
      - operators
    append: false
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Ensure the managers group can also manage the namespace
  redhat_cop.ah_configuration.ah_ee_namespace:
    name: ansible-automation-platform-20-early-access
    state: present
    groups:
      - managers
    append: true
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t
"""

RETURN = r""" # """

from ..module_utils.ah_api_module import AHAPIModule
from ..module_utils.ah_ui_object import AHUIGroup, AHUIEENamespace
from ..module_utils.ah_pulp_object import AHPulpEENamespace


# Name of the permissions
PERM_NAMES = [
    "change_containernamespace",
    "namespace_change_containerdistribution",
    "namespace_modify_content_containerpushrepository",
    "add_containernamespace",
    "namespace_push_containerdistribution",
]


def main():
    argument_spec = dict(
        name=dict(required=True),
        groups=dict(type="list", elements="str"),
        append=dict(type="bool", default=True),
        state=dict(choices=["present", "absent"], default="present"),
    )

    # Create a module for ourselves
    module = AHAPIModule(argument_spec=argument_spec, supports_check_mode=True)

    # Extract our parameters
    name = module.params.get("name")
    groups = module.params.get("groups")
    append = module.params.get("append")
    state = module.params.get("state")

    # Authenticate
    module.authenticate()

    # Only recent versions support execution environment
    vers = module.get_server_version()
    if vers < "4.3.2":
        module.fail_json(msg="This module requires private automation hub version 4.3.2 or later. Your version is {vers}".format(vers=vers))

    # Process the object from the Pulp API (delete or create)
    namespace_pulp = AHPulpEENamespace(module)

    # API (GET): /pulp/api/v3/pulp_container/namespaces/?name=<name>
    namespace_pulp.get_object(name)

    # Removing the namespace
    if state == "absent":
        namespace_pulp.delete()

    # Confirm that all the given groups exist and retrieve their details
    group = AHUIGroup(module)
    group_ids = []
    if groups is not None:
        error_groups = []
        for group_name in groups:
            group.get_object(group_name)
            if group.exists:
                group.load_perms()
                perms = []
                for p in group.get_perms():
                    if p.startswith("container."):
                        p = p[len("container.") :]
                    if p in PERM_NAMES:
                        perms.append(p)
                group.data["object_permissions"] = perms
                group_ids.append(group.data)
            else:
                error_groups.append(group_name)
        if error_groups:
            module.fail_json(msg="unknown groups: %s" % ", ".join(error_groups))

    # Creating the namespace if it does not exist
    if not namespace_pulp.exists:
        namespace_pulp.create({"name": name}, auto_exit=False)
        changed = True
    else:
        changed = False

    # Process the object from the UI API
    namespace_ui = AHUIEENamespace(module)

    # Get the namespace details from its name.
    # API (GET): /api/galaxy/_ui/v1/execution-environments/namespaces/<name>/
    namespace_ui.get_object(name)

    # Add the already assigned groups to the list of groups to update
    if append and "groups" in namespace_ui.data:
        ids = [v["id"] for v in group_ids]
        for g in namespace_ui.data["groups"]:
            if "id" in g and g["id"] not in ids:
                group_ids.append(g)

    # API (PUT): /api/galaxy/_ui/v1/execution-environments/namespaces/<name>/
    updated = namespace_ui.update_groups({"groups": group_ids}, auto_exit=False)
    if changed or updated:
        json_output = {"name": namespace_ui.name, "type": namespace_ui.object_type, "changed": True}
    else:
        json_output = {"name": namespace_ui.name, "type": namespace_ui.object_type, "changed": False}
    module.exit_json(**json_output)


if __name__ == "__main__":
    main()
