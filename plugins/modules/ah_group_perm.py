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
module: ah_group_perm
short_description: Manage group permissions
description:
  - Add and remove permissions for a group.
version_added: '0.4.3'
author: Herve Quatremain (@herve4m)
options:
  name:
    description:
      - Name of the group.
    required: true
    type: str
  perms:
    description:
      - The list of permissions to add to or remove from the given group.
      - The module accepts the following roles.
      - For user management, C(add_user), C(change_user), C(delete_user), and C(view_user).
      - For group management, C(add_group), C(change_group), C("delete_group"), and C(view_group).
      - For collection namespace management, C(add_namespace), C(change_namespace), C(upload_to_namespace), and C(delete_namespace).
      - For collection content management, C(modify_ansible_repo_content), and C(delete_collection).
      - For remote repository configuration, C(change_collectionremote), and C(view_collectionremote).
      - For container image management, only with private automation hub v4.3.2
        or later, C(change_containernamespace_perms), C(change_container),
        C(change_image_tag), C(create_container), and C(push_container), and C(delete_containerrepository).
      - For remote registry management, C(add_containerregistryremote), C(change_containerregistryremote), and C(delete_containerregistryremote).
      - For task management, C(change_task), C(view_task), and C(delete_task).
      - You can also grant or revoke all permissions with C(*) or C(all).
    type: list
    elements: str
    required: true
  state:
    description:
      - If C(absent), then the module removes the listed permissions from the
        group. If the group has permissions that are not listed in C(perms),
        then the module does not remove those pre-existing permissions.
      - If C(present), then the module adds the listed permissions to the group. The module does not remove the permissions that the group already has.
    type: str
    default: present
    choices: [absent, present]
seealso:
  - module: redhat_cop.ah_configuration.ah_group
  - module: redhat_cop.ah_configuration.ah_user
notes:
  - Supports C(check_mode).
  - The container permissions (C(change_containernamespace_perms),
    C(change_container), C(change_image_tag), C(create_container), and
    C(push_container)) are only available with private automation hub v4.3.2 or
    later.
extends_documentation_fragment: redhat_cop.ah_configuration.auth_ui
"""


EXAMPLES = r"""
- name: Ensure the operators have the correct permissions to manage users
  redhat_cop.ah_configuration.ah_group_perm:
    name: operators
    perms:
      - add_user
      - change_user
      - delete_user
      - view_user
    state: present
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Ensure the administrators have all the permissions
  redhat_cop.ah_configuration.ah_group_perm:
    name: administrators
    perms: "*"
    state: present
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Ensure the developers cannot manage groups nor users
  redhat_cop.ah_configuration.ah_group_perm:
    name: developers
    perms:
      - add_user
      - change_user
      - delete_user
      - add_group
      - change_group
      - delete_group
    state: absent
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t
"""

RETURN = r""" # """

from ..module_utils.ah_api_module import AHAPIModule
from ..module_utils.ah_ui_object import AHUIGroup


# Mapping between the permission names that the user provides in perms and the
# private automation hub internal names.
FRIENDLY_PERM_NAMES = {
    "*": "all",
    # Namespaces
    "add_namespace": "galaxy.add_namespace",
    "change_namespace": "galaxy.change_namespace",
    "upload_to_namespace": "galaxy.upload_to_namespace",
    "delete_namespace": "galaxy.delete_namespace",
    # Collections
    "modify_ansible_repo_content": "ansible.modify_ansible_repo_content",
    "delete_collection": "ansible.delete_collection",
    # Users
    "add_user": "galaxy.add_user",
    "change_user": "galaxy.change_user",
    "delete_user": "galaxy.delete_user",
    "view_user": "galaxy.view_user",
    # Groups
    "add_group": "galaxy.add_group",
    "change_group": "galaxy.change_group",
    "delete_group": "galaxy.delete_group",
    "view_group": "galaxy.view_group",
    # Remotes (Collections)
    "change_collectionremote": "ansible.change_collectionremote",
    "view_collectionremote": "ansible.view_collectionremote",
    # Containers
    "change_containernamespace_perms": "container.change_containernamespace",
    "change_container": "container.namespace_change_containerdistribution",
    "change_image_tag": "container.namespace_modify_content_containerpushrepository",
    "create_container": "container.add_containernamespace",
    "push_container": "container.namespace_push_containerdistribution",
    "delete_containerrepository": "container.delete_containerrepository",
    # Remote Registries
    "add_containerregistryremote": "galaxy.add_containerregistryremote",
    "change_containerregistryremote": "galaxy.change_containerregistryremote",
    "delete_containerregistryremote": "galaxy.delete_containerregistryremote",
    # Tasks
    "change_task": "core.change_task",
    "delete_task": "core.delete_task",
    "view_task": "core.view_task",
}


def main():
    argument_spec = dict(
        name=dict(required=True),
        perms=dict(type="list", elements="str", required=True),
        state=dict(choices=["present", "absent"], default="present"),
    )

    # Create a module for ourselves
    module = AHAPIModule(argument_spec=argument_spec, supports_check_mode=True)

    # Extract our parameters
    name = module.params.get("name")
    perms = module.params.get("perms")
    state = module.params.get("state")

    # Authenticate
    module.authenticate()

    vers = module.get_server_version()
    if vers < "4.3.2":
        del FRIENDLY_PERM_NAMES["change_containernamespace_perms"]
        del FRIENDLY_PERM_NAMES["change_container"]
        del FRIENDLY_PERM_NAMES["change_image_tag"]
        del FRIENDLY_PERM_NAMES["create_container"]
        del FRIENDLY_PERM_NAMES["push_container"]

    # Convert the given permission list to a list of internal names
    group_perms = []
    perm_ah_names = [v for v in FRIENDLY_PERM_NAMES.values() if v != "all"]
    for perm in perms:
        if perm == "*" or perm == "all":
            group_perms = perm_ah_names
            break
        if perm in FRIENDLY_PERM_NAMES:
            group_perms.append(FRIENDLY_PERM_NAMES[perm])
        elif perm in perm_ah_names:
            group_perms.append(perm)
        else:
            module.fail_json(msg="Unknown perm ({perm}) defined".format(perm=perm))

    group = AHUIGroup(module)
    group.get_object(name)
    if not group.exists:
        module.fail_json(msg="Unknown group: {group}".format(group=name))

    # Retrieve the group permissions
    group.load_perms()

    # Removing the permissions
    if state == "absent":
        # Which permissions should be removed?
        to_delete = list(set(group_perms) & set(group.get_perms()))
        # API (DELETE): /api/galaxy/_ui/v1/groups/<GR_ID#>/model-permissions/<PERM_ID#>/
        group.delete_perms(to_delete)

    # Adding the permissions not yet associated with the group
    # API (POST): /api/galaxy/_ui/v1/groups/<GR_ID#>/model-permissions/
    to_create = list(set(group_perms) - set(group.get_perms()))
    group.create_perms(to_create)


if __name__ == "__main__":
    main()
