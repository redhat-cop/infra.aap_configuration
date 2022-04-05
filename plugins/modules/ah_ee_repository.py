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
module: ah_ee_repository
short_description: Manage private automation hub execution environment repositories/containers
description:
  - Update and delete execution environment repositories (also known as containers).
  - Grant group access to repositories.
version_added: '0.4.3'
author: Herve Quatremain (@herve4m)
options:
  name:
    description:
      - Name of the repository to remove or modify.
    required: true
    type: str
  new_name:
    description:
      - New name for the repository. Setting this option changes the name of the repository which current name is set in C(name).
    type: str
  delete_namespace_if_empty:
    description:
      - If C(true), then the module deletes the original namespace if it is empty after the repository has been deleted or moved.
      - If C(false), then the module keeps the namespace even if it is empty.
      - Use C(false) when you plan to re-use the namespace and you want to preserve its parameters, such as the group permissions.
      - Only used when C(new_name) is set or C(state) is C(absent).
    type: bool
    default: true
  description:
    description:
      - Text that describes the repository.
    type: str
  readme:
    description:
      - README text in Markdown format for the repository.
      - Mutually exclusive with the C(readme_file) option.
    type: str
  readme_file:
    description:
      - Path to a README file in Markdown format to associate with the repository.
      - Mutually exclusive with the C(readme) option.
    type: path
  state:
    description:
      - If C(absent), then the module deletes the repository.
      - The module does not fail if the repository does not exist because the state is already as expected.
      - If C(present), then the module sets the description and README file for the repository.
    type: str
    default: present
    choices: [absent, present]
notes:
  - Supports C(check_mode).
  - Only works with private automation hub v4.3.2 or later.
  - The module cannot be use to create repositories.
    Use C(podman push) for example to create repositories.
extends_documentation_fragment: redhat_cop.ah_configuration.auth_ui
"""

EXAMPLES = r"""
- name: Ensure the repository description and README are set
  redhat_cop.ah_configuration.ah_ee_repository:
    name: ansible-automation-platform-20-early-access/ee-supported-rhel8
    state: present
    description: Supported execution environment
    readme: |
      # My execution environment

      * bullet 1
      * bullet 2
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Ensure the repository README is set
  redhat_cop.ah_configuration.ah_ee_repository:
    name: ansible-automation-platform-20-early-access/ee-supported-rhel8
    state: present
    readme_file: README.md
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Ensure the repository has the new name
  redhat_cop.ah_configuration.ah_ee_repository:
    name: ansible-automation-platform-20-early-access/ee-supported-rhel8
    new_name: aap-20/supported
    delete_namespace_if_empty: false
    state: present
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Ensure the repository is removed
  redhat_cop.ah_configuration.ah_ee_repository:
    name: ansible-automation-platform-20-early-access/ee-supported-rhel8
    state: absent
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t
"""

RETURN = r""" # """

import os
import os.path

from ..module_utils.ah_api_module import AHAPIModule
from ..module_utils.ah_ui_object import AHUIEERepository
from ..module_utils.ah_pulp_object import AHPulpEERepository, AHPulpEENamespace


def delete_empty_namespace(module, repository_name):
    """Delete the namespace of the given repository name.

    :param module: The API object that the function uses to access the API.
    :type module: :py:class:``ah_api_module.AHAPIModule``
    :param repository_name: Name of the repository for which the namespace must
                            be deleted if empty.
    :type repository_name: str
    """
    namespace_name = repository_name.split("/", 1)[0]
    repos = AHPulpEERepository.get_repositories_in_namespace(module, namespace_name)
    if len(repos) == 0:
        namespace_pulp = AHPulpEENamespace(module)
        namespace_pulp.get_object(namespace_name)
        namespace_pulp.delete(auto_exit=False)


def rename_repository(module, repository_pulp, old_name, new_name, delete_namespace_if_empty=True):
    """Rename the given repository.

    :param module: The API object that the function uses to access the API.
    :type module: :py:class:``ah_api_module.AHAPIModule``
    :param repository_pulp: The Pulp object that represents the repository
                            to rename.
    :type repository_pulp: :py:class:``ah_pulp_object.AHPulpEERepository``
    :param old_name: Current name of the repository to rename.
    :type old_name: str
    :param new_name: New name of the repository.
    :type new_name: str
    :param delete_namespace_if_empty: If ``True``, then the function deletes
                                      the original namespace if its empty.
    :type delete_namespace_if_empty: bool
    """
    repository_pulp.update({"name": new_name, "base_path": new_name}, auto_exit=False)
    if delete_namespace_if_empty:
        delete_empty_namespace(module, old_name)


def main():
    argument_spec = dict(
        name=dict(required=True),
        new_name=dict(),
        delete_namespace_if_empty=dict(type="bool", default=True),
        description=dict(),
        readme=dict(),
        readme_file=dict(type="path"),
        state=dict(choices=["present", "absent"], default="present"),
    )

    # Create a module for ourselves
    module = AHAPIModule(argument_spec=argument_spec, supports_check_mode=True, mutually_exclusive=[("readme", "readme_file")])

    # Extract our parameters
    name = module.params.get("name")
    new_name = module.params.get("new_name")
    delete_namespace_if_empty = module.params.get("delete_namespace_if_empty")
    description = module.params.get("description")
    readme = module.params.get("readme")
    readme_file = module.params.get("readme_file")
    state = module.params.get("state")

    # Authenticate
    module.authenticate()

    # Only recent versions support execution environment
    vers = module.get_server_version()
    if vers < "4.3.2":
        module.fail_json(msg="This module requires private automation hub version 4.3.2 or later. Your version is {vers}".format(vers=vers))

    # Process the object from the Pulp API (delete or create)
    repository_pulp = AHPulpEERepository(module)

    # API (GET): /pulp/api/v3/distributions/container/container/?name=<name>
    repository_pulp.get_object(name)

    # Removing the repository
    if state == "absent":
        if not repository_pulp.delete(auto_exit=False):
            json_output = {"name": name, "type": repository_pulp.object_type, "changed": False}
            module.exit_json(**json_output)
        if delete_namespace_if_empty:
            delete_empty_namespace(module, name)
        json_output = {"name": name, "type": repository_pulp.object_type, "changed": True}
        module.exit_json(**json_output)

    # If a README file is given, verify that it exists and then read it.
    if readme_file is not None:
        if not os.path.isfile(readme_file):
            module.fail_json(msg="The {file} file does not exist or is not a file.".format(file=readme_file))

        if not os.access(readme_file, os.R_OK):
            module.fail_json(msg="You do not have read access to the {file} file.".format(file=readme_file))

        # Read in the file contents
        try:
            with open(readme_file, "r") as f:
                readme = f.read()
        except Exception as e:
            module.fail_json(msg="Cannot read {file}: {error}".format(file=readme_file, error=e))

    changed = False
    if new_name and new_name != name:
        new_repository_pulp = AHPulpEERepository(module)
        new_repository_pulp.get_object(new_name)
        if new_repository_pulp.exists:
            if repository_pulp.exists:
                # Both repositories in `name` and `new_name` cannot exist.
                # Cannot rename a repo when the destination already exists.
                module.fail_json(msg="The repository {repository} (`new_name') already exists".format(repository=new_name))
            else:
                # Only the repository defined in `new_name` exists. Renaming is
                # already done. Use that `new_name` repository for the rest of
                # the module.
                repository_pulp = new_repository_pulp
                name = new_name
        elif repository_pulp.exists:
            rename_repository(module, repository_pulp, name, new_name, delete_namespace_if_empty)
            name = new_name
            changed = True

    # The repository must exist. The module does not create it.
    if not repository_pulp.exists:
        module.fail_json(msg="The {repository} repository does not exist.".format(repository=name))

    if description is not None and repository_pulp.update({"description": description}, auto_exit=False):
        changed = True

    if readme is None:
        json_output = {"name": repository_pulp.name, "type": repository_pulp.object_type, "changed": changed}
        module.exit_json(**json_output)

    # Process the object from the UI API
    repository_ui = AHUIEERepository(module)

    # Get the repository details from its name.
    # API (GET): /api/galaxy/_ui/v1/execution-environments/repositories/<name>/
    repository_ui.get_object(name)

    # API (GET): /api/galaxy/_ui/v1/execution-environments/repositories/<name>/_content/readme/
    # API (PUT): /api/galaxy/_ui/v1/execution-environments/repositories/<name>/_content/readme/
    updated = repository_ui.update_readme(readme, auto_exit=False)
    json_output = {"name": repository_ui.name, "type": repository_ui.object_type, "changed": changed or updated}
    module.exit_json(**json_output)


if __name__ == "__main__":
    main()
