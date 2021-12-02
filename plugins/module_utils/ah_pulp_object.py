# Copyright: (c) 2021, Herve Quatremain <hquatrem@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# You can consult the UI API documentation directly on a running private
# automation hub at https://hub.example.com/pulp/api/v3/docs/
#
# Ansible Automation Hub UI project at https://github.com/ansible/ansible-hub-ui

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class AHPulpObject(object):
    """Manage Pulp objects through the API.

    Create a subclass of :py:class:``AHPulpObject`` to represent a specific type
    of object (namespace, ...)

    :param API_object: Module object to use to access the private automation hub API.
    :type API_object: :py:class:``AHAPIModule``
    :param data: Initial data
    :type data: dict
    """

    def __init__(self, API_object, data={}):
        """Initialize the module."""
        # The API endpoint is the last component of the URL and allows access
        # to the object API:
        #   https://hub.example.com/pulp/api/v3/<endpoint>/
        # Example:
        #   https://hub.example.com/pulp/api/v3/pulp_container/namespaces/ (endpoint=pulp_container/namespaces)
        self.endpoint = None

        # Type of the objects managed by the class. This is only used in the
        # messages returned to the user.
        self.object_type = "object"

        # In the JSON API response message, self.name_field is the name of the
        # attribute that stores the object name. This is also used as the query
        # parameter in GET requests (https://..../pulp_container/namespaces/?name=aap20)
        self.name_field = "name"

        # JSON data returned by the last API call. This typically stores the
        # object details:
        #   {
        #      "name": "AAP20",
        #      "pulp_created": "2021-08-16T09:22:40.249903Z",
        #      "pulp_href": "/pulp/api/v3/pulp_container/namespaces/017bc08f-99f7-4fc6-859c-3cff0713e39b/"
        #   }
        self.data = data

        # Is the class instance has been initialized with a valid object?
        self.exists = True if data else False

        # The AHAPIModule class object that is used to access the API
        self.api = API_object

    @property
    def href(self):
        """Return the object URL path."""
        if "pulp_href" in self.data:
            return self.data["pulp_href"]
        return None

    @property
    def name(self):
        """Return the object name."""
        if self.name_field in self.data:
            return self.data[self.name_field]
        return None

    def get_object(self, name):
        """Retrieve a single object from a GET API call.

        Upon completion, :py:attr:``self.exists`` is set to ``True`` if the
        object exists or ``False`` if not.
        :py:attr:``self.data`` contains the retrieved object (or ``{}`` if
        the requested object does not exist)

        :param name: Name of the object to retrieve.
        :type name: str
        """
        query = {self.name_field: name}
        url = self.api.build_pulp_url(self.endpoint, query_params=query)
        response = self.api.make_request("GET", url)
        if response["status_code"] != 200:
            error_msg = self.api.extract_error_msg(response)
            if error_msg:
                fail_msg = "Unable to get {object_type} {name}: {code}: {error}".format(
                    object_type=self.object_type, name=name, code=response["status_code"], error=error_msg
                )
            else:
                fail_msg = "Unable to get {object_type} {name}: {code}".format(object_type=self.object_type, name=name, code=response["status_code"])
            self.api.fail_json(msg=fail_msg)

        if "count" not in response["json"] or "results" not in response["json"]:
            self.api.fail_json(
                msg="Unable to get {object_type} {name}: the endpoint did not provide count and results".format(object_type=self.object_type, name=name)
            )

        if response["json"]["count"] == 0:
            self.data = {}
            self.exists = False
            return

        if response["json"]["count"] > 1:
            # Only one object should be returned. If more that one is returned,
            # then look for the requested name in the returned list.
            for asset in response["json"]["results"]:
                if self.name_field in asset and asset[self.name_field] == name:
                    self.data = asset
                    self.exists = True
                    return
            self.data = {}
            self.exists = False
            return

        self.data = response["json"]["results"][0]
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

        url = self.api.host_url._replace(path=self.href)
        response = self.api.make_request("DELETE", url)

        if response["status_code"] in [202, 204]:
            if auto_exit:
                json_output = {"name": self.name, "href": self.href, "type": self.object_type, "changed": True}
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
                         object details ({"name": "test123"} for example)
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
                json_output = {"name": self.name, "type": self.object_type, "changed": True}
                self.api.exit_json(**json_output)
            return True

        url = self.api.build_pulp_url(self.endpoint)
        response = self.api.make_request("POST", url, data=new_item)

        if response["status_code"] in [200, 201]:
            self.exists = True
            self.data = response["json"]
            # Make sure the object name is available in the response
            if self.name_field not in self.data:
                self.data[self.name_field] = new_item[self.name_field]
            if auto_exit:
                json_output = {"name": self.name, "href": self.href, "type": self.object_type, "changed": True}
                self.api.exit_json(**json_output)
            return True

        error_msg = self.api.extract_error_msg(response)
        if error_msg:
            self.fail_json(msg="Unable to create {object_type} {name}: {error}".format(object_type=self.object_type, name=self.name, error=error_msg))
        self.fail_json(msg="Unable to create {object_type} {name}: {code}".format(object_type=self.object_type, name=self.name, code=response["status_code"]))

    def object_are_different(self, old, new):
        for k in new.keys():
            if k not in old:
                return True
            new_item = new[k]
            old_item = old[k]
            if type(new_item) != type(old_item) or new_item != old_item:
                return True
        return False

    def update(self, new_item, auto_exit=True):
        """Update the existing object in private automation hub.

        :param new_item: The data to pass to the API call. This provides the
                         object details ({"description": "test"} for example)
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
        if "base_path" not in new_item:
            if "base_path" in self.data:
                new_item["base_path"] = self.data["base_path"]
            else:
                new_item["base_path"] = self.name

        # Check to see if anything within the item requires the item to be
        # updated.
        needs_patch = self.object_are_different(self.data, new_item)

        if not needs_patch:
            if auto_exit:
                json_output = {"name": self.name, "href": self.href, "type": self.object_type, "changed": False}
                self.api.exit_json(**json_output)
            return False

        if self.api.check_mode:
            self.data.update(new_item)
            if auto_exit:
                json_output = {"name": self.name, "href": self.href, "type": self.object_type, "changed": True}
                self.api.exit_json(**json_output)
            return True

        url = self.api.host_url._replace(path=self.href)
        response = self.api.make_request("PUT", url, data=new_item)

        if response["status_code"] in [200, 202, 204]:
            self.exists = True
            self.data.update(new_item)
            if auto_exit:
                json_output = {"name": self.name, "href": self.href, "type": self.object_type, "changed": True}
                self.api.exit_json(**json_output)
            return True

        error_msg = self.api.extract_error_msg(response)
        if error_msg:
            self.fail_json(msg="Unable to update {object_type} {name}: {error}".format(object_type=self.object_type, name=self.name, error=error_msg))
        self.fail_json(msg="Unable to update {object_type} {name}: {code}".format(object_type=self.object_type, name=self.name, code=response["status_code"]))


class AHPulpEENamespace(AHPulpObject):
    """Manage the execution environment namespace with the Pulp API.

    The :py:class:``AHPulpEENamespace`` creates and deletes namespaces.
    See :py:class:``AHUIEENamespace`` to manage groups and permissions.

    Getting the details of a namespace:
        ``GET /pulp/api/v3/pulp_container/namespaces/?name=<name>`` ::

            {
              "count": 1,
              "next": null,
              "previous": null,
              "results": [
                {
                  "pulp_href": "/pulp/api/v3/pulp_container/namespaces/dd54d0df-cd88-420b-922a-43a0725a20fc/",
                  "pulp_created": "2021-08-17T14:19:29.217506Z",
                  "name": "namespace1"
                }
              ]
            }

    Create a namespace:
        ``POST /pulp/api/v3/pulp_container/namespaces/``

    Delete a namespace:
        ``DELETE /pulp/api/v3/pulp_container/namespaces/dd54d0df-cd88-420b-922a-43a0725a20fc/``
    """

    def __init__(self, API_object, data={}):
        """Initialize the object."""
        super(AHPulpEENamespace, self).__init__(API_object, data)
        self.endpoint = "pulp_container/namespaces"
        self.object_type = "namespace"
        self.name_field = "name"


class AHPulpEERepository(AHPulpObject):
    """Manage the execution environment repository with the Pulp API.

    A repository (or container for Pulp) represents a container image and is
    stored inside a namespace.

    The :py:class:``AHPulpEENamespace`` creates, deletes, and set a description
    to repositories.
    Although the class can be used to create a repository, the recommended
    method is to push an image, with C(podman push) for example.
    Creating the repository with this class breaks the web UI, therefore the
    module does not provide that functionnality.

    See :py:class:``AHUIEERepository`` to manage the README file associated with the repository.

    Getting the details of a repository:
        ``GET /pulp/api/v3/distributions/container/container/?name=<name>`` ::

            {
              "count": 1,
              "next": null,
              "previous": null,
              "results": [
                {
                  "name": "ansible-automation-platform-20-early-access/ee-minimal-rhel8",
                  "base_path": "ansible-automation-platform-20-early-access/ee-minimal-rhel8",
                  "pulp_created": "2021-08-17T08:22:24.338660Z",
                  "pulp_href": "/pulp/api/v3/distributions/container/container/d610ec76-ec86-427e-89d4-4d28c37515e1/",
                  "pulp_labels": {},
                  "content_guard": "/pulp/api/v3/contentguards/container/content_redirect/2406a920-5821-432c-9c86-3ed36f2c87ef/",
                  "repository_version": null,
                  "repository": "/pulp/api/v3/repositories/container/container-push/7f926cb2-1cc7-4043-b0f2-da6c5cd7caa0/",
                  "registry_path": "hub.lab.example.com/ansible-automation-platform-20-early-access/ee-minimal-rhel8",
                  "namespace": "/pulp/api/v3/pulp_container/namespaces/88c3275f-72be-405d-83e2-d4a49cb444d9/",
                  "private": false,
                  "description": null
                }
              ]
            }

    Delete a repository:
        ``DELETE /pulp/api/v3/distributions/container/container/d610ec76-ec86-427e-89d4-4d28c37515e1/``
    """

    def __init__(self, API_object, data={}):
        """Initialize the object."""
        super(AHPulpEERepository, self).__init__(API_object, data)
        self.endpoint = "distributions/container/container"
        self.object_type = "repository"
        self.name_field = "name"

    @property
    def repository_endpoint(self):
        """Return the repository endpoint."""
        if self.exists and "repository" in self.data:
            return self.data["repository"]
        return ""

    def delete_image(self, digest, auto_exit=True):
        """Perform a POST API call to delete the image with the given digest.

        :param digest: Digest (SHA256) of the image to delete.
        :type digest: str
        :param auto_exit: Exit the module when the API call is done.
        :type auto_exit: bool
        """
        if not self.exists:
            if auto_exit:
                json_output = {"digest": digest, "type": "image", "changed": False}
                self.api.exit_json(changed=False)
            return

        if self.api.check_mode:
            if auto_exit:
                json_output = {"name": self.name, "digest": digest, "type": "image", "changed": True}
                self.api.exit_json(**json_output)
            return

        url = self.api.host_url._replace(path="{endpoint}remove_image/".format(endpoint=self.repository_endpoint))
        response = self.api.make_request("POST", url, data={"digest": digest})

        if response["status_code"] in [202, 204]:
            if auto_exit:
                json_output = {"name": self.name, "digest": digest, "type": "image", "changed": True}
                self.api.exit_json(**json_output)
            return

        error_msg = self.api.extract_error_msg(response)
        if error_msg:
            self.api.fail_json(
                msg="Unable to delete image from {object_type} {name}: {digest}: {error}".format(
                    object_type=self.object_type, name=self.name, digest=digest, error=error_msg
                )
            )
        self.api.fail_json(
            msg="Unable to delete image from {object_type} {name}: {digest}: {code}".format(
                object_type=self.object_type, name=self.name, digest=digest, code=response["status_code"]
            )
        )

    def delete_tag(self, digest, tag, auto_exit=True):
        """Perform a POST API call to delete the tag for the image with the given digest.

        :param digest: Digest (SHA256) of the image to update.
        :type digest: str
        :param tag: Tag to remove from the image.
        :type tag: str
        :param auto_exit: Exit the module when the API call is done.
        :type auto_exit: bool

        :return: Do not return if ``auto_exit`` is ``True``. Otherwise, return
                 ``True`` if object has been updated (change state) or ``False``
                 if the object do not need updating.
        """
        if not self.exists:
            if auto_exit:
                json_output = {"digest": digest, "tag": tag, "type": "image", "changed": False}
                self.api.exit_json(**json_output)
            return False

        if self.api.check_mode:
            if auto_exit:
                json_output = {"name": self.name, "digest": digest, "tag": tag, "type": "image", "changed": True}
                self.api.exit_json(**json_output)
            return True

        url = self.api.host_url._replace(path="{endpoint}untag/".format(endpoint=self.repository_endpoint))
        response = self.api.make_request("POST", url, data={"digest": digest, "tag": tag})

        if response["status_code"] in [202, 204]:
            if auto_exit:
                json_output = {"name": self.name, "digest": digest, "tag": tag, "type": "image", "changed": True}
                self.api.exit_json(**json_output)
            return True

        if response["status_code"] >= 400:
            if auto_exit:
                json_output = {"name": self.name, "digest": digest, "tag": tag, "type": "image", "changed": False}
                self.api.exit_json(**json_output)
            return False

        error_msg = self.api.extract_error_msg(response)
        if error_msg:
            self.api.fail_json(
                msg="Unable to delete image tag {tag} from {object_type} {name}: {digest}: {error}".format(
                    tag=tag, object_type=self.object_type, name=self.name, digest=digest, error=error_msg
                )
            )
        self.api.fail_json(
            msg="Unable to delete image tag {tag} from {object_type} {name}: {digest}: {code}".format(
                tag=tag, object_type=self.object_type, name=self.name, digest=digest, code=response["status_code"]
            )
        )

    def create_tag(self, digest, tag, auto_exit=True):
        """Perform a POST API call to add a tag to the image with the given digest.

        :param digest: Digest (SHA256) of the image to update.
        :type digest: str
        :param tag: Tag to add to the image.
        :type tag: str
        :param auto_exit: Exit the module when the API call is done.
        :type auto_exit: bool

        :return: Do not return if ``auto_exit`` is ``True``. Otherwise, return
                 ``True`` if object has been updated (change state) or ``False``
                 if the object do not need updating.
        """
        if not self.exists:
            if auto_exit:
                json_output = {"digest": digest, "tag": tag, "type": "image", "changed": False}
                self.api.exit_json(**json_output)
            return False

        if self.api.check_mode:
            if auto_exit:
                json_output = {"name": self.name, "digest": digest, "tag": tag, "type": "image", "changed": True}
                self.api.exit_json(**json_output)
            return True

        url = self.api.host_url._replace(path="{endpoint}tag/".format(endpoint=self.repository_endpoint))
        response = self.api.make_request("POST", url, data={"digest": digest, "tag": tag})

        if response["status_code"] in [202, 204]:
            if auto_exit:
                json_output = {"name": self.name, "digest": digest, "tag": tag, "type": "image", "changed": True}
                self.api.exit_json(**json_output)
            return True

        error_msg = self.api.extract_error_msg(response)
        if error_msg:
            self.api.fail_json(
                msg="Unable to add image tag {tag} to {object_type} {name}: {digest}: {error}".format(
                    tag=tag, object_type=self.object_type, name=self.name, digest=digest, error=error_msg
                )
            )
        self.api.fail_json(
            msg="Unable to add image tag {tag} to {object_type} {name}: {digest}: {code}".format(
                tag=tag, object_type=self.object_type, name=self.name, digest=digest, code=response["status_code"]
            )
        )
