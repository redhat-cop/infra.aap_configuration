# Copyright: (c) 2021, Herve Quatremain <hquatrem@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# You can consult the UI API documentation directly on a running Ansible
# automation hub at https://hub.example.com/pulp/api/v3/docs/
#
# Ansible Automation Hub UI project at https://github.com/ansible/ansible-hub-ui

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from .ah_module import AHModule
from ansible.module_utils.six.moves.urllib.parse import urlencode


class AHUIAPIModule(AHModule):
    """Manage the Ansible automation hub UI API."""

    def __init__(self, argument_spec, supports_check_mode=False):
        """Initialize the module."""
        super(AHUIAPIModule, self).__init__(
            argument_spec=argument_spec, supports_check_mode=supports_check_mode
        )
        # The API endpoint is the last component of the URL and allows access
        # to the object API:
        #   https://hub.example.com/api/galaxy/_ui/v1/<endpoint>/
        # Examples:
        #   https://hub.example.com/api/galaxy/_ui/v1/groups/ (endpoint=groups)
        #   https://hub.example.com/api/galaxy/_ui/v1/users/ (endpoint=users)
        self.endpoint = None

        # Type of the objects manage by the class. This is only used in the
        # messages returned to the user.
        self.object_type = "object"

        # In the JSON API response message, self.name_field is the name of the
        # attribute that stores the object name. This is also used as the query
        # parameter in GET requests (https://..../users/?username=jdoe)
        self.name_field = "name"

        # In the JSON API response message, self.id_field is the name of the
        # attribute that stores the object ID. That ID is used with DELETE, PUT,
        # and POST resquests (https://.../users/<ID>/)
        self.id_field = "id"

        # URL base path for all the API calls.
        self.url_base_path = "/api/{0}/_ui/v1/".format(self.path_prefix)

        # Is the class instance has been initialized with a valid object?
        self.exists = False

        # JSON data returned by the last API call. This typically stores the
        # object details ({ "username": "jdoe", "last_name": "Doe", ...})
        self.data = {}

    @property
    def id(self):
        """Return the object ID."""
        if self.id_field in self.data:
            return self.data[self.id_field]
        return None

    @property
    def name(self):
        """Return the object name."""
        if self.name_field in self.data:
            return self.data[self.name_field]
        return None

    def build_url(self, endpoint, query_params=None):
        """Construct and return a URL object.

        :param endpoint: The API endpoint. That endpoint is the last directory
                         part in the API URL. For example:
                         https://.../api/galaxy/_ui/v1/<endpoint>/
        :type endpoint: str
        :param query_params: URL query string.
        :type query_params: str

        :return: The URL object.
        :rtype: :class:`urllib.parse.ParseResult`
        """
        # self.id is only defined once the object has been retrieved (GET).
        # In that case, the returned URL points the the API endpoint that can
        # be used to manage the object (used by PUT, POST, DELETE)
        if self.id is not None:
            url_path = "{base}{endpoint}/{id}/".format(
                base=self.url_base_path, endpoint=endpoint.strip("/"), id=self.id
            )
        else:
            url_path = "{base}{endpoint}/".format(
                base=self.url_base_path, endpoint=endpoint.strip("/")
            )
        url = self.url._replace(path=url_path)
        if query_params:
            url = url._replace(query=urlencode(query_params))
        return url

    def extract_error_msg(self, response):
        """Return the error message provided in the API response.

        Example of messages returned by the API call:

            {
                "errors": [
                    {
                        "status":"400",
                        "code":"invalid",
                        "title":"Invalid input.",
                        "detail":"Permission matching query does not exist."
                    }
                ]
            }

            {
                "errors": [
                    {
                        "status":"404",
                        "code":"not_found",
                        "title":"Not found."
                    }
                ]
            }

        :param response: The response message from the API.
        :type response: dict

        :return: The error message or an empty string if the reponse does not
                 provide a message.
        :rtype: str
        """
        # {"errors":[{"status":"400","code":"invalid","title":"Invalid input.","detail":"Permission matching query does not exist."}]}
        # {"errors":[{"status":"404","code":"not_found","title":"Not found."}]}
        if (
            response
            and "json" in response
            and "errors" in response["json"]
            and len(response["json"]["errors"])
        ):
            if "detail" in response["json"]["errors"][0]:
                return response["json"]["errors"][0]["detail"]
            if "title" in response["json"]["errors"][0]:
                return response["json"]["errors"][0]["title"]
        return ""

    def get_one_object(self, endpoint, name, name_field="name", object_type="object "):
        """Retrieve and return a single object from a GET API call.

        :param endpoint: The API endpoint. That endpoint is the last directory
                         part in the API URL. For example:
                         https://.../api/galaxy/_ui/v1/<endpoint>/
        :type endpoint: str
        :param name: Name of the object to retrieve.
        :type name: str
        :param name_field: Name of the query parameter. For example,
                           https://.../users/?username=jdoe
                           (name_field=username))
        :type name_field: str
        :param object_type: Type of the object (user, group, ...). This is only
                            used in the messages returned to the user.

        :return: The retrieved object.
        :rtype: dict or None
        """
        query = {"data": {name_field: name}}
        response = self.get_endpoint(endpoint, **query)
        if response["status_code"] != 200:
            error_msg = self.extract_error_msg(response)
            if error_msg:
                fail_msg = "Unable to get {0} {1}: {2}: {3}".format(
                    object_type, name, response["status_code"], error_msg
                )
            else:
                fail_msg = "Unable to get {0} {1}: {2}".format(
                    object_type, name, response["status_code"]
                )
            self.fail_json(msg=fail_msg)

        if "count" not in response["json"]["meta"] or "data" not in response["json"]:
            self.fail_json(
                msg="Unable to get {0} {1}: the endpoint did not provide count and results".format(
                    object_type, name
                )
            )

        if response["json"]["meta"]["count"] == 0:
            return None

        if response["json"]["meta"]["count"] > 1:
            # Only one object should be returned. If more that one is returned,
            # then look for the requested name in the returned list.
            for asset in response["json"]["data"]:
                if name_field in asset and asset[name_field] == name:
                    return asset
            self.fail_wanted_one(response, endpoint, query["data"])

        return response["json"]["data"][0]

    def get_one(self, name):
        """Retrieve the object through a GET API call.

        The retrieved object is store in self.data so that othe API calls that
        need the object ID can get it from there (DELETE, POST, and PUT)

        :param name: Name of the object to retrieve.
        :type name: str

        :return: True when the object as been retrieved or False when the object
                 does not exist.
        :rtype: bool
        """
        response = self.get_one_object(
            self.endpoint, name, self.name_field, self.object_type
        )
        if response is None:
            self.exists = False
            self.data = {}
            return False

        self.exists = True
        self.data = response
        return True

    def delete(self, auto_exit=True):
        """Perform an DELETE API call to delete the object.

        :param auto_exit: Exit the module when the API call is done.
        :type auto_exit: bool
        """
        if not self.exists:
            self.json_output["changed"] = False
            if auto_exit:
                self.exit_json(**self.json_output)
            return

        response = self.delete_endpoint(self.endpoint)

        if response["status_code"] in [202, 204]:
            if self.name:
                self.json_output["name"] = self.name
            self.json_output["id"] = self.id
            self.json_output["type"] = self.object_type
            self.json_output["changed"] = True
            if auto_exit:
                self.exit_json(**self.json_output)
            return

        error_msg = self.extract_error_msg(response)
        if error_msg:
            self.fail_json(
                msg="Unable to delete {0} {1}: {2}".format(
                    self.object_type,
                    self.name,
                    error_msg,
                )
            )
        self.fail_json(
            msg="Unable to delete {0} {1}: {2}".format(
                self.object_type, self.name, response["status_code"]
            )
        )

    def create_or_update(self, new_item, auto_exit=True):
        """Create or update the current object in Ansible automation hub.

        :param new_item: Tha data to pass to the API call. This provides the
                         object details ({"username": "jdoe", ...} for example)
        :type new_item: dict
        :param auto_exit: Exit the module when the API call is done.
        :type auto_exit: bool
        """
        if self.exists:
            self.update(new_item, auto_exit)
        else:
            self.create(new_item, auto_exit)

    def update(self, new_item, auto_exit=True):
        """Update the existing object in Ansible automation hub.

        :param new_item: Tha data to pass to the API call. This provides the
                         object details ({"username": "jdoe", ...} for example)
        :type new_item: dict
        :param auto_exit: Exit the module when the API call is done.
        :type auto_exit: bool
        """
        # The "key" field ("name", "username", ...) is required for PUT
        # requests. Making sure that it is present.
        if self.name_field not in new_item:
            new_item[self.name_field] = self.name

        # Check to see if anything within the item requires the item to be
        # updated.
        needs_patch = self.objects_could_be_different(self.data, new_item)

        if not needs_patch:
            if self.name:
                self.json_output["name"] = self.name
            self.json_output["id"] = self.id
            self.json_output["changed"] = False
            if auto_exit:
                self.exit_json(**self.json_output)
            return

        response = self.put_endpoint(self.endpoint, **{"data": new_item})

        if response["status_code"] == 200:
            self.exists = True
            self.data = response["json"]
            if self.name:
                self.json_output["name"] = self.name
            self.json_output["id"] = self.id
            self.json_output["type"] = self.object_type
            self.json_output["changed"] = True
            if auto_exit:
                self.exit_json(**self.json_output)
            return

        error_msg = self.extract_error_msg(response)
        if error_msg:
            self.fail_json(
                msg="Unable to update {0} {1}: {2}".format(
                    self.object_type,
                    self.name,
                    error_msg,
                )
            )
        self.fail_json(
            msg="Unable to update {0} {1}: {2}".format(
                self.object_type, self.name, response["status_code"]
            )
        )

    def create(self, new_item, auto_exit=True):
        """Perform an POST API call to create a new object.

        :param new_item: Tha data to pass to the API call. This provides the
                         object details ({"username": "jdoe", ...} for example)
        :type new_item: dict
        :param auto_exit: Exit the module when the API call is done.
        :type auto_exit: bool
        """
        response = self.post_endpoint(self.endpoint, **{"data": new_item})

        if response["status_code"] in [200, 201]:
            self.exists = True
            self.data = response["json"]
            if self.name:
                self.json_output["name"] = self.name
            self.json_output["id"] = self.id
            self.json_output["type"] = self.object_type
            self.json_output["changed"] = True
            if auto_exit:
                self.exit_json(**self.json_output)
            return

        error_msg = self.extract_error_msg(response)
        if error_msg:
            self.fail_json(
                msg="Unable to create {0} {1}: {2}".format(
                    self.object_type,
                    self.name,
                    error_msg,
                )
            )
        self.fail_json(
            msg="Unable to create {0} {1}: {2}".format(
                self.object_type, self.name, response["status_code"]
            )
        )


class AHUser(AHUIAPIModule):
    """Manage the Ansible automation hub UI user API."""

    def __init__(self, argument_spec, supports_check_mode=False):
        """Initialize the module."""
        super(AHUser, self).__init__(
            argument_spec=argument_spec, supports_check_mode=supports_check_mode
        )
        self.endpoint = "users"
        self.name_field = "username"
        self.object_type = "user"

        # API attributes that store a password. This is used to display a
        # warning message to the user when they update a password (changed
        # status always true because we don't get the previous password to
        # compare)
        self.password_fields = ["password"]

    @property
    def groups(self):
        """Return the groups for which the user is a member."""
        if "groups" in self.data:
            return self.data["groups"]
        return []

    @property
    def superuser(self):
        """Tell if the user is a super user or not."""
        if "is_superuser" in self.data:
            return self.boolean(self.data["is_superuser"])
        return False

    def _isequal_list(self, old, new, key="id"):
        """Compare two lists and tell is they are equal or not.

        If the items in the lists are dictionaries, then the attribute provided
        by the `key` parameters is used for comparing the lists.

        :param old: The first list.
        :type old: list
        :param new: The second list.
        :type new: list
        :param key: When the items in the lists are dictionaries, use that key
                    for comparing the items.
        :type key: str

        :return: True is the two lists are identical and False otherwise.
        :rtype: bool
        """
        if len(new) != len(old):
            return False
        if len(new) == 0:
            return True
        if isinstance(new[0], dict):
            new_items = set([k[key] for k in new if key in k])
            old_items = set([k[key] for k in old if key in k])
        else:
            new_items = set(new)
            old_items = set(old)
        return new_items == old_items

    def objects_could_be_different(self, old, new, warning=True):
        """Tell if the new dictionary is a subset of the old one.

        This method is used to decide if the object must be updated (PUT) or
        not. If no new attribute, or no attribute change, then no need to
        call the API.

        :param old: The old object parameters
        :type old: dict
        :param new: The new object parameters.
        :type new: dict

        :return: True is the new dictionary contains items not in the old one.
                 False otherwise.
        :rtype: bool
        """
        for k in new.keys():
            if k in self.password_fields:
                if warning:
                    self.warn(
                        "The field {0} of {1} {2} has encrypted data and may inaccurately report task is changed.".format(
                            k, self.object_type, self.name
                        )
                    )
                return True

            if k not in old:
                return True
            new_field = new[k]
            old_field = old[k]
            if isinstance(new_field, list) and isinstance(old_field, list):
                if not self._isequal_list(old_field, new_field):
                    return True
                continue

            if old_field != new_field:
                return True
        return False


class AHGroup(AHUIAPIModule):
    """Manage the Ansible automation hub UI group API."""

    def __init__(self, argument_spec, supports_check_mode=False):
        """Initialize the object."""
        super(AHGroup, self).__init__(
            argument_spec=argument_spec, supports_check_mode=supports_check_mode
        )
        self.endpoint = "groups"
        self.name_field = "name"
        self.object_type = "group"


class AHPerm(AHUIAPIModule):
    """Manage the Ansible automation hub UI group permission API.

    The group permission API uses a "nested" endpoint under the "groups"
    endpoint:

        https://.../api/galaxy/_ui/v1/groups/<GR_ID#>/model-permissions/<PERM_ID#>/

    When using that class, first call the :func:`get_group_perms` method. That
    method:

    * retrieves the group object (GET /api/galaxy/_ui/v1/groups/?name=<name>)
      and sets self.group_id with the group's ID. Once that ID has been
      retrieved, the URL to access the group permissions can be built.
    * retrieves the permissions (GET /api/galaxy/_ui/v1/groups/<GR_ID#>/model-permissions/)
      and stores them in self.perms. That dictionary maps each permission with
      its ID.
    """

    def __init__(self, argument_spec, supports_check_mode=False):
        """Initialize the object."""
        super(AHPerm, self).__init__(
            argument_spec=argument_spec, supports_check_mode=supports_check_mode
        )
        # The group permission API uses a "nested" endpoint under the "groups"
        # endpoint:
        #   https://.../api/galaxy/_ui/v1/groups/<GR_ID#>/model-permissions/<PERM_ID#>/
        #
        self.endpoint = "groups"
        self.nested_endpoint = "model-permissions"
        self.name_field = "permission"
        self.object_type = "permission"
        self.group_id = None
        self.perm_id = None
        self.perms = {}
        self.exists = True

    def build_url(self, endpoint, query_params=None):
        """Construct and return a URL object.

        This method is invoked during each API call. It relies on the preceding
        calls to build the URL from the already retrieved IDs.

        :param endpoint: The API endpoint. That endpoint is a directory
                         part in the API URL. For example:
                         https://.../api/galaxy/_ui/v1/<endpoint>/
        :type endpoint: str
        :param query_params: URL query string.
        :type query_params: str

        :return: The URL object.
        :rtype: :class:`urllib.parse.ParseResult`
        """
        # If the group ID and the permission ID are already kwown, then build
        # a URL to access that specifig permsission for the group.
        # /api/galaxy/_ui/v1/groups/<GR_ID#>/model-permissions/<PERM_ID#>/
        if self.group_id is not None and self.perm_id is not None:
            url_path = "{base}{endpoint}/{grid}/{nestedendpoint}/{id}/".format(
                base=self.url_base_path,
                endpoint=endpoint.strip("/"),
                grid=self.group_id,
                nestedendpoint=self.nested_endpoint.strip("/"),
                id=self.perm_id,
            )
        # If only the group ID is known at that point, then prepare a URL to
        # list its permissions.
        # /api/galaxy/_ui/v1/groups/<GR_ID#>/model-permissions/ (GET)
        elif self.group_id is not None:
            url_path = "{base}{endpoint}/{grid}/{nestedendpoint}/".format(
                base=self.url_base_path,
                endpoint=endpoint.strip("/"),
                grid=self.group_id,
                nestedendpoint=self.nested_endpoint.strip("/"),
            )
        # If the group ID is not yet available, then build a URL to access the
        # "groups" endpoint (where the group can be retrieved)
        else:
            url_path = "{base}{endpoint}/".format(
                base=self.url_base_path, endpoint=endpoint.strip("/")
            )
        url = self.url._replace(path=url_path)
        if query_params:
            url = url._replace(query=urlencode(query_params))
        return url

    def get_group_perms(self, name):
        """Retrieve the group details and its permissions.

        :return: The dictionary that maps the permission names with their IDs.
        :rtype: dict
        """
        # Retrieve the group first
        group = self.get_one_object("groups", name)
        if group is None:
            self.fail_json(msg="unknown group: %s" % name)
        self.group_id = group["id"]

        # Then retrieve the permissions for the group.
        # Set the limit to 100 to make sure to retrieve all the group's
        # permissions in one page.
        response = self.get_endpoint("groups", data={"limit": 100})
        self.perms = {}
        if (
            response
            and "json" in response
            and "meta" in response["json"]
            and "count" in response["json"]["meta"]
            and response["json"]["meta"]["count"] > 0
            and "data" in response["json"]
        ):
            for r in response["json"]["data"]:
                self.perms[r["permission"]] = r["id"]
        return self.perms

    def delete_perms(self, perms_to_delete):
        """Remove permission from the group.

        The method exits the module.

        :param perms_to_delete: List of the permission names to remove from the
                                group.
        :type perms_to_delete: list
        """
        if perms_to_delete is not None and len(perms_to_delete) > 0:
            for p in perms_to_delete:
                self.perm_id = self.perms[p]
                self.delete(auto_exit=False)
            self.exit_json(changed=True)
        self.exit_json(changed=False)

    def create_perms(self, perms_to_create):
        """Add a permission to the group.

        The method exits the module.

        :param perms_to_create: List of the permission names to add to the
                                group.
        :type perms_to_delete: list
        """
        if perms_to_create is not None and len(perms_to_create) > 0:
            for p in perms_to_create:
                self.create({"permission": p}, auto_exit=False)
            self.exit_json(changed=True)
        self.exit_json(changed=False)
