#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2020, Sean Sullivan <@sean-m-sullivan>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


ANSIBLE_METADATA = {"metadata_version": "1.1", "status": ["preview"], "supported_by": "community"}


DOCUMENTATION = """
---
module: ah_collection
author: "Sean Sullivan (@sean-m-sullivan), Tom Page <@Tompage1994>"
short_description: update, or destroy Automation Hub Collections.
description:
    - Upload, or destroy Automation Hub Collections. See
      U(https://www.ansible.com/) for an overview.
options:
    namespace:
      description:
        - Namespace name. Must be lower case containing only alphanumeric characters and underscores.
      required: True
      type: str
    name:
      description:
        - Collection name. Must be lower case containing only alphanumeric characters and underscores.
      required: True
      type: str
    version:
      description:
        - Collection Version. Must be lower case containing only alphanumeric characters and underscores.
      type: str
    path:
      description:
        - Collection artifact file path.
      type: str
    wait:
      description:
        - Waits for the collection to be uploaded
      type: bool
      default: true
    auto_approve:
      description:
        - Approves a collection.
        - Requires version to be set.
      type: bool
      default: true
    overwrite_existing:
      description:
        - Overwrites an existing collection.
        - Requires version to be set.
      type: bool
      default: true
    state:
      description:
        - Desired state of the resource.
        - If present with a path, will upload a collection artifact to Automation hub.
        - If present will return data on a collection.
        - If present with version, will return data on a collection version.
        - If absent without version, will delete the collection and all versions.
        - If absent with version, will delete only specified version.
      choices: ["present", "absent"]
      default: "present"
      type: str

extends_documentation_fragment: redhat_cop.ah_configuration.auth
"""


EXAMPLES = """
- name: Upload collection to automation hub
  ah_collection:
    namespace: awx
    name: awx
    path: /var/tmp/collections/awx_awx-15.0.0.tar.gz


- name: Remove collection
  ah_collection:
    namespace: test_collection
    name: test
    version: 4.1.2
    state: absent
"""

from ..module_utils.ah_module import AHModule
import pathlib


def main():
    # Any additional arguments that are not fields of the item can be added here
    argument_spec = dict(
        namespace=dict(required=True),
        name=dict(required=True),
        path=dict(),
        wait=dict(type="bool", default=True),
        auto_approve=dict(type="bool", default=True),
        overwrite_existing=dict(type="bool", default=False),
        version=dict(),
        state=dict(choices=["present", "absent"], default="present"),
    )

    # Create a module for ourselves
    module = AHModule(argument_spec=argument_spec)

    # Extract our parameters
    namespace = module.params.get("namespace")
    name = module.params.get("name")
    path = module.params.get("path")
    wait = module.params.get("wait")
    overwrite_existing = module.params.get("overwrite_existing")
    auto_approve = module.params.get("auto_approve")
    version = module.params.get("version")
    state = module.params.get("state")

    # Attempt to look up an existing item based on the provided data
    if version:
        collection_endpoint = "collections/{0}/{1}/versions/{2}".format(namespace, name, version)
    else:
        collection_endpoint = "collections/{0}/{1}".format(namespace, name)

    existing_item = module.get_endpoint(collection_endpoint, **{"return_none_on_404": True})

    # If state is absent, check if it exists, delete and exit.
    if state == "absent":
        if existing_item is None:
            module.json_output["deleted"] = False
            module.json_output["changed"] = False
        else:
            # If the state was absent we can let the module delete it if needed, the module will handle exiting from this
            module.json_output["task"] = module.delete_endpoint(existing_item["json"]["href"])["json"]["task"]
            module.json_output["deleted"] = True
            module.json_output["changed"] = True
        module.exit_json(**module.json_output)
    else:
        file = pathlib.Path(path)
        if not file.exists():
            module.fail_json(msg="Could not find Collection {0}.{1} in path {2}".format(namespace, name, path))

    if path:
        if existing_item is not None and overwrite_existing:
            # Delete collection
            module.json_output["task"] = module.delete_endpoint(existing_item["json"]["href"])["json"]["task"]
            module.json_output["deleted"] = True
            # Upload new collection
            module.upload(path, "artifacts/collections", wait, item_type="collections")
            module.json_output["changed"] = True
            # Get new collection version
            existing_item = module.get_endpoint(collection_endpoint, **{"return_none_on_404": True})
            if auto_approve:
                module.approve(
                    endpoint=collection_endpoint,
                )
        elif existing_item is None:
            module.upload(path, "artifacts/collections", wait, item_type="collections")
            module.json_output["changed"] = True
            if auto_approve:
                module.approve(
                    endpoint=collection_endpoint,
                )
        else:
            module.json_output["changed"] = False
    else:
        if existing_item is None and state == "absent":
            module.json_output["deleted"] = False
            module.json_output["changed"] = False
        elif existing_item is None:
            if version:
                module.fail_json(msg="Could not find Collection {0}.{1} with_version {2}".format(namespace, name, version))
            else:
                module.fail_json(msg="Could not find Collection {0}.{1}".format(namespace, name))
        else:
            module.json_output["collection"] = existing_item["json"]

    # If state is absent, check if it exists, delete and exit.
    if state == "absent":
        if existing_item is None:
            module.json_output["deleted"] = False
            module.json_output["changed"] = False
        else:
            # If the state was absent we can let the module delete it if needed, the module will handle exiting from this
            module.json_output["task"] = module.delete_endpoint(existing_item["json"]["href"])["json"]["task"]
            module.json_output["deleted"] = True
            module.json_output["changed"] = True

    # If the state was present and we can Return information about the collection
    module.exit_json(**module.json_output)


if __name__ == "__main__":
    main()
