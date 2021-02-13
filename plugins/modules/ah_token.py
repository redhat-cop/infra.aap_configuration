#!/usr/bin/python
# coding: utf-8 -*-


# (c) 2020, John Westcott IV <john.westcott.iv@redhat.com>
# (c) 2021, Sean Sullivan <@sean-m-sullivan>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


ANSIBLE_METADATA = {"metadata_version": "1.1", "status": ["preview"], "supported_by": "community"}

DOCUMENTATION = """
---
module: ah_token
author: "John Westcott IV (@john-westcott-iv), Sean Sullivan (@sean-m-sullivan)"
version_added: "2.10"
short_description: create, update, or destroy Automation Hub tokens.
description:
    - Create or destroy Automation Hub tokens. See
      U(https://www.ansible.com/tower) for an overview.
    - In addition, the module sets an Ansible fact which can be passed into other
      ah_* modules as the parameter ah_oauthtoken. See examples for usage.
    - Because of the sensitive nature of tokens, the created token value is only available once
      through the Ansible fact. (See RETURN for details)
    - Due to the nature of tokens in Automation Hub this module is not idempotent. A second will
      with the same parameters will create a new token.
    - If you are creating a temporary token for use with modules you should delete the token
      when you are done with it. See the example for how to do it.
options:
    state:
      description:
        - Desired state of the resource.
      choices: ["present", "absent"]
      default: "present"
      type: str
extends_documentation_fragment: redhat_cop.ah_configuration.auth
"""

EXAMPLES = """
- name: Create a new token using an existing token
  ah_token:
    ah_token: "{{ my_existing_token }}"

- name: Delete this token
  ah_token:
    ah_token: "{{ ah_token }}"
    state: absent

- name: Create a new token using username/password
  ah_token:
    state: present
    ah_username: "{{ my_username }}"
    ah_password: "{{ my_password }}"

- name: Use our new token to make another call
  namespace:
    ah_token: "{{ ah_token }}"
"""

RETURN = """
ah_token:
  type: dict
  description: An Ansible Fact variable representing a Tower token object which can be used for auth in subsequent modules. See examples for usage.
  contains:
    token:
      description: The token that was generated. This token can never be accessed again, make sure this value is noted before it is lost.
      type: str
    id:
      description: The numeric ID of the token created
      type: str
  returned: on successful create
"""

from ..module_utils.ah_module import AHModule


def return_token(module, last_response):
    # A token is special because you can never get the actual token ID back from the API.
    # So the default module return would give you an ID but then the token would forever be masked on you.
    # This method will return the entire token object we got back so that a user has access to the token

    module.json_output["ansible_facts"] = {
        # 'ah_token': last_response['token'],
        "ah_token": last_response,
    }
    module.exit_json(**module.json_output)


def main():
    # Any additional arguments that are not fields of the item can be added here
    argument_spec = dict(
        state=dict(choices=["present", "absent"], default="present"),
    )

    # Create a module for ourselves
    module = AHModule(argument_spec=argument_spec)

    # Extract our parameters
    state = module.params.get("state")

    # Delete an existing token
    if state == "absent":
        # If the state was absent we can let the module delete it if needed, the module will handle exiting from this
        existing_item = {}
        existing_item["endpoint"] = "auth/token/"
        existing_item["type"] = "token"
        module.delete_if_needed(existing_item)

    # If the state was present and we can let the module build or update the existing item, this will return on its own
    module.create_or_update_if_needed(
        None,
        None,
        endpoint="auth/token/",
        item_type="token",
        on_create=return_token,
    )


if __name__ == "__main__":
    main()
