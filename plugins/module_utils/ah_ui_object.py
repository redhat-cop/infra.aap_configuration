# Copyright: (c) 2021, Herve Quatremain <hquatrem@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# You can consult the UI API documentation directly on a running private
# automation hub at https://hub.example.com/pulp/api/v3/docs/
#
# Ansible Automation Hub UI project at https://github.com/ansible/ansible-hub-ui

from __future__ import absolute_import, division, print_function
import time

from .ah_api_module import AHAPIModuleError
from .ah_pulp_object import AHPulpTask

__metaclass__ = type


class AHUIObject(object):
    """Manage API objects.

    Create a subclass of :py:class:``AHUIObject`` to represent a specific type
    of object (user, group, ...)

    :param API_object: Module object to use to access the private automation hub API.
    :type API_object: :py:class:``AHAPIModule``
    :param data: Initial data
    :type data: dict
    """

    def __init__(self, API_object, data={}):
        """Initialize the module."""
        # The API endpoint is the last component of the URL and allows access
        # to the object API:
        #   https://hub.example.com/api/galaxy/_ui/v1/<endpoint>/
        # Examples:
        #   https://hub.example.com/api/galaxy/_ui/v1/groups/ (endpoint=groups)
        #   https://hub.example.com/api/galaxy/_ui/v1/users/ (endpoint=users)
        self.endpoint = None

        # Type of the objects managed by the class. This is only used in the
        # messages returned to the user.
        self.object_type = "object"

        # In the JSON API response message, self.name_field is the name of the
        # attribute that stores the object name. This is also used as the query
        # parameter in GET requests (https://..../groups/?name=operators)
        self.name_field = "name"

        # In the JSON API response message, self.id_field is the name of the
        # attribute that stores the object ID. That ID is used with DELETE, PUT,
        # and POST resquests (https://.../users/<ID>/)
        self.id_field = "id"

        # API attributes that store a password. This is used to display a
        # warning message to the user when they update a password (changed
        # status always True because we don't get the previous password to
        # compare)
        self.password_fields = ["password"]

        # JSON data returned by the last API call. This typically stores the
        # object details ({ "username": "jdoe", "last_name": "Doe", ...})
        self.data = data

        # Is the class instance has been initialized with a valid object?
        self.exists = True if data else False

        # The AHAPIModule class object that is used to access the API
        self.api = API_object

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

    @property
    def id_endpoint(self):
        """Return the object's endpoint."""
        id = self.id
        if id is None:
            return self.endpoint
        return "{endpoint}/{id}".format(endpoint=self.endpoint, id=id)

    def _isequal_list(self, old, new, key="id"):
        """Compare two lists and tell is they are equal or not.

        If the items in the lists are dictionaries, then the attribute provided
        by the `key` parameters is used for comparing the items.

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
                    self.api.warn(
                        "The field {k} of {object_type} {name} has encrypted data and may inaccurately report task is changed.".format(
                            k=k, object_type=self.object_type, name=self.name
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

    def get_object(self, name, exit_on_error=True):
        """Retrieve a single object from a GET API call.

        Upon completion, :py:attr:``self.exists`` is set to ``True`` if the
        object exists or ``False`` if not.
        :py:attr:``self.data`` contains the retrieved object (or ``{}`` if
        the requested object does not exist)

        :param name: Name of the object to retrieve.
        :type name: str
        :param exit_on_error: If ``True`` (the default), exit the module on API
                              error. Otherwise, raise the
                              :py:class:``AHAPIModuleError`` exception.
        :type exit_on_error: bool

        :raises AHAPIModuleError: An API error occured. That exception is only
                                  raised when ``exit_on_error`` is ``False``.
        """
        query = {self.name_field: name, "limit": "1000"}
        url = self.api.build_ui_url(self.endpoint, query_params=query)
        try:
            response = self.api.make_request("GET", url)
        except AHAPIModuleError as e:
            if exit_on_error:
                self.api.fail_json(msg="GET error: {error}".format(error=e))
            else:
                raise

        if response["status_code"] != 200:
            error_msg = self.api.extract_error_msg(response)
            if error_msg:
                fail_msg = "Unable to get {object_type} {name}: {code}: {error}".format(
                    object_type=self.object_type, name=name, code=response["status_code"], error=error_msg
                )
            else:
                fail_msg = "Unable to get {object_type} {name}: {code}".format(object_type=self.object_type, name=name, code=response["status_code"])
            if exit_on_error:
                self.api.fail_json(msg=fail_msg)
            else:
                raise AHAPIModuleError(fail_msg)

        if "meta" not in response["json"] or "count" not in response["json"]["meta"] or "data" not in response["json"]:
            fail_msg = "Unable to get {object_type} {name}: the endpoint did not provide count and results".format(object_type=self.object_type, name=name)
            if exit_on_error:
                self.api.fail_json(msg=fail_msg)
            else:
                raise AHAPIModuleError(fail_msg)

        if response["json"]["meta"]["count"] == 0:
            self.data = {}
            self.exists = False
            return

        if response["json"]["meta"]["count"] > 1:
            # Only one object should be returned. If more that one is returned,
            # then look for the requested name in the returned list.
            for asset in response["json"]["data"]:
                if self.name_field in asset and asset[self.name_field] == name:
                    self.data = asset
                    self.exists = True
                    return
            self.data = {}
            self.exists = False
            return

        self.data = response["json"]["data"][0]
        # Make sure the object name is available in the response
        if self.name_field not in self.data:
            self.data[self.name_field] = name
        self.exists = True

    def delete(self, auto_exit=True):
        """Perform a DELETE API call to delete the object.

        :param auto_exit: Exit the module when the API call is done.
        :type auto_exit: bool
        """
        if not self.exists:
            if auto_exit:
                self.api.exit_json(changed=False)
            return

        if self.api.check_mode:
            if auto_exit:
                self.api.exit_json(changed=True)
            self.exists = False
            self.data = {}
            return

        url = self.api.build_ui_url(self.id_endpoint)
        try:
            response = self.api.make_request("DELETE", url)
        except AHAPIModuleError as e:
            self.api.fail_json(msg="Delete error: {error}".format(error=e))

        if response["status_code"] in [202, 204]:
            if auto_exit:
                json_output = {"name": self.name, "id": self.id, "type": self.object_type, "changed": True}
                self.api.exit_json(**json_output)
            self.exists = False
            self.data = {}
            return

        error_msg = self.api.extract_error_msg(response)
        if error_msg:
            self.api.fail_json(msg="Unable to delete {object_type} {name}: {error}".format(object_type=self.object_type, name=self.name, error=error_msg))
        self.api.fail_json(
            msg="Unable to delete {object_type} {name}: {code}".format(object_type=self.object_type, name=self.name, code=response["status_code"])
        )

    def create(self, new_item, auto_exit=True):
        """Perform an POST API call to create a new object.

        :param new_item: Tha data to pass to the API call. This provides the
                         object details ({"username": "jdoe", ...} for example)
        :type new_item: dict
        :param auto_exit: Exit the module when the API call is done.
        :type auto_exit: bool

        :return: Do not return if ``auto_exit`` is ``True``. Otherwise, return
                 ``True``.
        :rtype: bool
        """
        if self.api.check_mode:
            self.data.update(new_item)
            if auto_exit:
                json_output = {"name": self.name, "id": self.id, "type": self.object_type, "changed": True}
                self.api.exit_json(**json_output)
            return True

        url = self.api.build_ui_url(self.endpoint)
        try:
            response = self.api.make_request("POST", url, data=new_item)
        except AHAPIModuleError as e:
            self.api.fail_json(msg="Create error: {error}".format(error=e))

        if response["status_code"] in [200, 201]:
            self.exists = True
            self.data = response["json"]
            # Make sure the object name is available in the response
            if self.name_field not in self.data:
                self.data[self.name_field] = new_item[self.name_field]
            if auto_exit:
                json_output = {"name": self.name, "id": self.id, "type": self.object_type, "changed": True}
                self.api.exit_json(**json_output)
            return True

        error_msg = self.api.extract_error_msg(response)
        if error_msg:
            self.fail_json(msg="Unable to create {object_type} {name}: {error}".format(object_type=self.object_type, name=self.name, error=error_msg))
        self.fail_json(msg="Unable to create {object_type} {name}: {code}".format(object_type=self.object_type, name=self.name, code=response["status_code"]))

    def update(self, new_item, auto_exit=True):
        """Update the existing object in private automation hub.

        :param new_item: The data to pass to the API call. This provides the
                         object details ({"username": "jdoe", ...} for example)
        :type new_item: dict
        :param auto_exit: Exit the module when the API call is done.
        :type auto_exit: bool

        :return: Do not return if ``auto_exit`` is ``True``. Otherwise, return
                 ``True`` if object has been updated (change state) or ``False``
                 if the object do not need updating.
        :rtype: bool
        """
        # The "key" field ("name", "username", ...) is required for PUT
        # requests. Making sure that it is present.
        if self.name_field not in new_item:
            new_item[self.name_field] = self.name

        # Check to see if anything within the item requires the item to be
        # updated.
        needs_patch = self.objects_could_be_different(self.data, new_item)

        if not needs_patch:
            if auto_exit:
                json_output = {"name": self.name, "id": self.id, "type": self.object_type, "changed": False}
                self.api.exit_json(**json_output)
            return False

        if self.api.check_mode:
            self.data.update(new_item)
            if auto_exit:
                json_output = {"name": self.name, "id": self.id, "type": self.object_type, "changed": True}
                self.api.exit_json(**json_output)
            return True

        url = self.api.build_ui_url(self.id_endpoint)
        try:
            response = self.api.make_request("PUT", url, data=new_item)
        except AHAPIModuleError as e:
            self.api.fail_json(msg="Update error: {error}".format(error=e))

        if response["status_code"] == 200:
            self.exists = True
            self.data = response["json"]
            # Make sure the object name is available in the response
            if self.name_field not in self.data:
                self.data[self.name_field] = new_item[self.name_field]
            if auto_exit:
                json_output = {"name": self.name, "id": self.id, "type": self.object_type, "changed": True}
                self.api.exit_json(**json_output)
            return True

        error_msg = self.api.extract_error_msg(response)
        if error_msg:
            self.fail_json(msg="Unable to update {object_type} {name}: {error}".format(object_type=self.object_type, name=self.name, error=error_msg))
        self.fail_json(msg="Unable to update {object_type} {name}: {code}".format(object_type=self.object_type, name=self.name, code=response["status_code"]))

    def create_or_update(self, new_item, auto_exit=True):
        """Create or update the current object in private automation hub.

        :param new_item: The data to pass to the API call. This provides the
                         object details ({"username": "jdoe", ...} for example)
        :type new_item: dict
        :param auto_exit: Exit the module when the API call is done.
        :type auto_exit: bool

        :return: Do not return if ``auto_exit`` is ``True``. Otherwise, return
                 ``True`` if object has been updated (change state) or ``False``
                 if the object do not need updating.
        :rtype: bool
        """
        if self.exists:
            return self.update(new_item, auto_exit)
        else:
            return self.create(new_item, auto_exit)


class AHUIUser(AHUIObject):
    """Manage the Ansible automation hub UI user API.

    Listing users:
        ``GET /api/galaxy/_ui/v1/users/``

    Getting the details of a user:
        ``GET /api/galaxy/_ui/v1/users/<ID#>/`` ::

            {
              "id": 19,
              "username": "admin1",
              "first_name": "Jean",
              "last_name": "Vasquez",
              "email": "lvasquez@example.com",
              "groups": [
                {
                  "id": 22,
                  "name": "operators"
                },
                {
                  "id": 23,
                  "name": "administrators"
                }
              ],
              "date_joined": "2021-08-12T09:45:21.516810Z",
              "is_superuser": false
            }

    Searching for users:
        ``GET /api/galaxy/_ui/v1/users/?username=admin1`` ::

            {
              "meta": {
                "count": 1
              },
              "links": {
                "first": "/api/galaxy/_ui/v1/users/?limit=10&offset=0&username=admin1",
                "previous": null,
                "next": null,
                "last": "/api/galaxy/_ui/v1/users/?limit=10&offset=0&username=admin1"
              },
              "data": [
                {
                  "id": 19,
                  "username": "admin1",
                  "first_name": "Jean",
                  "last_name": "Vasquez",
                  "email": "lvasquez@example.com",
                  "groups": [
                    {
                      "id": 22,
                      "name": "operators"
                    },
                    {
                      "id": 23,
                      "name": "administrators"
                    }
                  ],
                  "date_joined": "2021-08-12T09:45:21.516810Z",
                  "is_superuser": false
                }
              ]
            }

    Deleting a user:
        ``DELETE /api/galaxy/_ui/v1/users/<ID#>/``

    Creating a user:
        ``POST /api/galaxy/_ui/v1/users/``

    Updating a user:
        ``PUT /api/galaxy/_ui/v1/users/``
    """

    def __init__(self, API_object, data={}):
        """Initialize the object."""
        super(AHUIUser, self).__init__(API_object, data)
        self.endpoint = "users"
        self.object_type = "user"
        self.name_field = "username"

    @property
    def superuser(self):
        """Tell if the user is a super user or not."""
        return self.api.boolean(self.data.get("is_superuser", False))

    @property
    def groups(self):
        """Return the groups for which the user is a member."""
        return self.data.get("groups", [])


class AHUIGroup(AHUIObject):
    """Manage the Ansible Automation Hub UI group API.

    Listing groups:
        ``GET /api/galaxy/_ui/v1/groups/`` ::

            {
              "meta": {
                "count": 3
              },
              "links": {
                "first": "/api/galaxy/_ui/v1/groups/?limit=10&offset=0",
                "previous": null,
                "next": null,
                "last": "/api/galaxy/_ui/v1/groups/?limit=10&offset=0"
              },
              "data": [
                {
                  "name": "operators",
                  "pulp_href": "/pulp/api/v3/groups/22/",
                  "id": 22
                },
                {
                  "name": "administrators",
                  "pulp_href": "/pulp/api/v3/groups/23/",
                  "id": 23
                },
                {
                  "name": "managers",
                  "pulp_href": "/pulp/api/v3/groups/24/",
                  "id": 24
                }
              ]
            }

    Getting the details of a group:
        ``GET /api/galaxy/_ui/v1/groups/<ID#>/`` ::

            {
              "name": "operators",
              "pulp_href": "/pulp/api/v3/groups/22/",
              "id": 22
            }

    Searching for groups:
        ``GET /api/galaxy/_ui/v1/groups/?name=operators`` ::

            {
              "meta": {
                "count": 1
              },
              "links": {
                "first": "/api/galaxy/_ui/v1/groups/?limit=10&name=operators&offset=0",
                "previous": null,
                "next": null,
                "last": "/api/galaxy/_ui/v1/groups/?limit=10&name=operators&offset=0"
              },
              "data": [
                {
                  "name": "operators",
                  "pulp_href": "/pulp/api/v3/groups/22/",
                  "id": 22
                }
              ]
            }


    Deleting a group:
        ``DELETE /api/galaxy/_ui/v1/groups/<ID#>/``

    Creating a group:
        ``POST /api/galaxy/_ui/v1/groups/``

    Updating a group:
        The API does not allow changing the group name.
    """

    def __init__(self, API_object, data={}):
        """Initialize the object."""
        super(AHUIGroup, self).__init__(API_object, data)
        self.endpoint = "groups"
        self.object_type = "group"
        self.name_field = "name"
        self.perms = []

    def load_perms(self):
        """Retrieve the group permissions."""
        if not self.exists:
            self.perms = []
            return

        url = self.api.build_ui_url(AHUIGroupPerm.perm_endpoint(self.id), query_params={"limit": 100})
        try:
            response = self.api.make_request("GET", url)
        except AHAPIModuleError as e:
            self.api.fail_json(msg="Getting permissions error: {error}".format(error=e))

        if response["status_code"] != 200:
            error_msg = self.api.extract_error_msg(response)
            if error_msg:
                fail_msg = "Unable to get permissions for {object_type} {name}: {code}: {error}".format(
                    object_type=self.object_type, name=self.name, code=response["status_code"], error=error_msg
                )
            else:
                fail_msg = "Unable to get permissions for {object_type} {name}: {code}".format(
                    object_type=self.object_type, name=self.name, code=response["status_code"]
                )
            self.api.fail_json(msg=fail_msg)

        if "meta" not in response["json"] or "count" not in response["json"]["meta"] or "data" not in response["json"]:
            self.api.fail_json(
                msg="Unable to get permissions for {object_type} {name}: the endpoint did not provide count and results".format(
                    object_type=self.object_type, name=self.name
                )
            )

        self.perms = []
        if response["json"]["meta"]["count"] == 0:
            return
        for r in response["json"]["data"]:
            self.perms.append(AHUIGroupPerm(self.api, self.id, r))

    def get_perms(self):
        """Return the permissions associated with the group.

        :return: The list of permission names.
        :rtype: list
        """
        return [p.name for p in self.perms]

    def delete_perms(self, perms_to_delete):
        """Remove permissions from the group.

        The method exits the module.

        :param perms_to_delete: List of the permission names to remove from the
                                group.
        :type perms_to_delete: list
        """
        if perms_to_delete is not None and len(perms_to_delete) > 0:
            for perm_name in perms_to_delete:
                for perm in self.perms:
                    if perm.is_perm(perm_name):
                        perm.delete(auto_exit=False)
                        break
            self.api.exit_json(changed=True)
        self.api.exit_json(changed=False)

    def create_perms(self, perms_to_create):
        """Add a permission to the group.

        The method exits the module.

        :param perms_to_create: List of the permission names to add to the
                                group.
        :type perms_to_delete: list
        """
        if perms_to_create is not None and len(perms_to_create) > 0:
            for perm_name in perms_to_create:
                perm = AHUIGroupPerm(self.api, self.id)
                perm.create({"permission": perm_name}, auto_exit=False)
            self.api.exit_json(changed=True)
        self.api.exit_json(changed=False)


class AHUIGroupPerm(AHUIObject):
    """Manage the Ansible Automation Hub UI group permissions API.

    Listing permissions for the group ID 8:
        ``GET /api/galaxy/_ui/v1/groups/8/model-permissions/?limit=100`` ::

            {
              "meta": {
                "count": 2
              },
              "links": {
                "first": "/api/galaxy/_ui/v1/groups/8/model-permissions/?limit=100&offset=0",
                "previous": null,
                "next": null,
                "last": "/api/galaxy/_ui/v1/groups/8/model-permissions/?limit=100&offset=0"
              },
              "data": [
                {
                  "pulp_href": "/pulp/api/v3/groups/8/model_permissions/37/",
                  "id": 37,
                  "permission": "ansible.modify_ansible_repo_content",
                  "obj": null
                },
                {
                  "pulp_href": "/pulp/api/v3/groups/8/model_permissions/6/",
                  "id": 6,
                  "permission": "ansible.change_collectionremote",
                  "obj": null
                }
              ]
            }

    Removing a permission from a group:
        ``DELETE /api/galaxy/_ui/v1/groups/8/model-permissions/37/``

    Adding a permission to a group:
        ``POST /api/galaxy/_ui/v1/groups/8/model-permissions/``
    """

    @staticmethod
    def perm_endpoint(group_id):
        """Return the endpoint for permissions for the given group."""
        return "groups/{id}/model-permissions".format(id=group_id)

    def __init__(self, API_object, group_id, data={}):
        """Initialize the object."""
        super(AHUIGroupPerm, self).__init__(API_object, data)
        self.endpoint = AHUIGroupPerm.perm_endpoint(group_id)
        self.object_type = "permissions"
        self.name_field = "permission"

    @property
    def id_endpoint(self):
        """Return the object's endpoint."""
        id = self.id
        if id is None:
            return self.endpoint
        return "{endpoint}/{id}".format(endpoint=self.endpoint, id=id)

    def is_perm(self, perm_name):
        """Tell if the given permission name is the name of the current permission."""
        return self.name == perm_name


class AHUIEENamespace(AHUIObject):
    """Manage the private automation hub execution environment namespaces.

    Execution Environment namespaces are managed through the Pulp API for
    creation and deletion, and through the UI API for assigning groups and
    permission.
    Although the UI API and the web UI cannot create nor delete namespaces, the
    module provides that feature.
    Normally, a namespace is automatically created when an image is pushed by
    using ``podman push``.

    The :py:class:``AHUIEENamespace`` manages the namespace through the UI API.
    It is used to manage groups and permissions associated with namespaces.
    See :py:class:``AHPulpEENamespace`` to create and delete namespaces.

    Getting the details of a namespace:
        ``GET /api/galaxy/_ui/v1/execution-environments/namespaces/<name>/`` ::

            {
              "name": "ansible-automation-platform-20-early-access",
              "my_permissions": [
                "container.add_containernamespace",
                "container.change_containernamespace",
                "container.delete_containernamespace",
                "container.namespace_add_containerdistribution",
                "container.namespace_change_containerdistribution",
                "container.namespace_delete_containerdistribution",
                "container.namespace_modify_content_containerpushrepository",
                "container.namespace_pull_containerdistribution",
                "container.namespace_push_containerdistribution",
                "container.namespace_view_containerdistribution",
                "container.namespace_view_containerpushrepository",
                "container.view_containernamespace"
              ],
              "owners": [
                "admin"
              ],
              "groups": [
                {
                  "id": 50,
                  "name": "operators",
                  "object_permissions": [
                    "namespace_add_containerdistribution"
                  ]
                }
              ]
            }

    Updating the groups and permissions:
        ``PUT /api/galaxy/_ui/v1/execution-environments/namespaces/<name>/`` ::

            data:
            {
              "groups":[
                {
                 "id":50,
                 "name":"operators",
                 "object_permissions": [
                   "namespace_add_containerdistribution"
                 ]
                }
              ]
            }
    """

    def __init__(self, API_object, data={}):
        """Initialize the object."""
        super(AHUIEENamespace, self).__init__(API_object, data)
        self.endpoint = "execution-environments/namespaces"
        self.object_type = "namespace"
        self.name_field = "name"

    @property
    def id_endpoint(self):
        """Return the object's endpoint."""
        name = self.name
        if name is None:
            return self.endpoint
        return "{endpoint}/{name}".format(endpoint=self.endpoint, name=name)

    def groups_are_different(self, old, new):
        """Compare two dictionaries.

        :param old: The current groups and permissions.
        :type old: dict
        :param new: The new groups and permissions.
        :type new: dict

        :return: ``True`` if the two sets are different, ``False`` otherwise.
        :rtype: bool
        """
        for n in new:
            for o in old:
                if o["id"] == n["id"]:
                    if set(o["object_permissions"]) != set(n["object_permissions"]):
                        return True
                    break
            else:
                if len(n["object_permissions"]):
                    return True
        return False

    def update_groups(self, new_item, auto_exit=True, exit_on_error=True):
        """Update the existing object in private automation hub.

        :param new_item: The data to pass to the API call. This provides the
                         object details (``{"groups": ...}``)
        :type new_item: dict
        :param auto_exit: Exit the module when the API call is done.
        :type auto_exit: bool
        :param exit_on_error: If ``True`` (the default), exit the module on API
                              error. Otherwise, raise the
                              :py:class:``AHAPIModuleError`` exception.
        :type exit_on_error: bool

        :raises AHAPIModuleError: An API error occured. That exception is only
                                  raised when ``exit_on_error`` is ``False``.

        :return: Do not return if ``auto_exit`` is ``True``. Otherwise, return
                 ``True`` if object has been updated (change state) or ``False``
                 if the object do not need updating.
        :rtype: bool
        """

        # Check to see if anything within the item requires the item to be
        # updated.
        needs_patch = self.groups_are_different(self.data["groups"], new_item["groups"])

        if not needs_patch:
            if auto_exit:
                json_output = {"name": self.name, "type": self.object_type, "changed": False}
                self.api.exit_json(**json_output)
            return False

        if self.api.check_mode:
            self.data["groups"].new_item
            if auto_exit:
                json_output = {"name": self.name, "type": self.object_type, "changed": True}
                self.api.exit_json(**json_output)
            return True

        url = self.api.build_ui_url(self.id_endpoint)
        try:
            response = self.api.make_request("PUT", url, data=new_item)
        except AHAPIModuleError as e:
            if exit_on_error:
                self.api.fail_json(msg="Updating groups error: {error}".format(error=e))
            else:
                raise

        if response["status_code"] == 200:
            self.exists = True
            self.data = response["json"]
            # Make sure the object name is available in the response
            if self.name_field not in self.data:
                self.data[self.name_field] = new_item[self.name_field]
            if auto_exit:
                json_output = {"name": self.name, "type": self.object_type, "changed": True}
                self.api.exit_json(**json_output)
            return True

        error_msg = self.api.extract_error_msg(response)
        if error_msg:
            fail_msg = "Unable to update {object_type} {name}: {error}".format(object_type=self.object_type, name=self.name, error=error_msg)
        else:
            fail_msg = "Unable to update {object_type} {name}: {code}".format(object_type=self.object_type, name=self.name, code=response["status_code"])
        if exit_on_error:
            self.api.fail_json(msg=fail_msg)
        else:
            raise AHAPIModuleError(fail_msg)


class AHUIEERemote(AHUIObject):
    def __init__(self, API_object, data={}):
        """Initialize the object."""
        super(AHUIEERemote, self).__init__(API_object, data)
        self.endpoint = "execution-environments/remotes"
        self.object_type = "remote"
        self.name_field = "pulp_id"
        self.id_field = "pulp_id"


class AHUIEERepository(AHUIObject):
    """Manage the README file of execution environment repositories.

    A repository (or container for Pulp) represents a container image and is
    stored inside a namespace.

    You manage execution environment repositories through two APIs:

    * The Pulp API can create and delete repositories, and can update the
      repository descrition text.
      See the :py:class:``AHPulpEERepository`` class.
    * The UI API can update the README file associated with the repository.
      That current class manages that API.

    Getting the details of a repository:
        ``GET /api/galaxy/_ui/v1/execution-environments/repositories/<name>/`` ::

            {
              "meta": {
                "count": 1
              },
              "links": {
                "first": "/api/galaxy/_ui/v1/execution-environments/repositories/?name=ansible-automation-platform-20-early-access%2Fee-supported-rhel8",
                "previous": null,
                "next": null,
                "last": "/api/galaxy/_ui/v1/execution-environments/repositories/?name=ansible-automation-platform-20-early-access%2Fee-supported-rhel8"
              },
              "data": [
                {
                  "id": "61b6c7de-a19b-4976-89c2-15d665781e20",
                  "name": "ansible-automation-platform-20-early-access/ee-supported-rhel8",
                  "pulp": {
                    "repository": {
                      "pulp_id": "8be51c84-e14c-4b84-8db1-8db4737ca9ff",
                      "pulp_type": "container.container-push",
                      "version": 7,
                      "name": "ansible-automation-platform-20-early-access/ee-supported-rhel8",
                      "description": null
                    },
                    "distribution": {
                      "pulp_id": "61b6c7de-a19b-4976-89c2-15d665781e20",
                      "name": "ansible-automation-platform-20-early-access/ee-supported-rhel8",
                      "base_path": "ansible-automation-platform-20-early-access/ee-supported-rhel8"
                    }
                  },
                  "namespace": {
                    "name": "ansible-automation-platform-20-early-access",
                    "my_permissions": [
                      "container.add_containernamespace",
                      ...
                      "container.view_containernamespace"
                    ],
                    "owners": [
                      "admin"
                    ]
                  },
                  "description": null,
                  "created": "2021-08-17T08:21:01.751907Z",
                  "updated": "2021-08-17T08:21:37.194078Z"
                }
              ]
            }

    Getting the README file contents:
        ``GET /api/galaxy/_ui/v1/execution-environments/repositories/<name>/_content/readme/``

    Setting the README file contents:
        ``PUT /api/galaxy/_ui/v1/execution-environments/repositories/<name>/_content/readme/``
    """

    def __init__(self, API_object, data={}):
        """Initialize the object."""
        super(AHUIEERepository, self).__init__(API_object, data)
        self.endpoint = "execution-environments/repositories"
        self.object_type = "repository"
        self.name_field = "name"

    @property
    def id_endpoint(self):
        """Return the object's endpoint."""
        name = self.name
        if name is None:
            return self.endpoint
        return "{endpoint}/{name}".format(endpoint=self.endpoint, name=name)

    def sync(self, wait, interval, timeout):
        """Perform an POST API call to sync an object.

        :param wait: Whether to wait for the object to finish syncing
        :type wait: bool
        :param interval: How often to poll for a change in the sync status
        :type interval: integer
        :param timeout: How long to wait for the sync to complete in seconds
        :type timeout: integer
        :param auto_exit: Exit the module when the API call is done.
        :type auto_exit: bool

        :return: Do not return if ``auto_exit`` is ``True``. Otherwise, return
                 ``True``.
        :rtype: bool
        """

        url = self.api.build_ui_url("{endpoint}/_content/sync".format(endpoint=self.id_endpoint))
        try:
            response = self.api.make_request("POST", url, wait_for_task=False)
        except AHAPIModuleError as e:
            self.api.fail_json(msg="Start Sync error: {error}".format(error=e))

        if response["status_code"] == 202:
            sync_status = "Started"
            if wait:
                start = time.time()
                task_href = response["json"]["task"]
                taskPulp = AHPulpTask(self.api)
                elapsed = 0
                while sync_status not in ["Complete", "Failed"]:
                    taskPulp.get_object(task_href)
                    if taskPulp.data["error"]:
                        sync_status = "Complete"
                        error_output = taskPulp.data["error"]["description"].split(",")
                        self.api.fail_json(status=error_output[0], msg=error_output[1], url=error_output[2], traceback=taskPulp.data["error"]["traceback"])
                    if taskPulp.data["state"] == "completed":
                        sync_status = "Complete"
                        break
                    time.sleep(interval)
                    elapsed = time.time() - start
                    if timeout and elapsed > timeout:
                        self.api.fail_json(msg="Timed out awaiting sync")

            json_output = {"name": self.name, "changed": True, "sync_status": sync_status, "task": response["json"]["task"]}
            self.api.exit_json(**json_output)
            return True

        error_msg = self.api.extract_error_msg(response)
        if error_msg:
            self.api.fail_json(msg="Unable to create {object_type} {name}: {error}".format(object_type=self.object_type, name=self.name, error=error_msg))
        self.api.fail_json(
            msg="Unable to create {object_type} {name}: {code}".format(object_type=self.object_type, name=self.name, code=response["status_code"])
        )

    def get_readme(self):
        """Retrieve and return the README file associated with the repository.

        ``GET /api/galaxy/_ui/v1/execution-environments/repositories/<name>/_content/readme/ ::

            {
                "updated":"2021-08-17T12:54:37.250390Z",
                "created":"2021-08-17T12:54:37.250369Z",
                "text":""
            }

        :return: The README file contents.
        :rtype: str
        """
        if not self.exists:
            return ""

        url = self.api.build_ui_url("{endpoint}/_content/readme".format(endpoint=self.id_endpoint))
        try:
            response = self.api.make_request("GET", url)
        except AHAPIModuleError as e:
            self.api.fail_json(msg="Error while getting the README: {error}".format(error=e))

        if response["status_code"] == 200:
            return response["json"]["text"] if "text" in response["json"] else ""
        error_msg = self.api.extract_error_msg(response)
        if error_msg:
            self.fail_json(
                msg="Unable to retrieve the README for {object_type} {name}: {error}".format(object_type=self.object_type, name=self.name, error=error_msg)
            )
        self.fail_json(
            msg="Unable to retrieve the README for {object_type} {name}: {code}".format(
                object_type=self.object_type, name=self.name, code=response["status_code"]
            )
        )

    def update_readme(self, readme, auto_exit=True):
        """Update the repository README in private automation hub.

        :param readme: The README file contents.
        :type readme: str
        :param auto_exit: Exit the module when the API call is done.
        :type auto_exit: bool

        :return: Do not return if ``auto_exit`` is ``True``. Otherwise, return
                 ``True`` if object has been updated (change state) or ``False``
                 if the object do not need updating.
        :rtype: bool
        """
        # Verify if the README needs updating
        old_readme = self.get_readme()
        if old_readme.strip() == readme.strip():
            if auto_exit:
                json_output = {"name": self.name, "type": self.object_type, "changed": False}
                self.api.exit_json(**json_output)
            return False

        if self.api.check_mode:
            if auto_exit:
                json_output = {"name": self.name, "type": self.object_type, "changed": True}
                self.api.exit_json(**json_output)
            return True

        url = self.api.build_ui_url("{endpoint}/_content/readme".format(endpoint=self.id_endpoint))
        try:
            response = self.api.make_request("PUT", url, data={"text": readme})
        except AHAPIModuleError as e:
            self.api.fail_json(msg="Unable to update the README: {error}".format(error=e))

        if response["status_code"] == 200:
            if auto_exit:
                json_output = {"name": self.name, "type": self.object_type, "changed": True}
                self.api.exit_json(**json_output)
            return True

        error_msg = self.api.extract_error_msg(response)
        if error_msg:
            self.fail_json(
                msg="Unable to update the README for {object_type} {name}: {error}".format(object_type=self.object_type, name=self.name, error=error_msg)
            )
        self.fail_json(
            msg="Unable to update the README for {object_type} {name}: {code}".format(
                object_type=self.object_type, name=self.name, code=response["status_code"]
            )
        )


class AHUIEERegistry(AHUIObject):
    """Manage execution environment registries.

    A registry is a remote resource which can be synced to pull down repositories (container images)

    Getting the info for a registry:
        ``GET /api/galaxy/_ui/v1/execution-environments/registries/<pk>`` ::

            {
                "pk": "70acd9b2-ca24-48bb-b62f-87099022d69c",
                "name": "test3",
                "url": "https://quay.io/mytest",
                "policy": "immediate",
                "created_at": "2022-04-05T17:21:41.556808Z",
                "updated_at": "2022-04-05T17:21:41.556829Z",
                "tls_validation": false,
                "client_cert": null,
                "ca_cert": null,
                "last_sync_task": {},
                "download_concurrency": null,
                "proxy_url": null,
                "write_only_fields": [
                    {
                        "name": "client_key",
                        "is_set": false
                    },
                    {
                        "name": "username",
                        "is_set": false
                    },
                    {
                        "name": "password",
                        "is_set": false
                    },
                    {
                        "name": "client_key",
                        "is_set": false
                    },
                    {
                        "name": "proxy_username",
                        "is_set": false
                    },
                    {
                        "name": "proxy_password",
                        "is_set": false
                    }
                ],
                "rate_limit": null,
                "is_indexable": false
            }
    """

    def __init__(self, API_object, data={}):
        """Initialize the object."""
        super(AHUIEERegistry, self).__init__(API_object, data)
        self.endpoint = "execution-environments/registries"
        self.object_type = "registries"
        self.name_field = "name"
        self.id_field = "pk"

    def sync(self, wait, interval, timeout, auto_exit=True):
        """Perform an POST API call to sync an object.

        :param wait: Whether to wait for the object to finish syncing
        :type wait: bool
        :param interval: How often to poll for a change in the sync status
        :type interval: integer
        :param timeout: How long to wait for the sync to complete in seconds
        :type timeout: integer
        :param auto_exit: Exit the module when the API call is done.
        :type auto_exit: bool

        :return: Do not return if ``auto_exit`` is ``True``. Otherwise, return
                 ``True``.
        :rtype: bool
        """

        url = self.api.build_ui_url("{endpoint}/sync".format(endpoint=self.id_endpoint))
        try:
            response = self.api.make_request("POST", url)
        except AHAPIModuleError as e:
            self.api.fail_json(msg="Start Sync error: {error}".format(error=e))

        if response["status_code"] == 202:
            task_status = "Started"
            if wait:
                parentTask = response["json"]["task"]
                taskPulp = AHPulpTask(self.api)
                task_status = taskPulp.wait_for_children(parentTask, interval, timeout)

            if auto_exit:
                json_output = {"name": self.name, "changed": True, "task_status": task_status, "task": response["json"]["task"]}
                self.api.exit_json(**json_output)
            return True

        error_msg = self.api.extract_error_msg(response)
        if error_msg:
            self.api.fail_json(msg="Unable to create {object_type} {name}: {error}".format(object_type=self.object_type, name=self.name, error=error_msg))
        self.api.fail_json(
            msg="Unable to create {object_type} {name}: {code}".format(object_type=self.object_type, name=self.name, code=response["status_code"])
        )

    def index(self, wait, interval, timeout, auto_exit=True):
        """Perform an POST API call to index an object.

        :param wait: Whether to wait for the object to finish syncing
        :type wait: bool
        :param interval: How often to poll for a change in the sync status
        :type interval: integer
        :param timeout: How long to wait for the sync to complete in seconds
        :type timeout: integer
        :param auto_exit: Exit the module when the API call is done.
        :type auto_exit: bool

        :return: Do not return if ``auto_exit`` is ``True``. Otherwise, return
                 ``True``.
        :rtype: bool
        """

        url = self.api.build_ui_url("{endpoint}/index".format(endpoint=self.id_endpoint))
        try:
            response = self.api.make_request("POST", url)
        except AHAPIModuleError as e:
            self.api.fail_json(msg="Start Sync error: {error}".format(error=e))

        if response["status_code"] == 202:
            task_status = "Started"
            if wait:
                parentTask = response["json"]["task"]
                taskPulp = AHPulpTask(self.api)
                task_status = taskPulp.wait_for_children(parentTask, interval, timeout)

            if auto_exit:
                json_output = {"name": self.name, "changed": True, "task_status": task_status, "task": response["json"]["task"]}
                self.api.exit_json(**json_output)
            return True

        error_msg = self.api.extract_error_msg(response)
        if error_msg:
            self.api.fail_json(msg="Unable to create {object_type} {name}: {error}".format(object_type=self.object_type, name=self.name, error=error_msg))
        self.api.fail_json(
            msg="Unable to create {object_type} {name}: {code}".format(object_type=self.object_type, name=self.name, code=response["status_code"])
        )


class AHUIEEImage(AHUIObject):
    """Manage execution environment images.

    A repository (or container for Pulp) represents a container image and is
    stored inside a namespace.

    You manage execution environment images through two APIs:

    * The Pulp API can delete images, and add or remove tags.
      See the :py:class:``AHPulpEERepository`` class.
    * The UI API can retrieve the SHA256 digests for the tagging operations.
      That current class manages that API.

    Getting the list of images for a repository:
        ``GET /api/galaxy/_ui/v1/execution-environments/repositories/<name>/_content/images/`` ::

            {
              "meta": {
                "count": 2
              },
              "links": {
                ...
              },
              "data": [
                {
                  "pulp_id": "a7d13a94-cd12-4fee-9d7f-665f0b083382",
                  "digest": "sha256:a4ebd33ba78252a3c17bf951ff82ac39a6e1020d25031            eb42a8c0d2a0f673c9e",
                  "schema_version": 2,
                  "media_type": "application/vnd.docker.distribution.manifest.v2+json",
                  "config_blob": {
                    "digest": "sha256:54993dbce43b6d346b7840cde5ab44c3001d4751deaf8ac4a9592d56638e062f",
                    "media_type": "application/vnd.docker.image.rootfs.diff.tar.gzip"
                  },
                  "tags": [
                    "test123",
                    "2.0.0-10"
                  ],
                  "pulp_created": "2021-08-16T09:22:45.136729Z",
                  "layers": [
                    ...
                  ]
                },
                {
                  "pulp_id": "1fcf4d3e-15ef-44c3-87f0-2037aaefd249",
                  "digest": "sha256:902643fa5de3ce478dccd7a7182e6b91469a8a9539043e788d315ecc557d792a",
                  "schema_version": 2,
                  "media_type": "application/vnd.docker.distribution.manifest.v2+json",
                  "config_blob": {
                    "digest": "sha256:078c7d4aca51b39cf0dc6dfdf8efb9953216cb1502a9ec935d5973b7afdfbdb7",
                    "media_type": "application/vnd.docker.image.rootfs.diff.tar.gzip"
                  },
                  "tags": [
                    "2.0.0-15"
                  ],
                  "pulp_created": "2021-08-18T08:31:38.919872Z",
                  "layers": [
                    ...
                  ]
                }
              ]
            }
    """

    def __init__(self, API_object, data={}):
        """Initialize the object."""
        super(AHUIEEImage, self).__init__(API_object, data)
        self.endpoint = "execution-environments/repositories"
        self.object_type = "image"
        self.name_field = "name"

    @property
    def id_endpoint(self):
        """Return the object's endpoint."""
        name = self.image_name
        if name is None:
            return self.endpoint
        return "{endpoint}/{name}/_content/images/".format(endpoint=self.endpoint, name=name)

    def get_tag(self, name, tag):
        """Retrieve the image associated with the given repository and tag.

        Upon completion, if the object exists, then :py:attr:``self.digest`` is
        set to the SHA256 image digest and :py:attr:``self.tags`` is set to the
        list of tags.
        If the object does not exist, then :py:attr:``self.digest`` is set to
        ``None``.

        :param name: Name of the image (or repository name).
        :type name: str
        :param tag: Name of the tag to retrieve.
        :type tag: str
        """
        self.image_name = name
        self.tag = tag
        url = self.api.build_ui_url(self.id_endpoint, query_params={"limit": 1000})
        try:
            response = self.api.make_request("GET", url)
        except AHAPIModuleError as e:
            self.api.fail_json(msg="Unable to get tag: {error}".format(error=e))

        if response["status_code"] != 200:
            error_msg = self.api.extract_error_msg(response)
            if error_msg:
                fail_msg = "Unable to get {object_type} {name}: {code}: {error}".format(
                    object_type=self.object_type, name=name, code=response["status_code"], error=error_msg
                )
            else:
                fail_msg = "Unable to get {object_type} {name}: {code}".format(object_type=self.object_type, name=name, code=response["status_code"])
            self.api.fail_json(msg=fail_msg)

        if "meta" not in response["json"] or "count" not in response["json"]["meta"] or "data" not in response["json"]:
            self.api.fail_json(
                msg="Unable to get {object_type} {name}: the endpoint did not provide count and results".format(object_type=self.object_type, name=name)
            )

        self.digest = None
        self.tags = []
        for asset in response["json"]["data"]:
            if "tags" in asset and tag in asset["tags"] and "digest" in asset:
                self.digest = asset["digest"]
                self.tags = asset["tags"]
                break
