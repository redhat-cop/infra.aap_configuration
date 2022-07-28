# (c) 2020 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
lookup: ah_api
author: Tom Page (@Tompage1994)
short_description: Search the API for objects
requirements:
  - None
description:
  - Returns GET requests from the Automation Hub or GalaxyNG API.
options:
  _terms:
    description:
      - The endpoint to query.
    choices:
      - "'ee_images', [ee_image_repository_name]"
      - "'ee_namespaces'"
      - "'ee_registries'"
      - "'ee_repositories'"
      - "'collections'"
      - "'collection', [repository={published, rh_certified, community}], [collection_namespace], [collection_name]"
      - "'groups'"
      - "'namespaces'"
      - "'repository_community'"
      - "'repository_rh_certified'"
      - "'users'"
    required: True
  query_params:
    description:
      - The query parameters to search for in the form of key/value pairs.
    type: dict
    required: False
    aliases: [query, data, filter, params]
  expect_objects:
    description:
      - Error if the response does not contain either a detail view or a list view.
    type: boolean
    default: False
    aliases: [expect_object]
  expect_one:
    description:
      - Error if the response contains more than one object.
    type: boolean
    default: False
  return_objects:
    description:
      - If a list view is returned, promote the list of data to the top-level of list returned.
      - Allows using this lookup plugin to loop over objects without additional work.
    type: boolean
    default: True
  return_all:
    description:
      - If the response is paginated, return all pages.
    type: boolean
    default: False
  return_ids:
    description:
      - If response contains objects, promote the id key to the top-level entries in the list.
      - Allows looking up a related object and passing it as a parameter to another module.
      - This will convert the return to a string or list of strings depending on the number of selected items.
    type: boolean
    aliases: [return_id]
    default: False
  max_objects:
    description:
      - if C(return_all) is true, this is the maximum of number of objects to return from the list.
      - If a list view returns more an max_objects an exception will be raised
    type: integer
    default: 1000
extends_documentation_fragment: redhat_cop.ah_configuration.auth_plugin
notes:
  - If the query is not filtered properly this can cause a performance impact.
  - Two options take multiple terms. 'ee_images' and 'collection'. See the _terms choices above or the examples below for more details.
"""

EXAMPLES = """
- name: Report the usernames of all users
  debug:
    msg: "Users: {{ query('redhat_cop.ah_configuration.ah_api', 'users', return_all=true) | map(attribute='username') | list }}"

- name: List all collection namespaces by the devops team
  debug:
    msg: "{{ lookup('redhat_cop.ah_configuration.ah_api', 'namespaces', host='https://ah.example.com', username='ansible',
              password='Passw0rd123', verify_ssl=false, query_params={'company': 'Devops'}) }}"

- name: Get the list of tags for my_ee
  set_fact:
    my_ee_tags: "{{ lookup('redhat_cop.ah_configuration.ah_api', 'ee_images', 'my_ee') | map(attribute='tags') | list | flatten }}"

- name: Get the list of versions for redhat_cop.ah_configuration in the published repo
  set_fact:
    collection_versions: "{{ lookup('redhat_cop.ah_configuration.ah_api', 'collection', 'published', 'redhat_cop',
                            'ah_configuration').all_versions | map(attribute='version') | list }}"
"""

RETURN = """
_raw:
  description:
    - Response from the API
  type: dict
  returned: on successful request
"""

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError
from ansible.module_utils._text import to_native
from ansible.utils.display import Display
from ..module_utils.ah_api_module import AHAPIModule


display = Display()


class LookupModule(LookupBase):
    def handle_error(self, **kwargs):
        raise AnsibleError(to_native(kwargs.get("msg")))

    def warn_callback(self, warning):
        self.display.warning(warning)

    def run(self, terms, variables=None, **kwargs):
        self.set_options(direct=kwargs)

        # Defer processing of params to logic shared with the modules
        module_params = {}
        for plugin_param, module_param in AHAPIModule.short_params.items():
            opt_val = self.get_option(plugin_param)
            if opt_val is not None:
                module_params[module_param] = opt_val

        # Create our module
        module = AHAPIModule(argument_spec={}, direct_params=module_params, error_callback=self.handle_error, warn_callback=self.warn_callback)

        endpoints = {
            "ee_images": "/api/{prefix}/_ui/v1/execution-environments/repositories/{ee_repository}/_content/images/",
            "ee_namespaces": "/pulp/api/v3/pulp_container/namespaces/",
            "ee_registries": "/api/{prefix}/_ui/v1/registry/",
            "ee_repositories": "/api/{prefix}/_ui/v1/execution-environments/repositories/",
            "collections": "/api/{prefix}/v3/collections/",
            "collection": "/api/{prefix}/_ui/v1/repo/{repository}/{namespace}/{name}",
            "groups": "/api/{prefix}/_ui/v1/groups/",
            "namespaces": "/api/{prefix}/v3/namespaces/",
            "repository_community": "/api/{prefix}/content/community/v3/sync/config/",
            "repository_rh_certified": "/api/{prefix}/content/rh-certified/v3/sync/config/",
            "users": "/api/{prefix}/_ui/v1/users/",
        }

        if terms[0] not in endpoints:
            raise AnsibleError("{0} is not a valid endpoint to query. See the full list of choices in the plugin documentation".format(terms[0]))

        if terms[0] == "ee_images":
            if len(terms) != 2:
                raise AnsibleError("A second term for the name of the ee repository is required")
            endpoint = endpoints[terms[0]].format(prefix=module.path_prefix, ee_repository=terms[1])
        elif terms[0] == "collection":
            if len(terms) != 4:
                raise AnsibleError("4 terms are required with: 'collection', <repository>, <namespace>, <name>")
            endpoint = endpoints[terms[0]].format(prefix=module.path_prefix, repository=terms[1], namespace=terms[2], name=terms[3])
        else:
            endpoint = endpoints[terms[0]].format(prefix=module.path_prefix)

        url = module._build_url("", endpoint=endpoint, query_params=self.get_option("query_params", {}))

        module.authenticate()
        response = module.make_request("GET", url)

        if "status_code" not in response:
            raise AnsibleError("Unclear response from API: {0}".format(response))

        if response["status_code"] != 200:
            raise AnsibleError("Failed to query the API: {0}".format(response["json"].get("detail", response["json"])))

        return_data = response["json"]

        if endpoint.startswith("/api/"):
            if self.get_option("expect_objects") or self.get_option("expect_one"):
                if ("id" not in return_data) and ("data" not in return_data):
                    raise AnsibleError("Did not obtain a list or detail view at {0}, and " "expect_objects or expect_one is set to True".format(terms[0]))

            if self.get_option("expect_one"):
                if "data" in return_data and len(return_data["data"]) != 1:
                    raise AnsibleError("Expected one object from endpoint {0}, " "but obtained {1} from API".format(terms[0], len(return_data["data"])))

            if self.get_option("return_all") and "data" in return_data:
                if return_data["meta"]["count"] > self.get_option("max_objects"):
                    raise AnsibleError(
                        "List view at {0} returned {1} objects, which is more than the maximum allowed "
                        "by max_objects, {2}".format(terms[0], return_data["meta"]["count"], self.get_option("max_objects"))
                    )

                next_page = module._build_url("", endpoint=return_data["links"]["next"])
                while return_data["links"]["next"] is not None:
                    next_response = module.make_request("GET", next_page)
                    return_data["data"] += next_response["json"]["data"]
                    if next_response["json"]["links"]["next"] is not None:
                        next_page = module._build_url("", endpoint=next_response["json"]["links"]["next"])
                    else:
                        break
                return_data["links"]["next"] = None

            if self.get_option("return_ids"):
                if "data" in return_data:
                    return_data["data"] = [str(item["id"]) for item in return_data["data"]]
                elif "id" in return_data:
                    return_data = str(return_data["id"])

            if self.get_option("return_objects") and "data" in return_data:
                return [return_data["data"]]
            else:
                return [return_data]

        elif endpoint.startswith("/pulp/"):
            if self.get_option("expect_objects") or self.get_option("expect_one"):
                if ("id" not in return_data) and ("results" not in return_data):
                    raise AnsibleError("Did not obtain a list or detail view at {0}, and " "expect_objects or expect_one is set to True".format(terms[0]))

            if self.get_option("expect_one"):
                if "results" in return_data and len(return_data["results"]) != 1:
                    raise AnsibleError("Expected one object from endpoint {0}, " "but obtained {1} from API".format(terms[0], len(return_data["results"])))

            if self.get_option("return_all") and "results" in return_data:
                if return_data["count"] > self.get_option("max_objects"):
                    raise AnsibleError(
                        "List view at {0} returned {1} objects, which is more than the maximum allowed "
                        "by max_objects, {2}".format(terms[0], return_data["count"], self.get_option("max_objects"))
                    )

                next_page = module.host_url._replace(path=return_data["next"])
                while return_data["next"] is not None:
                    next_response = module.make_request("GET", next_page)
                    return_data["results"] += next_response["json"]["results"]
                    if next_response["json"]["next"] is not None:
                        next_page = module._build_url("", endpoint=next_response["json"]["next"])
                    else:
                        break
                return_data["next"] = None

            if self.get_option("return_ids"):
                if "results" in return_data:
                    return_data["results"] = [str(item["id"]) for item in return_data["results"]]
                elif "id" in return_data:
                    return_data = str(return_data["id"])

            if self.get_option("return_objects") and "results" in return_data:
                return [return_data["results"]]
            else:
                return [return_data]
        else:
            return [return_data]
