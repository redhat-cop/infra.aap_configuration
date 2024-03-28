#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2023, Tom Page <@Tompage1994>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}


DOCUMENTATION = """
---
module: rulebook_activation
author: "Tom Page (@Tompage1994)"
short_description: Manage a rulebook_activation in EDA Controller
description:
    - Create, enable, disable and delete rulebook activations in EDA Controller
options:
    name:
      description:
        - The name of the rulebook activation.
      required: True
      type: str
    description:
      description:
        - The description of the rulebook_activation.
      required: False
      type: str
    project:
      description:
        - The project from which the rulebook is found.
      required: False
      type: str
    rulebook:
      description:
        - The name of the rulebook to activate.
      required: True
      type: str
    decision_environment:
      description:
        - The decision environment to be used.
      required: True
      type: str
    restart_policy:
      description:
        - The policy used to determine whether to restart a rulebook.
      required: False
      choices: ["always", "never", "on_failure"]
      default: "always"
      type: str
    extra_vars:
      description:
        - Specify C(extra_vars) for the template.
      required: False
      type: dict
    enabled:
      description:
        - Whether the rulebook activation is automatically enabled to run.
      default: true
      type: bool
    state:
      description:
        - Desired state of the resource.
      choices: ["present", "absent", "restarted"]
      default: "present"
      type: str

extends_documentation_fragment: infra.eda_configuration.auth
"""


EXAMPLES = """
- name: Create eda rulebook activation
  infra.eda_configuration.rulebook_activation:
    name: Github Hook
    description: Hook to listen for changes in GitHub
    project: eda_examples
    rulebook: git-hook-deploy-rules.yml
    decision_environment: my_de
    extra_vars:
      provider: github
      repo_url: https://github.com/ansible/ansible-rulebook.git
    enabled: true
    state: present

- name: Restart eda rulebook activation
  infra.eda_configuration.rulebook_activation:
    name: Github Hook
    state: restarted

- name: Delete eda rulebook activation
  infra.eda_configuration.rulebook_activation:
    name: Github Hook
    state: absent
"""

from ..module_utils.eda_module import EDAModule
import json


def main():
    # Any additional arguments that are not fields of the item can be added here
    argument_spec = dict(
        name=dict(required=True),
        description=dict(),
        project=dict(),
        rulebook=dict(required=True),
        decision_environment=dict(required=True),
        restart_policy=dict(choices=["always", "never", "on_failure"], default="always"),
        extra_vars=dict(type="dict"),
        enabled=dict(type="bool", default="true"),
        state=dict(choices=["present", "absent", "restarted"], default="present"),
    )

    # Create a module for ourselves
    module = EDAModule(argument_spec=argument_spec, required_if=[("state", "present", ("rulebook", "decision_environment"))])

    # Extract our parameters
    name = module.params.get("name")
    state = module.params.get("state")

    new_fields = {}

    # Attempt to look up an existing item based on the provided data
    existing_item = module.get_one("activations", name_or_id=name, key="req_url")

    if state == "absent":
        # If the state was absent we can let the module delete it if needed, the module will handle exiting from this
        module.delete_if_needed(existing_item, key="req_url")

    if state == "restarted":
        if module.params.get("enabled") is not None and not module.params.get("enabled"):
            module.fail_json(msg="It is not possible to restart a disabled rulebook activation. Ensure it is set to enabled.")
        # If the options want the activation enabled but it currently isn't then just run through as though enabling as that performs the restart
        if existing_item["is_enabled"]:
            # If the state was restarted we will hit the restart endpoint, the module will handle exiting from this
            # If the item doesn't exist we will just create it anyway
            module.trigger_post_action("activations/{id}/restart".format(id=existing_item["id"]), auto_exit=True)

    # Create the data that gets sent for create and update
    # Remove these two comments for final
    # Check that Links and groups works with this.
    for field_name in (
        "name",
        "description",
        "restart_policy",
    ):
        field_val = module.params.get(field_name)
        if field_val is not None:
            new_fields[field_name] = field_val

    if module.params.get("enabled") is not None:
        new_fields["is_enabled"] = module.params.get("enabled")

    if (module.params.get("project") is not None) and (module.params.get("rulebook") is not None):
        new_fields["project_id"] = module.resolve_name_to_id("projects", module.params.get("project"))
        new_fields["rulebook_id"] = module.resolve_name_to_id("rulebooks",
                                                              module.params.get("rulebook"),
                                                              data={"project_id": int(new_fields["project_id"])},
                                                              )
    else:
        new_fields["rulebook_id"] = module.resolve_name_to_id("rulebooks", module.params.get("rulebook"))

    if module.params.get("decision_environment") is not None:
        new_fields["decision_environment_id"] = module.resolve_name_to_id("decision-environments", module.params.get("decision_environment"))

    # Create the extra_vars
    if module.params.get("extra_vars") is not None:
        if existing_item is not None:
            new_fields["extra_var_id"] = -1  # Default it as something that isn't acceptable. Prove otherwise
            if existing_item["extra_var_id"]:
                # Check if matching existing extra_vars
                existing_vars = module.get_by_id("extra-vars", id=existing_item["extra_var_id"])
                # Test if the same
                if json.dumps(module.params.get("extra_vars")) == existing_vars["extra_var"]:
                    new_fields["extra_var_id"] = existing_item["extra_var_id"]
        else:
            new_fields["extra_var_id"] = module.create_no_name(
                {"extra_var": json.dumps(module.params.get("extra_vars"))},
                endpoint="extra-vars",
                item_type="extra_vars"
            )["id"]

    if existing_item is not None:
        # If the activation already exists, all we can do is change whether it is enabled or disabled.
        # The module will exit from this section

        # First, fail; if trying to change anything other than being enabled
        if ("description" in new_fields and existing_item["description"] != new_fields["description"]
                or "restart_policy" in new_fields and existing_item["restart_policy"] != new_fields["restart_policy"]
                or "project_id" in new_fields and existing_item["project_id"] != new_fields["project_id"]
                or "rulebook_id" in new_fields and existing_item["rulebook_id"] != new_fields["rulebook_id"]
                or "decision_environment_id" in new_fields and existing_item["decision_environment_id"] != new_fields["decision_environment_id"]
                or "extra_var_id" in new_fields and existing_item["extra_var_id"] != new_fields["extra_var_id"]):
            module.fail_json(msg="Once an activation has been created it can only be enabled, disabled or deleted. Other changes cannot be made.")

        if module.params.get("enabled") is not None:
            if module.params.get("enabled") and not existing_item["is_enabled"]:
                module.trigger_post_action("activations/{id}/enable".format(id=existing_item["id"]), auto_exit=True)
            elif (not module.params.get("enabled")) and existing_item["is_enabled"]:
                module.trigger_post_action("activations/{id}/disable".format(id=existing_item["id"]), auto_exit=True)
        module.exit_json(**module.json_output)

    # If the state was present and we can let the module build or update the existing item, this will return on its own
    module.create_if_needed(
        existing_item,
        new_fields,
        endpoint="activations",
        item_type="rulebook_activations",
    )


if __name__ == "__main__":
    main()
