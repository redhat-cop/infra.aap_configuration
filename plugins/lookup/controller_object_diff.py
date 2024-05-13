# (c) 2020 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
name: controller_object_diff
author: "Sean Sullivan (@sean-m-sullivan)"
short_description: Return difference for objects from Controller API
requirements:
  - None
description:
  - Takes results of GET requests from the Automation Platform Controller API. See
    U(https://docs.ansible.com/ansible-tower/latest/html/towerapi/index.html) for API usage.
  - Returns difference of on Unique Name and Organization, between two sets of groups
options:
  api_list:
    description:
      - The list of objects returned from the controller api.
      - Requires at least two items in the list
    type: list
    elements: dict
    required: True
  compare_list:
    description:
      - The list of objects to compare the api_list to.
    type: list
    elements: dict
    required: True
  set_absent:
    description:
      - Set state of items not in the compare list to 'absent'
    type: boolean
    default: True
  with_present:
    description:
      - Include items in the original compare list in the output, and set state to 'present'
    type: boolean
    default: True
  warn_on_empty_api:
    description:
      - If the API list is empty, issue an ansible warning and return the empty list.
      - This allows the module to be idempotent.
      - Setting to false will make the lookup error and fail when there is an empty list.
    type: boolean
    default: True
"""

EXAMPLES = """
- name: Get the organization ID
  set_fact:
    controller_organization_id: "{{ lookup('awx.awx.controller_api', 'organizations', query_params={ 'name': 'Default' },
      host=controller_hostname, username=controller_username, password=controller_password, verify_ssl=false) }}"

- name: "Get the API list of all Projects in the Default Organization"
  set_fact:
    controller_api_results: "{{ lookup('awx.awx.controller_api', 'projects', query_params={ 'organization':
      controller_organization_id.id } ,host=controller_hostname, username=controller_username,
      password=controller_password, verify_ssl=false) }}"

- name: "Get the API in a list form. Useful for making sure the results of one item is set to a list."
  set_fact:
    controller_api_results: "{{ query('awx.awx.controller_api', 'inventories', query_params={ 'organization':
      controller_organization_id.id } ,host=controller_hostname, username=controller_username,
      password=controller_password, verify_ssl=false) }}"

- name: "Find the difference of Project between what is on the Controller versus curated list."
  set_fact:
    project_difference: "{{ query('infra.controller_configuration.controller_object_diff',
      api_list=controller_api_results, compare_list=differential_item.differential_test_items,
      with_present=true, set_absent=true) }}"

- name: Add Projects
  include_role:
    name: infra.controller_configuration.projects
  vars:
    controller_projects: "{{ project_difference }}"
"""

RETURN = """
_raw:
  description:
    - Items that are not in the compare list will only return with Name, Organization, and State.
    - When set_absent is true, items that are not in the compare list will be set to absent.
    - When with_present is true items that are not in the compare list with be appended to the compare list.
  type: list
  returned: on successful differential
"""

import copy
from ansible.errors import AnsibleError, AnsibleLookupError
from ansible.module_utils._text import to_native
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display


class LookupModule(LookupBase):
    display = Display()

    def handle_error(self, **kwargs):
        raise AnsibleError(to_native(kwargs.get("msg")))

    def warn_callback(self, warning):
        self.display.warning(warning)

    def create_present_list(self, compare_list):
        if not compare_list and not isinstance(compare_list, list):
            return [compare_list]

        for item in compare_list:
            item.update({"state": "present"})

        return compare_list

    def map_item(self, item, new_attribute_name, attribute_value, dupitems):
        new_item = copy.deepcopy(item)
        for dupitem in [dupitem for dupitem in dupitems if dupitem in new_item]:
            new_item.pop(dupitem)
        new_item.update({new_attribute_name: attribute_value})
        return new_item

    def equal_dicts(self, d1, d2, ignore_keys):
        d1_filtered = {k: v for k, v in d1.items() if k not in ignore_keys}
        d2_filtered = {k: v for k, v in d2.items() if k not in ignore_keys}
        return d1_filtered == d2_filtered

    def run(self, terms, variables=None, **kwargs):
        self.set_options(direct=kwargs)

        # Set Variables for user input
        api_list = self.get_option("api_list")
        compare_list = self.get_option("compare_list")
        warn_on_empty_api = self.get_option("warn_on_empty_api")
        if not api_list:
            if warn_on_empty_api:
                if not compare_list:
                    self._display.warning("Skipping, did not find items in neither api_list nor compare_list")
            else:
                raise AnsibleLookupError("Unable to find items in api_list")
            return self.create_present_list(compare_list)

        # Set Keys to keep for each list. Depending on type
        if api_list[0]["type"] == "organization" or api_list[0]["type"] == "credential_type" or api_list[0]["type"] == "instance_group":
            keys_to_keep = ["name"]
            api_keys_to_keep = ["name"]
        elif api_list[0]["type"] == "user":
            keys_to_keep = ["username"]
            api_keys_to_keep = ["username"]
        elif api_list[0]["type"] == "workflow_job_template_node":
            keys_to_keep = ["workflow_job_template", "unified_job_template", "identifier"]
            api_keys_to_keep = ["identifier", "summary_fields"]
        elif api_list[0]["type"] == "group" or api_list[0]["type"] == "host":
            keys_to_keep = ["name", "inventory"]
            api_keys_to_keep = ["name", "summary_fields"]
        elif api_list[0]["type"] == "schedule":
            keys_to_keep = ["name", "unified_job_template"]
            api_keys_to_keep = ["name", "summary_fields"]
        elif api_list[0]["type"] == "execution_environment":
            keys_to_keep = ["name", "organization", "image"]
            api_keys_to_keep = ["name", "summary_fields", "image"]
        elif api_list[0]["type"] == "role":
            pass
        else:
            keys_to_keep = ["name", "organization"]
            api_keys_to_keep = ["name", "summary_fields"]

            # Depending on type, keep additional keys
            if api_list[0]["type"] == "credential":
                keys_to_keep.append("credential_type")
                api_keys_to_keep.append("credential_type")
            if api_list[0]["type"] == "inventory_source":
                keys_to_keep.append("inventory")
                api_keys_to_keep.append("inventory")

        if api_list[0]["type"] != "role":
            for item in compare_list:
                for key in keys_to_keep:
                    if key not in item.keys():
                        self.handle_error(msg="Key: '{0}' missing from item in compare_list item: {1}".format(key, item))

            for item in api_list:
                for key in api_keys_to_keep:
                    if key not in item.keys():
                        self.handle_error(msg="Key: '{0}' missing from item in api_list. Does this object come from the api? item: {1}".format(key, item))

        # Reduce list to name and organization
        if api_list[0]["type"] == "role":
            compare_list_reduced = copy.deepcopy(compare_list)
            api_list_reduced = copy.deepcopy(api_list)
        elif api_list[0]["type"] == "instance_group":
            compare_list_reduced = [{key: item[key] for key in keys_to_keep} for item in compare_list]
            api_list_reduced = [
                {key: item[key] for key in api_keys_to_keep}
                for item in api_list
                if (item["summary_fields"] and item["summary_fields"]["user_capabilities"]["delete"])
            ]

        else:
            compare_list_reduced = [{key: item[key] for key in keys_to_keep} for item in compare_list]
            api_list_reduced = [{key: item[key] for key in api_keys_to_keep} for item in api_list]

        # Convert summary field name into org name Only if not type organization
        if api_list[0]["type"] == "group" or api_list[0]["type"] == "host":
            for item in api_list_reduced:
                item.update({"inventory": item["summary_fields"]["inventory"]["name"]})
                item.pop("summary_fields")
        elif api_list[0]["type"] == "inventory_source":
            for item in api_list_reduced:
                item.update({"inventory": item["summary_fields"]["inventory"]["name"]})
                item.update({"organization": item["summary_fields"]["organization"]["name"]})
                item.pop("summary_fields")
        elif api_list[0]["type"] == "credential":
            for item in api_list_reduced:
                item.update({"organization": item["summary_fields"]["organization"]["name"] if item["summary_fields"]["organization"] else ""})
                item.update({"credential_type": item["summary_fields"]["credential_type"]["name"]})
                item.pop("summary_fields")
        elif api_list[0]["type"] == "workflow_job_template_node":
            for item in api_list_reduced:
                item.update({"unified_job_template": item["summary_fields"]["unified_job_template"]["name"]})
                item.update({"workflow_job_template": item["summary_fields"]["workflow_job_template"]["name"]})
                item.pop("summary_fields")
        elif api_list[0]["type"] == "schedule":
            for item in api_list_reduced:
                item.update({"unified_job_template": item["summary_fields"]["unified_job_template"]["name"]})
                item.pop("summary_fields")
        elif api_list[0]["type"] == "role":
            for item in api_list_reduced:
                if item["resource_type"] == "organization":
                    item.update({"organizations": [item[item["resource_type"]]]})
                if item["resource_type"] == "instance_group":
                    item.update({"instance_groups": [item[item["resource_type"]]]})
                item.update({"role": item["name"].lower().replace(" ", "_").replace("ad_hoc", "adhoc")})
                # Remove the extra fields
                item.pop("users")
                item.pop("teams")
                item.pop("name")
                item.pop("resource_type")
                if "organization" in item:
                    item.pop("organization")
                if "instance_group" in item:
                    item.pop("instance_group")
                if "type" in item:
                    item.pop("type")
            list_to_extend = []
            list_to_remove = []
            for item in compare_list_reduced:
                expanded = False
                dupitems = [
                    "target_team",
                    "target_teams",
                    "job_template",
                    "job_templates",
                    "workflow",
                    "workflows",
                    "inventory",
                    "inventories",
                    "project",
                    "projects",
                    "credential",
                    "credentials",
                ]
                if "target_team" in item:
                    list_to_extend.append(self.map_item(item, "team", item["target_team"], dupitems))
                    expanded = True
                if "target_teams" in item:
                    for team in item["target_teams"]:
                        list_to_extend.append(self.map_item(item, "team", team, dupitems))
                    expanded = True
                if "job_template" in item:
                    list_to_extend.append(self.map_item(item, "job_template", item["job_template"], dupitems))
                    expanded = True
                if "job_templates" in item:
                    for job_template in item["job_templates"]:
                        list_to_extend.append(self.map_item(item, "job_template", job_template, dupitems))
                    expanded = True
                if "workflow" in item:
                    list_to_extend.append(self.map_item(item, "workflow_job_template", item["workflow"], dupitems))
                    expanded = True
                if "workflows" in item:
                    for workflow in item["workflows"]:
                        list_to_extend.append(self.map_item(item, "workflow_job_template", workflow, dupitems))
                    expanded = True
                if "inventory" in item:
                    list_to_extend.append(self.map_item(item, "inventory", item["inventory"], dupitems))
                    expanded = True
                if "inventories" in item:
                    for inventory in item["inventories"]:
                        list_to_extend.append(self.map_item(item, "inventory", inventory, dupitems))
                    expanded = True
                if "project" in item:
                    list_to_extend.append(self.map_item(item, "project", item["project"], dupitems))
                    expanded = True
                if "projects" in item:
                    for project in item["projects"]:
                        list_to_extend.append(self.map_item(item, "project", project, dupitems))
                    expanded = True
                if expanded:
                    list_to_remove.append(item)
            for item in list_to_remove:
                compare_list_reduced.remove(item)
            compare_list_reduced.extend(list_to_extend)
            # Expand all compare list elements when roles is provided as list
            list_to_extend.clear()
            list_to_remove.clear()
            for item in compare_list_reduced:
                expanded = False
                dupitems = ["roles", "role"]
                if "roles" in item:
                    for role in item["roles"]:
                        list_to_extend.append(self.map_item(item, "role", role, dupitems))
                    expanded = True
                if expanded:
                    list_to_remove.append(item)
            for item in list_to_remove:
                compare_list_reduced.remove(item)
            compare_list_reduced.extend(list_to_extend)
        elif (
            api_list[0]["type"] != "organization"
            and api_list[0]["type"] != "user"
            and api_list[0]["type"] != "credential_type"
            and api_list[0]["type"] != "schedule"
            and api_list[0]["type"] != "instance_group"
        ):
            for item in api_list_reduced:
                item.update({"organization": item["summary_fields"]["organization"]["name"]})
                item.pop("summary_fields")

        self.display.v("compare_list_reduced: {0}".format(compare_list_reduced))
        self.display.v("api_list_reduced: {0}".format(api_list_reduced))

        # Find difference between lists
        if api_list[0]["type"] != "role":
            difference = [i for i in api_list_reduced if i not in compare_list_reduced]
        else:
            difference = []
            for item in api_list_reduced:
                for compare_item in compare_list_reduced:
                    if self.equal_dicts(compare_item, item, "state"):
                        break
                    elif (
                        ("organization" in compare_item)  # permission applies to all objects in orga
                        and (len(compare_item) == 3)  # we only have orga, team/user, and role
                        and self.equal_dicts(compare_item, item, ["organization"] + list(item.keys() - compare_item.keys()))
                    ):
                        break
                else:
                    difference.append(item)

        # Set
        if self.get_option("set_absent"):
            for item in difference:
                item.update({"state": "absent"})
                if "team" in item and item["role"] == "member":
                    item.update({"target_team": item["team"]})
                    item.pop("team")

        # Combine Lists
        if self.get_option("with_present"):
            for item in compare_list:
                item.update({"state": "present"})
            compare_list.extend(difference)
            # Return Compare list with difference attached
            difference = compare_list

        if api_list[0]["type"] == "role":
            difference_to_remove = []
            for item in difference:
                if "no_resource_type" in item or len(item) <= 3:
                    difference_to_remove.append(item)
            for item in difference_to_remove:
                difference.remove(item)

        return [difference]
