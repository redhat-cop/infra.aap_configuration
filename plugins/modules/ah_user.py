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
module: ah_user
short_description: Manage private automation hub users
description:
  - Create, delete, and update user accounts in private automation hub.
version_added: '0.4.3'
author: Herve Quatremain (@herve4m)
options:
  username:
    description:
      - Name of the user to create, remove, or modify.
    required: true
    type: str
  groups:
    description:
      - List of the groups the user is added to. When not set or set to an
        empty list (C([])), the module removes the user from all groups.
    type: list
    elements: str
  append:
    description:
      - If C(yes), then add the user to the groups specified in C(groups).
      - If C(no), then the module only adds the user to the groups specified in
        C(groups), removing them from all other groups.
    type: bool
    default: yes
  first_name:
    description:
      - User's first name.
    type: str
  last_name:
    description:
      - User's last name.
    type: str
  email:
    description:
      - User's email address. That address must be correctly formed.
    type: str
  is_superuser:
    description:
      - Gives the super user permissions to the user.
    type: bool
    default: False
    aliases: ['superuser']
  password:
    description:
      - User's password as a clear string. The password must contain at least 9 characters with numbers or special characters.
    type: str
  state:
    description:
      - If C(absent), then the module deletes the user.
      - The module does not fail if the user does not exist because the state is already as expected.
      - If C(present), then the module creates the user if it does not already exist.
        If the user account already exists, then the module updates its state.
    type: str
    default: present
    choices: [absent, present]
seealso:
  - module: redhat_cop.ah_configuration.ah_group_perm
  - module: redhat_cop.ah_configuration.ah_group
notes:
  - Supports C(check_mode).
extends_documentation_fragment: redhat_cop.ah_configuration.auth_ui
"""

EXAMPLES = r"""
- name: Ensure the user exists
  redhat_cop.ah_configuration.ah_user:
    username: lvasquez
    first_name: Lena
    last_name: Vasquez
    email: lvasquez@example.com
    password: vs9mrD55NP
    groups:
      - operators
    state: present
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Ensure the user is removed
  redhat_cop.ah_configuration.ah_user:
    username:  dwilde
    state: absent
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Ensure the user only belongs to the operators and developers groups
  redhat_cop.ah_configuration.ah_user:
    username: qhazelrigg
    state: present
    groups:
      - operators
      - developers
    append: false
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Ensure the user is added to the managers group
  redhat_cop.ah_configuration.ah_user:
    username: chorwitz
    state: present
    groups:
      - managers
    append: true
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Ensure the password is changed
  redhat_cop.ah_configuration.ah_user:
    username: jziglar
    state: present
    password: bQtVeBUK2F
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Ensure the user is a super user
  redhat_cop.ah_configuration.ah_user:
    username:  ekrob
    state: present
    is_superuser: true
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t
"""

RETURN = r""" # """

from ..module_utils.ah_api_module import AHAPIModule
from ..module_utils.ah_ui_object import AHUIUser, AHUIGroup


def main():
    argument_spec = dict(
        username=dict(required=True),
        first_name=dict(),
        last_name=dict(),
        email=dict(),
        is_superuser=dict(type="bool", default=False, aliases=["superuser"]),
        password=dict(no_log=True),
        groups=dict(type="list", elements="str"),
        append=dict(type="bool", default=True),
        state=dict(choices=["present", "absent"], default="present"),
    )

    # Create a module for ourselves
    module = AHAPIModule(argument_spec=argument_spec, supports_check_mode=True)

    # Extract our parameters
    username = module.params.get("username")
    first_name = module.params.get("first_name")
    last_name = module.params.get("last_name")
    email = module.params.get("email")
    is_superuser = module.params.get("is_superuser")
    password = module.params.get("password")
    groups = module.params.get("groups")
    append = module.params.get("append")
    state = module.params.get("state")

    # Authenticate
    module.authenticate()
    user = AHUIUser(module)

    # Get the user details from its name.
    # API (GET): /api/galaxy/_ui/v1/users/?username=<user_name>
    user.get_object(username)

    # Removing the user
    if state == "absent":
        # Cannot delete an account that has the super user flag.
        # First, remove that super user status from the account.
        if user.superuser:
            new_fields = {"username": username, "is_superuser": False}
            user.update(new_fields, auto_exit=False)
        user.delete()

    # Confirm that all the given groups exist and retrieve their details
    group = AHUIGroup(module)
    group_ids = []
    if groups is not None:
        error_groups = []
        for group_name in groups:
            group.get_object(group_name)
            if group.exists:
                group_ids.append(group.data)
            else:
                error_groups.append(group_name)
        if error_groups:
            module.fail_json(msg="unknown groups: %s" % ", ".join(error_groups))

    # Create the data that gets sent for create and update
    new_fields = {}
    if username is not None:
        new_fields["username"] = username
    if first_name is not None:
        new_fields["first_name"] = first_name
    if last_name is not None:
        new_fields["last_name"] = last_name
    if email is not None:
        new_fields["email"] = email
    if is_superuser is not None:
        new_fields["is_superuser"] = is_superuser
    if password is not None:
        new_fields["password"] = password

    if append and user.exists:
        ids = [v["id"] for v in group_ids]
        for g in user.groups:
            if "id" in g and g["id"] not in ids:
                group_ids.append(g)
    new_fields["groups"] = group_ids

    # API (POST): /api/galaxy/_ui/v1/users/
    # API (PUT): /api/galaxy/_ui/v1/users/<USER_ID#>/
    user.create_or_update(new_fields)


if __name__ == "__main__":
    main()
