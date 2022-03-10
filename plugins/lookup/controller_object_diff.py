# (c) 2020 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
lookup: controller_object_diff
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
    required: True
  compare_list:
    description:
      - The list of objects to compare the api_list to.
    type: list
    required: True
  set_absent:
    description:
      - Set items not in the compare list to state: absent
    type: boolean
    default: True
  with_present:
    description:
      - Include items in the original compare list in the output, and set state: present
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

- name: "Get the API in a list form. Useful for making sure the results of one item is set to a list.
  set_fact:
    controller_api_results: "{{ query('awx.awx.controller_api', 'inventories', query_params={ 'organization':
      controller_organization_id.id } ,host=controller_hostname, username=controller_username,
      password=controller_password, verify_ssl=false) }}"

- name: "Find the difference of Project between what is on the Controller versus curated list."
  set_fact:
    project_difference: "{{ lookup('redhat_cop.controller_configuration.controller_object_diff',
      api_list=controller_api_results, compare_list=differential_item.differential_test_items,
      with_present=true, set_absent=true ) }}"

- name: Add Projects
  include_role:
    name: redhat_cop.controller_configuration.projects
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

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError, AnsibleLookupError
from ansible.module_utils._text import to_native
from ansible.utils.display import Display


class LookupModule(LookupBase):
    display = Display()

    def handle_error(self, **kwargs):
        raise AnsibleError(to_native(kwargs.get("msg")))

    def warn_callback(self, warning):
        self.display.warning(warning)

    def run(self, terms, variables=None, **kwargs):
        self.set_options(direct=kwargs)

        # Set Variables for user input
        api_list = self.get_option("api_list")
        compare_list = self.get_option("compare_list")
        warn_on_empty_api = self.get_option("warn_on_empty_api")
        if not api_list:
            if warn_on_empty_api:
                self._display.warning("Skipping, did not find items in api_list")
            else:
                raise AnsibleLookupError("Unable to find items in api_list")
            return [api_list]

        # Set Keys to keep for each list. Depending on type
        if api_list[0]["type"] == "organization":
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

        for item in compare_list:
            for key in keys_to_keep:
                if key not in item.keys():
                    self.handle_error(msg="Key: '{0}' missing from item in compare_list item: {1}".format(key, item))

        for item in api_list:
            for key in api_keys_to_keep:
                if key not in item.keys():
                    self.handle_error(msg="Key: '{0}' missing from item in api_list. Does this object come from the api? item: {1}".format(key, item))

        # Reduce list to name and organization
        compare_list_reduced = [{key: item[key] for key in keys_to_keep} for item in compare_list]
        api_list_reduced = [{key: item[key] for key in api_keys_to_keep} for item in api_list]

        # Convert summary field name into org name Only if not type organization
        if api_list[0]["type"] == "group" or api_list[0]["type"] == "host":
            for item in api_list_reduced:
                item.update({"inventory": item["summary_fields"]["inventory"]["name"]})
                item.pop("summary_fields")
        elif api_list[0]["type"] == "credential":
            for item in api_list_reduced:
                item.update({"organization": item["summary_fields"]["organization"]["name"]})
                item.update({"credential_type": item["summary_fields"]["credential_type"]["name"]})
                item.pop("summary_fields")
        elif api_list[0]["type"] == "workflow_job_template_node":
            for item in api_list_reduced:
                item.update({"unified_job_template": item["summary_fields"]["unified_job_template"]["name"]})
                item.update({"workflow_job_template": item["summary_fields"]["workflow_job_template"]["name"]})
                item.pop("summary_fields")
        elif api_list[0]["type"] != "organization" and api_list[0]["type"] != "user":
            for item in api_list_reduced:
                item.update({"organization": item["summary_fields"]["organization"]["name"]})
                item.pop("summary_fields")

        self.display.warning("compare_list_reduced: {0}".format(compare_list_reduced))
        self.display.warning("api_list_reduced: {0}".format(api_list_reduced))

        # Find difference between lists
        difference = [i for i in api_list_reduced if i not in compare_list_reduced]

        # Set
        if self.get_option("set_absent"):
            for item in difference:
                item.update({"state": "absent"})
        # Combine Lists
        if self.get_option("with_present"):
            for item in compare_list_reduced:
                item.update({"state": "present"})
            compare_list.extend(difference)
            # Return Compare list with difference attached
            difference = compare_list

        return [difference]
