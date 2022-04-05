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
module: ah_ee_image
short_description: Manage private automation hub execution environment images
description:
  - Delete execution environment images.
  - Update container image tags.
version_added: '0.4.3'
author: Herve Quatremain (@herve4m)
options:
  name:
    description:
      - Name and tag of the image to remove or modify.
      - Use a colon character between the image name and the tag.
    required: true
    type: str
  tags:
    description:
      - List of the image tags to update.
      - Only used when C(state) is set to C(present), otherwise ignored.
    type: list
    elements: str
  append:
    description:
      - If C(yes), then add the tags specified in C(tags) to the image.
      - If C(no), then the module sets the image tags to the given list and removes all the other existing tags.
    type: bool
    default: yes
  state:
    description:
      - If C(absent), then the module deletes the image and all its tags.
      - If C(present), then the module updates the image tags.
    type: str
    default: present
    choices: [absent, present]
notes:
  - Supports C(check_mode).
  - Only works with private automation hub v4.3.2 or later.
extends_documentation_fragment: redhat_cop.ah_configuration.auth_ui
"""

EXAMPLES = r"""
- name: Ensure the image has the additional tags
  redhat_cop.ah_configuration.ah_ee_image:
    name: ansible-automation-platform-20-early-access/ee-supported-rhel8:2.0.0-15
    state: present
    tags:
      - v2
      - "2.0"
      - prod1
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Replace all the image tags
  redhat_cop.ah_configuration.ah_ee_image:
    name: ansible-automation-platform-20-early-access/ee-supported-rhel8:2.0.0-15
    state: present
    append: false
    tags:
      - prod2
      - "2.0"
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Ensure the image does not exist
  redhat_cop.ah_configuration.ah_ee_image:
    name: ansible-automation-platform-20-early-access/ee-supported-rhel8:2.0
    state: absent
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t
"""

RETURN = r""" # """

from ..module_utils.ah_api_module import AHAPIModule
from ..module_utils.ah_ui_object import AHUIEEImage
from ..module_utils.ah_pulp_object import AHPulpEERepository


def main():
    argument_spec = dict(
        name=dict(required=True),
        tags=dict(type="list", elements="str"),
        append=dict(type="bool", default=True),
        state=dict(choices=["present", "absent"], default="present"),
    )

    # Create a module for ourselves
    module = AHAPIModule(argument_spec=argument_spec, supports_check_mode=True)

    # Extract our parameters
    name_with_tag = module.params.get("name")
    tags = module.params.get("tags")
    append = module.params.get("append")
    state = module.params.get("state")

    name_tag = name_with_tag.rsplit(":", 1)
    name = name_tag[0]
    tag = "latest" if len(name_tag) == 1 else name_tag[1]

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

    # The repository must exist.
    if not repository_pulp.exists:
        module.fail_json(msg="The {repository} repository does not exist.".format(repository=name))

    # Process the object from the UI API
    image_ui = AHUIEEImage(module)

    # Get the repository details from the name and tag.
    # API (GET): /api/galaxy/_ui/v1/execution-environments/repositories/<name>/_content/images/
    image_ui.get_tag(name, tag)

    # Removing the image
    if state == "absent":
        if image_ui.digest is None:
            json_output = {"name": name, "tag": tag, "type": "image", "changed": False}
            module.exit_json(**json_output)
        repository_pulp.delete_image(image_ui.digest)

    if image_ui.digest is None:
        module.fail_json(msg="The image tag {tag} for the {repository} repository does not exist.".format(tag=tag, repository=name))

    # When the user does not set the `tags' option (or gives an empty list), then
    # do nothing in append mode, and delete the whole image when append is False.
    if tags is None or len(tags) == 0:
        if append:
            json_output = {"name": name, "tag": tag, "type": "image", "changed": False}
            module.exit_json(**json_output)
        repository_pulp.delete_image(image_ui.digest)

    current_tags = set(image_ui.tags)
    new_tags = set(tags)

    # Adding new tags to the image
    tags_to_add = new_tags - current_tags
    for t in tags_to_add:
        repository_pulp.create_tag(image_ui.digest, t, auto_exit=False)

    if append:
        json_output = {"name": name, "tag": tag, "type": "image", "changed": True if tags_to_add else False}
        module.exit_json(**json_output)

    # Removing tags from the image
    tags_to_remove = current_tags - new_tags
    for t in tags_to_remove:
        repository_pulp.delete_tag(image_ui.digest, t, auto_exit=False)
    json_output = {"name": name, "tag": tag, "type": "image", "changed": True if tags_to_remove or tags_to_add else False}
    module.exit_json(**json_output)


if __name__ == "__main__":
    main()
