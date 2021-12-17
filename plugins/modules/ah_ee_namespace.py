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
  - Create, rename, and delete execution environment namespaces.
  - Grant group access to namespaces.
version_added: '0.4.3'
author: Herve Quatremain (@herve4m)
options:
  name:
    description:
      - Name of the namespace to create, remove, or modify.
    required: true
    type: str
  new_name:
    description:
      - New name for the namespace. Setting this option changes the name of the namespace which current name is provided in C(name).
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

- name: Ensure the namespace has a new name
  redhat_cop.ah_configuration.ah_ee_namespace:
    name: ansible-automation-platform-20-early-access
    new_name: custom-ee-01
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

from ..module_utils.ah_api_module import AHAPIModule, AHAPIModuleError
from ..module_utils.ah_ui_object import AHUIGroup, AHUIEENamespace
from ..module_utils.ah_pulp_object import AHPulpEENamespace, AHPulpEERepository


# Name of the permissions
PERM_NAMES = [
    "change_containernamespace",
    "namespace_change_containerdistribution",
    "namespace_modify_content_containerpushrepository",
    "add_containernamespace",
    "namespace_push_containerdistribution",
]


def rename_namespace(module, src_namespace_pulp, dest_namespace_pulp, dest_namespace_name):
    """Rename the given namespace.

    The Pulp API does not provide a method to rename namespaces. That function
    provides that functionnality.
    It creates the destination namespace, copies over the access rights from the
    source namespace, renames all the repositories that references the source
    namespace, and then delete the source namespace.

    :param module: The API object that the function uses to access the API.
    :type module: :py:class:``ah_api_module.AHAPIModule``
    :param src_namespace_pulp: The Pulp object that represents the source
                               namespace to rename.
    :type src_namespace_pulp: :py:class:``ah_pulp_object.AHPulpEENamespace``
    :param dest_namespace_pulp: The Pulp object that represents the destination
                                namespace. The function creates that namespace.
    :type dest_namespace_pulp: :py:class:``ah_pulp_object.AHPulpEENamespace``
    :param dest_namespace_name: Name of the destination namespace.
    :type dest_namespace_name: str
    """
    # Get the source namespace details (groups) that are needed to create
    # a similar destination namespace.
    src_namespace_ui = AHUIEENamespace(module)
    src_namespace_ui.get_object(src_namespace_pulp.name)

    # Create the destination namespace (Pulp)
    dest_namespace_pulp.create({"name": dest_namespace_name}, auto_exit=False)

    # Duplicate the group details
    if "groups" in src_namespace_ui.data and len(src_namespace_ui.data["groups"]):
        dest_namespace_ui = AHUIEENamespace(module)
        try:
            dest_namespace_ui.get_object(dest_namespace_name, exit_on_error=False)
            dest_namespace_ui.update_groups({"groups": src_namespace_ui.data["groups"]}, auto_exit=False, exit_on_error=False)
        except AHAPIModuleError as e:
            # Roll back
            try:
                dest_namespace_pulp.delete(exit_on_error=False)
            except AHAPIModuleError:
                pass
            module.fail_json(msg=str(e))

    # Get all the repositories in the source namespace
    try:
        repos = AHPulpEERepository.get_repositories_in_namespace(module, src_namespace_pulp.name, exit_on_error=False)
    except AHAPIModuleError as e:
        # Roll back
        try:
            dest_namespace_pulp.delete(exit_on_error=False)
        except AHAPIModuleError:
            pass
        module.fail_json(msg=str(e))

    # Replace the namespace part of the repository names by the name of the
    # destination namespace
    for repo in repos:
        new_name = repo.name.replace(src_namespace_pulp.name, dest_namespace_name, 1)
        repo.update({"name": new_name, "base_path": new_name}, auto_exit=False)

    # Delete the source namespace
    src_namespace_pulp.delete(auto_exit=False)


def main():
    argument_spec = dict(
        name=dict(required=True),
        new_name=dict(),
        groups=dict(type="list", elements="str"),
        append=dict(type="bool", default=True),
        state=dict(choices=["present", "absent"], default="present"),
    )

    # Create a module for ourselves
    module = AHAPIModule(argument_spec=argument_spec, supports_check_mode=True)

    # Extract our parameters
    name = module.params.get("name")
    new_name = module.params.get("new_name")
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

    # The API does not provide a method to rename a namespace. The module
    # performs that operation by creating a namespace with the new name and then
    # copying over all the source namespace details. Finally, the original
    # namespace is deleted.
    #
    # Matrix that defines the operation to perform depending on the provided
    # parameters and the current state.
    # +-----------------------------+---+---+---+---+---+---+
    # |                        Case | 1 | 2 | 3 | 4 | 5 | 6 |
    # +-----------------------------+---+---+---+---+---+---+
    # |         `new_name` provided | N | N | Y | Y | Y | Y |
    # |     `name` namespace exists | N | Y | N | N | Y | Y |
    # | `new_name` namespace exists |   |   | N | Y | N | Y |
    # +-----------------------------+---+---+---+---+---+---+
    #
    # 1. Create the namespace which name is given in `name`.
    # 2. Do not create any namespace.
    # 3. Create the new namespace and use it for the remaining of the Ansible module.
    # 4. Use the new namespace name for the remaining of the module.
    # 5. Rename the namespace and then use it for the remaining of the module.
    # 6. Error. Cannot rename to an existing destination.
    changed = False
    if new_name:
        new_namespace_pulp = AHPulpEENamespace(module)
        new_namespace_pulp.get_object(new_name)

        if namespace_pulp.exists:
            if new_namespace_pulp.exists:
                # Case 6
                module.fail_json(msg="The namespace {namespace} (`new_name') already exists".format(namespace=new_name))
            else:
                # Case 5
                rename_namespace(module, namespace_pulp, new_namespace_pulp, new_name)
                namespace_pulp = new_namespace_pulp
                name = new_name
                changed = True

        else:
            # Cases 3 and 4
            namespace_pulp = new_namespace_pulp
            name = new_name
            if not namespace_pulp.exists:
                # Case 3
                namespace_pulp.create({"name": name}, auto_exit=False)
                changed = True

    elif not namespace_pulp.exists:
        # Case 1
        namespace_pulp.create({"name": name}, auto_exit=False)
        changed = True

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
