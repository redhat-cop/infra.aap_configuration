#!/usr/bin/python
# coding: utf-8 -*-

# Copyright: (c) 2023, Jiří Jeřábek <@jerabekjiri>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: collection_repository
author: Jiří Jeřábek (@jerabekjiri)
short_description: Create, Update, Delete repository
description:
    - Configure an Automation Hub repository. See
      U(https://www.ansible.com/) for an overview.
options:
    name:
      description:
        - Collection Repository name.
      required: True
      type: str
    description:
      description:
        - Description for the Collection repository.
      type: str
    retain_repo_versions:
      description:
        - Retain X versions of the repository. Default is 0 which retains all versions.
      type: int
      default: 0
    pulp_labels:
      description: Pipeline and search options for the collection repository.
      type: dict
      suboptions:
        pipeline:
          description: Pipeline adds repository labels with pre-defined meanings.
          type: str
          choices: [None, "approved", "staging", "rejected"]
        hide_from_search:
          description: Prevent collections in this repository from showing up on the home page.
          type: str
    distribution:
      description:
        - Content in repositories without a distribution will not be visible to clients for sync, download or search.
      type: dict
      suboptions:
        name:
          description:
            - Distribution name and base_path.
            - If not set, repository name is used.
          type: str
        state:
          description:
            - If C(absent), then the module deletes the distribution.
            - If C(present), then the module creates or updates the distribution.
          type: str
          choices: ["present", "absent"]
          default: present
    private:
      description:
        - Make the repository private.
      type: bool
      default: False
    remote:
      description:
        - Existing remote name.
      type: str
    update_repo:
      description:
        - Whether to update the collection repository before exiting the module.
      required: false
      default: False
      type: bool
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
          amount of seconds
      type: int
    state:
      description:
        - If C(absent), then the module deletes the repository and its distribution.
        - If C(present), then the module updates the repository.
      type: str
      choices: ["present", "absent"]
      default: present
extends_documentation_fragment: galaxy.galaxy.auth_ui
"""


EXAMPLES = """
- name: Create "foobar" repository with distribution and remote
  collection_repository:
    name: "foobar"
    description: "description of foobar repository"
    pulp_labels:
      pipeline: "approved"
    distribution:
      name: "foobar"
      state: present
    remote: community
    wait: true

- name: Create rejected "foobar" repository with
  collection_repository:
    name: "foobar"
    description: "description of foobar repository"
    pulp_labels:
      pipeline: "rejected"
      hide_from_search: ""

- name: Delete "foobar" repository
  collection_repository:
    name: foobar
    state: absent
"""

from ..module_utils.ah_api_module import AHAPIModule
from ..module_utils.ah_pulp_object import (
    AHPulpAnsibleRepository,
    AHPulpAnsibleDistribution,
    AHPulpAnsibleRemote,
)


def main():
    # Any additional arguments that are not fields of the item can be added here
    argument_spec = dict(
        name=dict(required=True),
        description=dict(),
        retain_repo_versions=dict(type="int", default=0),
        distribution=dict(type="dict"),
        pulp_labels=dict(type="dict"),
        private=dict(type="bool", default=False),
        remote=dict(),
        update_repo=dict(type="bool", default=False),
        wait=dict(default=True, type="bool"),
        interval=dict(default=1.0, type="float"),
        timeout=dict(default=None, type="int"),
        state=dict(choices=["present", "absent"], default="present"),
    )

    module = AHAPIModule(argument_spec=argument_spec, supports_check_mode=True)

    # Extract our parameters
    name = module.params.get("name")
    module.fail_on_missing_params(["name"])
    update_repo = module.params.get("update_repo")
    wait = module.params.get("wait")
    interval = module.params.get("interval")
    timeout = module.params.get("timeout")
    new_fields = {}
    repo_fields = {}

    repo_keys = [
        "name",
        "description",
        "retain_repo_versions",
        "pulp_labels",
        "private",
        "remote",
    ]

    for field_name in (*repo_keys, "distribution", "state"):
        field_val = module.params.get(field_name)
        if field_val is not None:
            new_fields[field_name] = field_val

            if field_name in repo_keys:
                repo_fields[field_name] = field_val

    if repo_fields["retain_repo_versions"] == 0:
        repo_fields["retain_repo_versions"] = None
    ansible_repository = AHPulpAnsibleRepository(module)
    ansible_repository.get_object(name=name)

    distro = new_fields.get("distribution")
    if distro:
        # if "distribution" is set, but "state" is missing, set "present"
        distro_state = distro.get("state", None)

        if distro_state not in [None, "present", "absent"]:
            module.fail_json(
                msg="value of state must be one of: present, absent, got: {0}".format(
                    distro_state
                )
            )

        if not distro_state:
            distro_state = "present"

        # if distro name isn't specified, use repo name as distro
        distro_name = distro.get("name", None)
        if not distro_name:
            distro_name = name

        ansible_distro = AHPulpAnsibleDistribution(module)
        ansible_distro.get_object(name=distro_name)

    if new_fields.get("state") == "absent":
        if distro:
            ansible_distro.delete(auto_exit=False)

        ansible_repository.delete(auto_exit=True)

    remote = new_fields.get("remote")
    if remote:
        ansible_remote = AHPulpAnsibleRemote(module)
        ansible_remote.get_object(name=remote)

        if not ansible_remote.exists:
            module.fail_json(msg="Remote {0} doesn't exist.".format(remote))

        repo_fields["remote"] = ansible_remote.data.get("pulp_href")
    else:
        repo_fields["remote"] = None

    if ansible_repository.exists:
        ansible_repository.update(new_item=repo_fields, auto_exit=False)
    else:
        ansible_repository.create(new_item=repo_fields, auto_exit=False)

    repo_href = ansible_repository.data.get("pulp_href")

    if distro:
        if not ansible_distro.exists:
            if distro_state == "present":
                ansible_distro.create(
                    new_item={
                        "base_path": distro_name,
                        "name": distro_name,
                        "repository": repo_href,
                    },
                    auto_exit=False,
                )
        else:
            if distro_state == "absent":
                ansible_distro.delete(auto_exit=False)
            elif distro_state == "present":
                ansible_distro.update(
                    new_item={"base_path": distro_name, "repository": repo_href},
                    auto_exit=False,
                )

    if update_repo:
        ansible_repository.sync(wait, interval, timeout)

    module.exit_json(**module.json_output)


if __name__ == "__main__":
    main()
