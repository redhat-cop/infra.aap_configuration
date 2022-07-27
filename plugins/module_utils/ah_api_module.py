# Copyright: (c) 2021, Herve Quatremain <hquatrem@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# You can consult the UI API documentation directly on a running private
# automation hub at https://hub.example.com/pulp/api/v3/docs/
#
# Ansible Automation Hub UI project at https://github.com/ansible/ansible-hub-ui

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import base64
import re
import socket
import json
import time

from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_bytes, to_text

from ansible.module_utils.six.moves.urllib.parse import urlparse, urlencode
from ansible.module_utils.six.moves.urllib.error import HTTPError

from ansible.module_utils.urls import Request, SSLValidationError


class AHAPIModuleError(Exception):
    """API request error exception.

    :param error_message: Error message.
    :type error_message: str
    """

    def __init__(self, error_message):
        """Initialize the object."""
        self.error_message = error_message

    def __str__(self):
        """Return the error message."""
        return self.error_message


class AHAPIModule(AnsibleModule):
    """Ansible module for managing private automation hub servers."""

    AUTH_ARGSPEC = dict(
        ah_host=dict(required=False, aliases=["ah_hostname"], fallback=(env_fallback, ["AH_HOST"])),
        ah_username=dict(required=False, fallback=(env_fallback, ["AH_USERNAME"])),
        ah_password=dict(no_log=True, required=False, fallback=(env_fallback, ["AH_PASSWORD"])),
        ah_path_prefix=dict(required=False, fallback=(env_fallback, ["GALAXY_API_PATH_PREFIX"])),
        validate_certs=dict(type="bool", aliases=["ah_verify_ssl"], required=False, fallback=(env_fallback, ["AH_VERIFY_SSL"])),
    )
    short_params = {
        "host": "ah_host",
        "username": "ah_username",
        "password": "ah_password",
        "verify_ssl": "validate_certs",
        "path_prefix": "ah_path_prefix",
    }

    host = "127.0.0.1"
    username = None
    password = None
    verify_ssl = True
    path_prefix = "galaxy"
    authenticated = False

    def __init__(self, argument_spec, direct_params=None, **kwargs):
        """Initialize the object."""
        full_argspec = {}
        full_argspec.update(AHAPIModule.AUTH_ARGSPEC)
        full_argspec.update(argument_spec)

        if direct_params is not None:
            self.params = direct_params
        else:
            super(AHAPIModule, self).__init__(argument_spec=full_argspec, **kwargs)

        # Update the current object with the provided parameters
        for short_param, long_param in self.short_params.items():
            direct_value = self.params.get(long_param)
            if direct_value is not None:
                setattr(self, short_param, direct_value)

        # Perform some basic validation
        if not re.match("^https{0,1}://", self.host):
            self.host = "https://{host}".format(host=self.host)

        # Try to parse the hostname as a url
        try:
            self.host_url = urlparse(self.host)
        except Exception as e:
            self.fail_json(msg="Unable to parse ah_host as a URL ({host}): {error}".format(host=self.host, error=e))

        # Try to resolve the hostname
        try:
            socket.gethostbyname(self.host_url.hostname)
        except Exception as e:
            self.fail_json(msg="Unable to resolve ah_host ({host}): {error}".format(host=self.host_url.hostname, error=e))

        self.headers = {"referer": self.host, "Content-Type": "application/json", "Accept": "application/json"}
        self.session = Request(validate_certs=self.verify_ssl, headers=self.headers)

        # Define the API paths
        self.galaxy_path_prefix = "/api/{prefix}".format(prefix=self.path_prefix.strip("/"))
        self.ui_path_prefix = "{galaxy_prefix}/_ui/v1".format(galaxy_prefix=self.galaxy_path_prefix)
        self.pulp_path_prefix = "/pulp/api/v3"

    def _build_url(self, prefix, endpoint=None, query_params=None):
        """Return a URL from the given prefix and endpoint.

        The URL is build as follows::

            https://<host>/<prefix>/[<endpoint>]/[?<query>]

        :param prefix: Prefix to add to the endpoint.
        :type prefix: str
        :param endpoint: Usually the API object name ("users", "groups", ...)
        :type endpoint: str
        :param query_params: The optional query to append to the URL
        :type query_params: dict

        :return: The full URL built from the given prefix and endpoint.
        :rtype: :py:class:``urllib.parse.ParseResult``
        """
        if endpoint is None:
            api_path = "/{base}/".format(base=prefix.strip("/"))
        elif "?" in endpoint:
            api_path = "{base}/{endpoint}".format(base=prefix, endpoint=endpoint.strip("/"))
        else:
            api_path = "{base}/{endpoint}/".format(base=prefix, endpoint=endpoint.strip("/"))
        url = self.host_url._replace(path=api_path)
        if query_params:
            url = url._replace(query=urlencode(query_params))
        return url

    def build_ui_url(self, endpoint, query_params=None):
        """Return the URL of the given endpoint in the UI API.

        :param endpoint: Usually the API object name ("users", "groups", ...)
        :type endpoint: str
        :return: The full URL built from the given endpoint.
        :rtype: :py:class:``urllib.parse.ParseResult``
        """
        return self._build_url(self.ui_path_prefix, endpoint, query_params)

    def build_pulp_url(self, endpoint, query_params=None):
        """Return the URL of the given endpoint in the Pulp API.

        :param endpoint: Usually the API object name ("users", "groups", ...)
        :type endpoint: str
        :return: The full URL built from the given endpoint.
        :rtype: :py:class:``urllib.parse.ParseResult``
        """
        return self._build_url(self.pulp_path_prefix, endpoint, query_params)

    def make_request_raw_reponse(self, method, url, **kwargs):
        """Perform an API call and return the retrieved data.

        :param method: GET, PUT, POST, or DELETE
        :type method: str
        :param url: URL to the API endpoint
        :type url: :py:class:``urllib.parse.ParseResult``
        :param kwargs: Additionnal parameter to pass to the API (headers, data
                       for PUT and POST requests, ...)

        :raises AHAPIModuleError: The API request failed.

        :return: The reponse from the API call
        :rtype: :py:class:``http.client.HTTPResponse``
        """
        # In case someone is calling us directly; make sure we were given a method, let's not just assume a GET
        if not method:
            raise Exception("The HTTP method must be defined")

        # Extract the provided headers and data
        headers = kwargs.get("headers", {})
        data = json.dumps(kwargs.get("data", {}))

        # set default response
        response = {}

        try:
            response = self.session.open(method, url.geturl(), headers=headers, data=data)
        except SSLValidationError as ssl_err:
            raise AHAPIModuleError("Could not establish a secure connection to {host}: {error}.".format(host=url.netloc, error=ssl_err))
        except ConnectionError as con_err:
            raise AHAPIModuleError("Network error when trying to connect to {host}: {error}.".format(host=url.netloc, error=con_err))
        except HTTPError as he:
            # Sanity check: Did the server send back some kind of internal error?
            if he.code >= 500:
                raise AHAPIModuleError(
                    "The host sent back a server error: {path}: {error}. Please check the logs and try again later".format(path=url.path, error=he)
                )
            # Sanity check: Did we fail to authenticate properly?  If so, fail out now; this is always a failure.
            elif he.code == 401:
                raise AHAPIModuleError("Invalid authentication credentials for {path} (HTTP 401).".format(path=url.path))
            # Sanity check: Did we get a forbidden response, which means that the user isn't allowed to do this? Report that.
            elif he.code == 403:
                raise AHAPIModuleError("You do not have permission to {method} {path} (HTTP 403).".format(method=method, path=url.path))
            # Sanity check: Did we get a 404 response?
            # Requests with primary keys will return a 404 if there is no response, and we want to consistently trap these.
            elif he.code == 404:
                raise AHAPIModuleError("The requested object could not be found at {path}.".format(path=url.path))
            # Sanity check: Did we get a 405 response?
            # A 405 means we used a method that isn't allowed. Usually this is a bad request, but it requires special treatment because the
            # API sends it as a logic error in a few situations (e.g. trying to cancel a job that isn't running).
            elif he.code == 405:
                raise AHAPIModuleError("Cannot make a {method} request to this endpoint {path}".format(method=method, path=url.path))
            # Sanity check: Did we get some other kind of error?  If so, write an appropriate error message.
            elif he.code >= 400:
                # We are going to return a 400 so the module can decide what to do with it
                page_data = he.read()
                try:
                    return {"status_code": he.code, "json": json.loads(page_data)}
                # JSONDecodeError only available on Python 3.5+
                except ValueError:
                    return {"status_code": he.code, "text": page_data}
            elif he.code == 204 and method == "DELETE":
                # A 204 is a normal response for a delete function
                pass
            else:
                raise AHAPIModuleError("Unexpected return code when calling {url}: {error}".format(url=url.geturl(), error=he))
        except Exception as e:
            raise AHAPIModuleError(
                "There was an unknown error when trying to connect to {name}: {error} {url}".format(name=type(e).__name__, error=e, url=url.geturl())
            )

        return response

    def make_request(self, method, url, wait_for_task=True, **kwargs):
        """Perform an API call and return the data.

        :param method: GET, PUT, POST, or DELETE
        :type method: str
        :param url: URL to the API endpoint
        :type url: :py:class:``urllib.parse.ParseResult``
        :param kwargs: Additionnal parameter to pass to the API (headers, data
                       for PUT and POST requests, ...)

        :raises AHAPIModuleError: The API request failed.

        :return: A dictionnary with two entries: ``status_code`` provides the
                 API call returned code and ``json`` provides the returned data
                 in JSON format.
        :rtype: dict
        """
        response = self.make_request_raw_reponse(method, url, **kwargs)

        try:
            response_body = response.read()
        except Exception as e:
            if response["json"]["errors"]:
                raise AHAPIModuleError("Errors occurred with request (HTTP 400). Errors: {errors}".format(errors=response["json"]["errors"]))
            elif response["text"]:
                raise AHAPIModuleError("Errors occurred with request (HTTP 400). Errors: {errors}".format(errors=response["text"]))
            raise AHAPIModuleError("Failed to read response body: {error}".format(error=e))

        response_json = {}
        if response_body:
            try:
                response_json = json.loads(response_body)
            except Exception as e:
                raise AHAPIModuleError("Failed to parse the response json: {0}".format(e))

        # A background task has been triggered. Check if the task is completed
        if response.status == 202 and "task" in response_json and wait_for_task:
            url = url._replace(path=response_json["task"], query="")
            for _ in range(5):
                time.sleep(3)
                bg_task = self.make_request("GET", url)
                if "state" in bg_task["json"] and bg_task["json"]["state"].lower().startswith("complete"):
                    break
            else:
                if "state" in bg_task["json"]:
                    raise AHAPIModuleError(
                        "Failed to get the status of the remote task: {task}: last status: {status}".format(
                            task=response_json["task"], status=bg_task["json"]["state"]
                        )
                    )
                raise AHAPIModuleError("Failed to get the status of the remote task: {task}".format(task=response_json["task"]))

        return {"status_code": response.status, "json": response_json}

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

            {
                "detail":"Not found."
            }

        :param response: The response message from the API. This dictionary has
                         two keys: ``status_code`` provides the API call
                         returned code and ``json`` provides the returned data
                         in JSON format.
        :type response: dict

        :return: The error message or an empty string if the reponse does not
                 provide a message.
        :rtype: str
        """
        if not response or "json" not in response:
            return ""
        if "errors" in response["json"] and len(response["json"]["errors"]):
            if "detail" in response["json"]["errors"][0]:
                return response["json"]["errors"][0]["detail"]
            if "title" in response["json"]["errors"][0]:
                return response["json"]["errors"][0]["title"]
        if "detail" in response["json"]:
            return response["json"]["detail"]
        return ""

    def authenticate(self):
        """Authenticate with the API."""
        # curl -k -i  -X GET -H "Accept: application/json" -H "Content-Type: application/json" https://hub.lab.example.com/api/galaxy/_ui/v1/auth/login/

        # HTTP/1.1 204 No Content
        # Server: nginx/1.18.0
        # Date: Tue, 10 Aug 2021 07:33:37 GMT
        # Content-Length: 0
        # Connection: keep-alive
        # Vary: Accept, Cookie
        # Allow: GET, POST, HEAD, OPTIONS
        # X-Frame-Options: SAMEORIGIN
        # Set-Cookie: csrftoken=jvdb...kKHo; expires=Tue, 09 Aug 2022 07:33:37 GMT; Max-Age=31449600; Path=/; SameSite=Lax
        # Strict-Transport-Security: max-age=15768000

        url = self.build_ui_url("auth/login")
        try:
            response = self.make_request_raw_reponse("GET", url)
        except AHAPIModuleError as e:
            self.fail_json(msg="Authentication error: {error}".format(error=e))
        # Set-Cookie: csrftoken=jvdb...kKHo; expires=Tue, 09 Aug 2022 07:33:37 GMT
        for h in response.getheaders():
            if h[0].lower() == "set-cookie":
                k, v = h[1].split("=", 1)
                if k.lower() == "csrftoken":
                    header = {"X-CSRFToken": v.split(";", 1)[0]}
                    break
        else:
            header = {}

        # curl -k -i -X POST  -H 'referer: https://hub.lab.example.com' -H "Accept: application/json" -H "Content-Type: application/json"
        #      -H 'X-CSRFToken: jvdb...kKHo' --cookie 'csrftoken=jvdb...kKHo' -d '{"username":"admin","password":"redhat"}'
        #      https://hub.lab.example.com/api/galaxy/_ui/v1/auth/login/

        # HTTP/1.1 204 No Content
        # Server: nginx/1.18.0
        # Date: Tue, 10 Aug 2021 07:35:33 GMT
        # Content-Length: 0
        # Connection: keep-alive
        # Vary: Accept, Cookie
        # Allow: GET, POST, HEAD, OPTIONS
        # X-Frame-Options: SAMEORIGIN
        # Set-Cookie: csrftoken=6DVP...at9a; expires=Tue, 09 Aug 2022 07:35:33 GMT; Max-Age=31449600; Path=/; SameSite=Lax
        # Set-Cookie: sessionid=87b0iw12wyvy0353rk5fwci0loy5s615; expires=Tue, 24 Aug 2021 07:35:33 GMT; HttpOnly; Max-Age=1209600; Path=/; SameSite=Lax
        # Strict-Transport-Security: max-age=15768000

        try:
            try:
                response = self.make_request_raw_reponse("POST", url, data={"username": self.username, "password": self.password}, headers=header)
                for h in response.getheaders():
                    if h[0].lower() == "set-cookie":
                        k, v = h[1].split("=", 1)
                        if k.lower() == "csrftoken":
                            header = {"X-CSRFToken": v.split(";", 1)[0]}
                            self.headers.update(header)
                            break
            except AHAPIModuleError:
                test_url = self.build_ui_url("me")
                basic_str = base64.b64encode("{}:{}".format(self.username, self.password).encode("ascii"))
                header = {"Authorization": "Basic {}".format(basic_str.decode("ascii"))}
                response = self.make_request_raw_reponse("GET", test_url, headers=header)
                self.headers.update(header)
        except AHAPIModuleError as e:
            self.fail_json(msg="Authentication error: {error}".format(error=e))
        self.authenticated = True

    def getFileContent(self, path):
        try:
            with open(to_bytes(path, errors="surrogate_or_strict"), "rb") as f:
                b_file_data = f.read()
            return to_text(b_file_data)
        except FileNotFoundError:
            self.fail_json(msg="No such file found on the local filesystem: '{}'".format(path))

    def logout(self):
        if not self.authenticated:
            return

        url = self.build_ui_url("auth/logout")
        try:
            self.make_request_raw_reponse("POST", url)
        except AHAPIModuleError:
            pass
        self.headers = {"referer": self.host, "Content-Type": "application/json", "Accept": "application/json"}
        self.session = Request(validate_certs=self.verify_ssl, headers=self.headers)
        self.authenticated = False

    def fail_json(self, **kwargs):
        self.logout()
        super(AHAPIModule, self).fail_json(**kwargs)

    def exit_json(self, **kwargs):
        self.logout()
        super(AHAPIModule, self).exit_json(**kwargs)

    def get_server_version(self):
        """Return the automation hub/galaxy server version.

        :return: the server version ("4.2.5" for example) or an empty string if
                 that information is not available.
        :rtype: str
        """
        url = self._build_url(self.galaxy_path_prefix)
        try:
            response = self.make_request("GET", url)
        except AHAPIModuleError as e:
            self.fail_json(msg="Error while getting server version: {error}".format(error=e))
        if response["status_code"] != 200:
            error_msg = self.extract_error_msg(response)
            if error_msg:
                fail_msg = "Unable to get server version: {code}: {error}".format(code=response["status_code"], error=error_msg)
            else:
                fail_msg = "Unable to get server version: {code}".format(code=response["status_code"])
            self.fail_json(msg=fail_msg)
        return response["json"]["server_version"] if "server_version" in response["json"] else ""
