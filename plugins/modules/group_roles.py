#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Sean Sullivan <ssulliva@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# You can consult the UI API documentation directly on a running private
# automation hub at https://hub.example.com/pulp/api/v3/docs/


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: group_roles
short_description: Add roles to private automation hub user groups
description:
  - Add roles to private automation hub user groups.
  - Requires AAP 2.3 or Galaxy 4.6 or Later for global roles.
  - Requires AAP 2.4 or Galaxy 4.7 or Later for most targeted roles.
version_added: '2.0.0'
author: Sean Sullivan (@sean-m-sullivan)
options:
  groups:
    description:
      - List of Group names that receive the permissions specified by the roles.
      - If the group is not found, it will be created.
    required: True
    type: list
    elements: str
  role_list:
    description:
      - List of sets of roles and targets to apply to the groups.
    required: True
    type: list
    elements: dict
    suboptions:
      roles:
        description:
          - List of roles to apply to the groups.
        type: list
        elements: str
      targets:
        description:
          - List of targets to apply the roles to.
          - If left empty, it will give global permissions to the group.
          - An example of using this would be to give a specific group rights over a list of collection namespaces.
        type: dict
        default: {}
        suboptions:
          collection_namespaces:
            description:
              - List of collection namespaces to limit the role permissions to.
            type: list
            default: []
            elements: str
          collection_remotes:
            description:
              - List of collection remotes to limit the role permissions to.
            type: list
            default: []
            elements: str
          collection_repositories:
            description:
              - List of collection repositories to limit the role permissions to.
            type: list
            default: []
            elements: str
          execution_environments:
            description:
              - List of execution environments to limit the role permissions to.
            type: list
            default: []
            elements: str
          container_registery_remotes:
            description:
              - List of container remote registries to limit the role permissions to.
            type: list
            default: []
            elements: str
  state:
    description:
      - If C(absent), then the module deletes the given combination of roles for given groups.
      - The module does not fail if the combination does not exist because the state is already as expected.
      - If C(present), then the module creates the group roles if it does not already exist.
      - If already existing, no change is made.
      - If C(enforced), then the module will remove any group role combinations not provided.
    type: str
    default: present
    choices: [present, enforced, absent]
extends_documentation_fragment: galaxy.galaxy.auth_ui
"""

EXAMPLES = """
- name: Ensure the group exists
  galaxy.galaxy.group_roles:
    groups:
      - santa
      - group1
    role_list:
      - roles:
          - galaxy.group_admin
      - roles:
          - galaxy.collection_remote_owner
        targets:
          collection_remotes:
            - community
      - roles:
          - galaxy.execution_environment_admin
      - roles:
          - galaxy.collection_namespace_owner
        targets:
          collection_namespaces:
            - autohubtest2
    state: present
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t
"""

from ..module_utils.ah_api_module import AHAPIModule
from ..module_utils.ah_module import AHModule
from ..module_utils.ah_ui_object import AHUIEERegistry
from ..module_utils.ah_pulp_object import (
    AHPulpRolePerm,
    AHPulpGroups,
    AHPulpAnsibleRepository,
    AHPulpAnsibleRemote,
    AHPulpEERepository,
)


def main():
    argument_spec = dict(
        groups=dict(type='list', elements='str', required=True),
        role_list=dict(type='list', elements='dict', required=True),
        state=dict(choices=["present", "enforced", "absent"], default="present"),
    )

    # Create a module for ourselves
    module = AHAPIModule(argument_spec=argument_spec, supports_check_mode=True)
    group_role_data = {}
    # Extract our parameters
    group_list = module.params.get("groups")
    group_role_data['role_list'] = module.params.get("role_list")
    state = module.params.get("state")
    # Set role data defaults
    group_role_data['perm_list'] = []
    # Set Group object
    group = AHPulpGroups(module)
    vers = module.get_server_version()

    for index, role_item in enumerate(group_role_data['role_list']):
        group_role_data['role_list'][index]['content_urls'] = []
        if "targets" in role_item and role_item['targets'] is not None:
            if "collection_namespaces" in role_item['targets']:
                namespace = AHModule(argument_spec=argument_spec)
                for namespace_item in role_item['targets']['collection_namespaces']:
                    namespace_lookup = namespace.get_one("namespaces", name_or_id=namespace_item)
                    if namespace_lookup is not None:
                        group_role_data['role_list'][index]['content_urls'].append(namespace_lookup['pulp_href'])
                    else:
                        module.fail_json(msg="Collection Namespace `{0}` was not found".format(namespace_item))
            if "users" in role_item['targets']:
                module.fail_json(msg="*Users cannot have targets, only global permissions allowed")
            if "groups" in role_item['targets']:
                module.fail_json(msg="Groups cannot have targets, only global permissions allowed")
            if "collection_remotes" in role_item['targets']:
                ansible_remote = AHPulpAnsibleRemote(module)
                for collection_remote_item in role_item['targets']['collection_remotes']:
                    ansible_remote.get_object(name=collection_remote_item)
                    if ansible_remote.exists:
                        group_role_data['role_list'][index]['content_urls'].append(ansible_remote.data['pulp_href'])
                    else:
                        module.fail_json(msg="Collection Remote `{0}` was not found".format(collection_remote_item))
            if "collection_repositories" in role_item['targets']:
                ansible_repository = AHPulpAnsibleRepository(module)
                for collection_repositories_item in role_item['targets']['collection_repositories']:
                    ansible_repository.get_object(name=collection_repositories_item)
                    if ansible_repository.exists:
                        group_role_data['role_list'][index]['content_urls'].append(ansible_repository.data['pulp_href'])
                    else:
                        module.fail_json(msg="Collection Repository `{0}` was not found".format(collection_repositories_item))
            if "execution_environments" in role_item['targets']:
                repository_pulp = AHPulpEERepository(module)
                for execution_environment_item in role_item['targets']['execution_environments']:
                    repository_pulp.get_object(execution_environment_item)
                    if repository_pulp.exists:
                        group_role_data['role_list'][index]['content_urls'].append(repository_pulp.data['pulp_href'])
                    else:
                        module.fail_json(msg="Execution Environment `{0}` was not found".format(execution_environment_item))
            if "container_registery_remotes" in role_item['targets']:
                registry = AHUIEERegistry(module)
                for container_registery_remote_item in role_item['targets']['container_registery_remotes']:
                    registry.get_object(container_registery_remote_item, vers)
                    if registry.exists:
                        group_role_data['role_list'][index]['content_urls'].append(registry.data['pulp_href'])
                    else:
                        module.fail_json(msg="Container Registry Remote `{0}` was not found".format(container_registery_remote_item))
            for role in role_item['roles']:
                role_pulp = AHPulpRolePerm(module)
                role_pulp.get_object(role)
                if role_pulp.exists:
                    for content_url in role_item['content_urls']:
                        group_role_data['perm_list'].append(
                            {
                                "role": role_pulp.data['name'],
                                "content_object": content_url
                            }
                        )
                else:
                    module.fail_json(msg="Role `{0}` was not found".format(role))
        else:
            for role in role_item['roles']:
                role_pulp = AHPulpRolePerm(module)
                role_pulp.get_object(role)
                if role_pulp.exists:
                    group_role_data['perm_list'].append(
                        {
                            "role": role,
                            "content_object": None
                        }
                    )
                else:
                    module.fail_json(msg="Role `{0}` was not found".format(role))

    # Set Base output Lists for actions
    group.api.json_output['removed'] = []
    group.api.json_output['added'] = []
    group.api.json_output['existing'] = []
    # Process roles on each group
    for group_item in group_list:
        group.get_object(group_item)
        if not group.exists:
            group.create_or_update({"name": group_item}, auto_exit=False)
        group.data['before_perms'] = group.get_perms(group.data)
        # Perform associations
        associations = group.associate_permissions(group_data=group.data, new_perms=group_role_data['perm_list'], state=state)
        # Add data to output
        if 'removed' in group.api.json_output:
            group.api.json_output['removed'].extend(associations['removed'])
        if 'added' in group.api.json_output:
            group.api.json_output['added'].extend(associations['added'])
        if 'existing' in group.api.json_output:
            group.api.json_output['existing'].extend(associations['existing'])
    # Add general Data to Output
    group.api.json_output.update(group_role_data)
    group.api.exit_json(**group.api.json_output)


if __name__ == "__main__":
    main()
