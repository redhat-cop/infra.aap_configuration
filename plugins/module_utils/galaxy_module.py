from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.urls import Request, SSLValidationError, ConnectionError
from ansible.module_utils.six import string_types
from ansible.module_utils.six import PY2
from ansible.module_utils.six.moves.urllib.parse import urlparse, urlencode
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.module_utils.six.moves.http_cookiejar import CookieJar
from socket import gethostbyname
import re
from os.path import split
from json import loads, dumps

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class ItemNotDefined(Exception):
    pass


class GalaxyModule(AnsibleModule):
    url = None
    session = None
    AUTH_ARGSPEC = dict(
        galaxy_server=dict(required=False, fallback=(env_fallback, ['GALAXY_SERVER'])),
        validate_certs=dict(type='bool', aliases=['galaxy_verify_ssl'], required=False, fallback=(env_fallback, ['GALAXY_VERIFY_SSL'])),
        galaxy_token=dict(type='str', no_log=True, required=False, fallback=(env_fallback, ['GALAXY_API_TOKEN'])),
    )
    ENCRYPTED_STRING = "$encrypted$"
    short_params = {
        'host': 'galaxy_server',
        'verify_ssl': 'validate_certs',
        'oauth_token': 'galaxy_token',
    }
    host = '127.0.0.1'
    verify_ssl = True
    oauth_token = None
    error_callback = None
    warn_callback = None

    def __init__(self, argument_spec=None, direct_params=None, error_callback=None, warn_callback=None, **kwargs):
        full_argspec = {}
        full_argspec.update(GalaxyModule.AUTH_ARGSPEC)
        full_argspec.update(argument_spec)
        kwargs['supports_check_mode'] = True

        self.error_callback = error_callback
        self.warn_callback = warn_callback

        self.json_output = {'changed': False}

        if direct_params is not None:
            self.params = direct_params
        else:
            super(GalaxyModule, self).__init__(argument_spec=full_argspec, direct_params=direct_params,
                                                error_callback=error_callback, warn_callback=warn_callback, **kwargs)
            self.session = Request(cookies=CookieJar(), validate_certs=self.verify_ssl)

        # Parameters specified on command line will override settings in any config
        for short_param, long_param in self.short_params.items():
            direct_value = self.params.get(long_param)
            if direct_value is not None:
                setattr(self, short_param, direct_value)

        # Perform magic checking whether galaxy_token is a string
        if self.params.get('galaxy_token'):
            token_param = self.params.get('galaxy_token')
            if isinstance(token_param, string_types):
                self.oauth_token = self.params.get('galaxy_token')
            else:
                error_msg = "The provided galaxy_token type was not valid ({0}). Valid options are str or dict.".format(type(token_param).__name__)
                self.fail_json(msg=error_msg)

        # Perform some basic validation
        if not re.match('^https{0,1}://', self.host):
            self.host = "https://{0}".format(self.host)

        # Try to parse the hostname as a url
        try:
            self.url = urlparse(self.host)
        except Exception as e:
            self.fail_json(msg="Unable to parse galaxy host as a URL ({1}): {0}".format(self.host, e))

        # Try to resolve the hostname
        hostname = self.url.netloc.split(':')[0]
        try:
            gethostbyname(hostname)
        except Exception as e:
            self.fail_json(msg="Unable to resolve galaxy host ({1}): {0}".format(hostname, e))

    def build_url(self, endpoint, query_params=None):
        # Make sure we start with /api/vX
        if not endpoint.startswith("/"):
            endpoint = "/{0}".format(endpoint)
        if not endpoint.startswith("/api/"):
            endpoint = "api/automation-hub/v3{0}".format(endpoint)
        if not endpoint.endswith('/') and '?' not in endpoint:
            endpoint = "{0}/".format(endpoint)

        # Update the URL path with the endpoint
        url = self.url._replace(path=endpoint)

        if query_params:
            url = url._replace(query=urlencode(query_params))

        return url

    def fail_json(self, **kwargs):
        # Try to log out if we are authenticated
        if self.error_callback:
            self.error_callback(**kwargs)
        else:
            super(GalaxyModule, self).fail_json(**kwargs)

    def exit_json(self, **kwargs):
        # Try to log out if we are authenticated
        super(GalaxyModule, self).exit_json(**kwargs)

    def warn(self, warning):
        if self.warn_callback is not None:
            self.warn_callback(warning)
        else:
            super(GalaxyModule, self).warn(warning)

    @staticmethod
    def get_name_field_from_endpoint(endpoint):
        return GalaxyModule.IDENTITY_FIELDS.get(endpoint, 'name')

    def get_endpoint(self, endpoint, *args, **kwargs):
        return self.make_request('GET', endpoint, **kwargs)

    def make_request(self, method, endpoint, *args, **kwargs):
        # In case someone is calling us directly; make sure we were given a method, let's not just assume a GET
        if not method:
            raise Exception("The HTTP method must be defined")

        if method in ['POST', 'PUT', 'PATCH']:
            url = self.build_url(endpoint)
        else:
            url = self.build_url(endpoint, query_params=kwargs.get('data'))

        # Extract the headers, this will be used in a couple of places
        headers = kwargs.get('headers', {})

        # Authenticate to Automation Hub
        if self.oauth_token:
            # If we have a oauth token, we just use a token header
            headers['Authorization'] = 'token {0}'.format(self.oauth_token)

        if method in ['POST', 'PUT', 'PATCH']:
            headers.setdefault('Content-Type', 'application/json')
            kwargs['headers'] = headers

        data = None  # Important, if content type is not JSON, this should not be dict type
        if headers.get('Content-Type', '') == 'application/json':
            data = dumps(kwargs.get('data', {}))

        try:
            response = self.session.open(method, url.geturl(), headers=headers, validate_certs=self.verify_ssl, follow_redirects=True, data=data)
        except(SSLValidationError) as ssl_err:
            self.fail_json(msg="Could not establish a secure connection to your host ({1}): {0}.".format(url.netloc, ssl_err))
        except(ConnectionError) as con_err:
            self.fail_json(msg="There was a network error of some kind trying to connect to your host ({1}): {0}.".format(url.netloc, con_err))
        except(HTTPError) as he:
            # Sanity check: Did the server send back some kind of internal error?
            if he.code >= 500:
                self.fail_json(msg='The host sent back a server error ({1}): {0}. Please check the logs and try again later'.format(url.path, he))
            # Sanity check: Did we fail to authenticate properly?  If so, fail out now; this is always a failure.
            elif he.code == 401:
                self.fail_json(msg='Invalid Automation Hub authentication credentials for {0} (HTTP 401).'.format(url.path))
            # Sanity check: Did we get a forbidden response, which means that the user isn't allowed to do this? Report that.
            elif he.code == 403:
                self.fail_json(msg="You don't have permission to {1} to {0} (HTTP 403).".format(url.path, method))
            # Sanity check: Did we get a 404 response?
            # Requests with primary keys will return a 404 if there is no response, and we want to consistently trap these.
            elif he.code == 404:
                if kwargs.get('return_none_on_404', False):
                    return None
                self.fail_json(msg='The requested object could not be found at {0}.'.format(url.path))
            # Sanity check: Did we get a 405 response?
            # A 405 means we used a method that isn't allowed. Usually this is a bad request, but it requires special treatment because the
            # API sends it as a logic error in a few situations (e.g. trying to cancel a job that isn't running).
            elif he.code == 405:
                self.fail_json(msg="The Automation Hub server says you can't make a request with the {0} method to this endpoing {1}".format(method, url.path))
            # Sanity check: Did we get some other kind of error?  If so, write an appropriate error message.
            elif he.code >= 400:
                # We are going to return a 400 so the module can decide what to do with it
                page_data = he.read()
                try:
                    return {'status_code': he.code, 'json': loads(page_data)}
                # JSONDecodeError only available on Python 3.5+
                except ValueError:
                    return {'status_code': he.code, 'text': page_data}
            elif he.code == 204 and method == 'DELETE':
                # A 204 is a normal response for a delete function
                pass
            else:
                self.fail_json(msg="Unexpected return code when calling {0}: {1}".format(url.geturl(), he))
        except(Exception) as e:
            self.fail_json(msg="There was an unknown error when trying to connect to {2}: {0} {1}".format(type(e).__name__, e, url.geturl()))

        if not self.version_checked:
            # In PY2 we get back an HTTPResponse object but PY2 is returning an addinfourl
            # First try to get the headers in PY3 format and then drop down to PY2.
            try:
                tower_type = response.getheader('X-API-Product-Name', None)
                tower_version = response.getheader('X-API-Product-Version', None)
            except Exception:
                tower_type = response.info().getheader('X-API-Product-Name', None)
                tower_version = response.info().getheader('X-API-Product-Version', None)

            if self._COLLECTION_TYPE not in self.collection_to_version or self.collection_to_version[self._COLLECTION_TYPE] != tower_type:
                self.warn("You are using the {0} version of this collection but connecting to {1}".format(
                    self._COLLECTION_TYPE, tower_type
                ))
            elif self._COLLECTION_VERSION != tower_version:
                self.warn("You are running collection version {0} but connecting to tower version {1}".format(
                    self._COLLECTION_VERSION, tower_version
                ))
            self.version_checked = True

        response_body = ''
        try:
            response_body = response.read()
        except(Exception) as e:
            self.fail_json(msg="Failed to read response body: {0}".format(e))

        response_json = {}
        if response_body and response_body != '':
            try:
                response_json = loads(response_body)
            except(Exception) as e:
                self.fail_json(msg="Failed to parse the response json: {0}".format(e))

        if PY2:
            status_code = response.getcode()
        else:
            status_code = response.status
        return {'status_code': status_code, 'json': response_json}

    def get_one(self, endpoint, name_or_id=None, allow_none=True, **kwargs):
        new_kwargs = kwargs.copy()
        if name_or_id:
            name_field = self.get_name_field_from_endpoint(endpoint)
            new_data = kwargs.get('data', {}).copy()
            if name_field in new_data:
                self.fail_json(msg="You can't specify the field {0} in your search data if using the name_or_id field".format(name_field))

            try:
                new_data['or__id'] = int(name_or_id)
                new_data['or__{0}'.format(name_field)] = name_or_id
            except ValueError:
                # If we get a value error, then we didn't have an integer so we can just pass and fall down to the fail
                new_data[name_field] = name_or_id
            new_kwargs['data'] = new_data

        response = self.get_endpoint(endpoint, **new_kwargs)
        if response['status_code'] != 200:
            fail_msg = "Got a {0} response when trying to get one from {1}".format(response['status_code'], endpoint)
            if 'detail' in response.get('json', {}):
                fail_msg += ', detail: {0}'.format(response['json']['detail'])
            self.fail_json(msg=fail_msg)

        if 'count' not in response['json'] or 'results' not in response['json']:
            self.fail_json(msg="The endpoint did not provide count and results")

        if response['json']['count'] == 0:
            if allow_none:
                return None
            else:
                self.fail_wanted_one(response, endpoint, new_kwargs.get('data'))
        elif response['json']['count'] > 1:
            if name_or_id:
                # Since we did a name or ID search and got > 1 return something if the id matches
                for asset in response['json']['results']:
                    if str(asset['id']) == name_or_id:
                        return asset
            # We got > 1 and either didn't find something by ID (which means multiple names)
            # Or we weren't running with a or search and just got back too many to begin with.
            self.fail_wanted_one(response, endpoint, new_kwargs.get('data'))

        return response['json']['results'][0]

    def delete_if_needed(self, existing_item, on_delete=None, auto_exit=True):
        # This will exit from the module on its own.
        # If the method successfully deletes an item and on_delete param is defined,
        #   the on_delete parameter will be called as a method pasing in this object and the json from the response
        # This will return one of two things:
        #   1. None if the existing_item is not defined (so no delete needs to happen)
        #   2. The response from Tower from calling the delete on the endpont. It's up to you to process the response and exit from the module
        # Note: common error codes from the Tower API can cause the module to fail
        if existing_item:
            # If we have an item, we can try to delete it
            try:
                item_url = existing_item['url']
                item_type = existing_item['type']
                item_id = existing_item['id']
                item_name = self.get_item_name(existing_item, allow_unknown=True)
            except KeyError as ke:
                self.fail_json(msg="Unable to process delete of item due to missing data {0}".format(ke))

            response = self.delete_endpoint(item_url)

            if response['status_code'] in [202, 204]:
                if on_delete:
                    on_delete(self, response['json'])
                self.json_output['changed'] = True
                self.json_output['id'] = item_id
                self.exit_json(**self.json_output)
                if auto_exit:
                    self.exit_json(**self.json_output)
                else:
                    return self.json_output
            else:
                if 'json' in response and '__all__' in response['json']:
                    self.fail_json(msg="Unable to delete {0} {1}: {2}".format(item_type, item_name, response['json']['__all__'][0]))
                elif 'json' in response:
                    # This is from a project delete (if there is an active job against it)
                    if 'error' in response['json']:
                        self.fail_json(msg="Unable to delete {0} {1}: {2}".format(item_type, item_name, response['json']['error']))
                    else:
                        self.fail_json(msg="Unable to delete {0} {1}: {2}".format(item_type, item_name, response['json']))
                else:
                    self.fail_json(msg="Unable to delete {0} {1}: {2}".format(item_type, item_name, response['status_code']))
        else:
            if auto_exit:
                self.exit_json(**self.json_output)
            else:
                return self.json_output

    def get_item_name(self, item, allow_unknown=False):
        if item:
            if 'name' in item:
                return item['name']

        if allow_unknown:
            return 'unknown'

        if item:
            self.exit_json(msg='Cannot determine identity field for {0} object.'.format(item.get('type', 'unknown')))
        else:
            self.exit_json(msg='Cannot determine identity field for Undefined object.')

    def delete_endpoint(self, endpoint, *args, **kwargs):
        # Handle check mode
        if self.check_mode:
            self.json_output['changed'] = True
            self.exit_json(**self.json_output)

        return self.make_request('DELETE', endpoint, **kwargs)

    def create_or_update_if_needed(
        self, existing_item, new_item, endpoint=None, item_type='unknown', on_create=None, on_update=None, auto_exit=True, associations=None
    ):
        if existing_item:
            return self.update_if_needed(existing_item, new_item, on_update=on_update, auto_exit=auto_exit, associations=associations)
        else:
            return self.create_if_needed(
                existing_item, new_item, endpoint, on_create=on_create, item_type=item_type, auto_exit=auto_exit, associations=associations)

    def create_if_needed(self, existing_item, new_item, endpoint, on_create=None, auto_exit=True, item_type='unknown', associations=None):

        # This will exit from the module on its own
        # If the method successfully creates an item and on_create param is defined,
        #    the on_create parameter will be called as a method pasing in this object and the json from the response
        # This will return one of two things:
        #    1. None if the existing_item is already defined (so no create needs to happen)
        #    2. The response from Tower from calling the patch on the endpont. It's up to you to process the response and exit from the module
        # Note: common error codes from the Galaxy API can cause the module to fail

        if not endpoint:
            self.fail_json(msg="Unable to create new {0} due to missing endpoint".format(item_type))

        item_url = None
        if existing_item:
            try:
                item_url = existing_item['url']
            except KeyError as ke:
                self.fail_json(msg="Unable to process create of item due to missing data {0}".format(ke))
        else:
            # If we don't have an exisitng_item, we can try to create it

            # We have to rely on item_type being passed in since we don't have an existing item that declares its type
            # We will pull the item_name out from the new_item, if it exists
            item_name = self.get_item_name(new_item, allow_unknown=True)

            response = self.post_endpoint(endpoint, **{'data': new_item})

            if response['status_code'] in [201]:
                self.json_output['name'] = 'unknown'
                for key in ('name', 'username', 'identifier', 'hostname'):
                    if key in response['json']:
                        self.json_output['name'] = response['json'][key]
                self.json_output['id'] = response['json']['id']
                self.json_output['changed'] = True
                item_url = response['json']['url']
            else:
                if 'json' in response and '__all__' in response['json']:
                    self.fail_json(msg="Unable to create {0} {1}: {2}".format(item_type, item_name, response['json']['__all__'][0]))
                elif 'json' in response:
                    self.fail_json(msg="Unable to create {0} {1}: {2}".format(item_type, item_name, response['json']))
                else:
                    self.fail_json(msg="Unable to create {0} {1}: {2}".format(item_type, item_name, response['status_code']))

        # Process any associations with this item
        if associations is not None:
            for association_type in associations:
                sub_endpoint = '{0}{1}/'.format(item_url, association_type)
                self.modify_associations(sub_endpoint, associations[association_type])

        # If we have an on_create method and we actually changed something we can call on_create
        if on_create is not None and self.json_output['changed']:
            on_create(self, response['json'])
        elif auto_exit:
            self.exit_json(**self.json_output)
        else:
            last_data = response['json']
            return last_data

    def update_if_needed(self, existing_item, new_item, on_update=None, auto_exit=True, associations=None):
        # This will exit from the module on its own
        # If the method successfully updates an item and on_update param is defined,
        #   the on_update parameter will be called as a method pasing in this object and the json from the response
        # This will return one of two things:
        #    1. None if the existing_item does not need to be updated
        #    2. The response from Tower from patching to the endpoint. It's up to you to process the response and exit from the module.
        # Note: common error codes from the Tower API can cause the module to fail
        response = None
        if existing_item:

            # If we have an item, we can see if it needs an update
            try:
                item_url = existing_item['url']
                item_type = existing_item['type']
                item_name = existing_item['name']
                item_id = existing_item['id']
            except KeyError as ke:
                self.fail_json(msg="Unable to process update of item due to missing data {0}".format(ke))

            # Check to see if anything within the item requires the item to be updated
            needs_patch = self.objects_could_be_different(existing_item, new_item)

            # If we decided the item needs to be updated, update it
            self.json_output['id'] = item_id
            if needs_patch:
                response = self.patch_endpoint(item_url, **{'data': new_item})
                if response['status_code'] == 200:
                    # compare apples-to-apples, old API data to new API data
                    # but do so considering the fields given in parameters
                    self.json_output['changed'] = self.objects_could_be_different(
                        existing_item, response['json'], field_set=new_item.keys(), warning=True)
                elif 'json' in response and '__all__' in response['json']:
                    self.fail_json(msg=response['json']['__all__'])
                else:
                    self.fail_json(**{'msg': "Unable to update {0} {1}, see response".format(item_type, item_name), 'response': response})

        else:
            raise RuntimeError('update_if_needed called incorrectly without existing_item')

        # Process any associations with this item
        if associations is not None:
            for association_type, id_list in associations.items():
                endpoint = '{0}{1}/'.format(item_url, association_type)
                self.modify_associations(endpoint, id_list)

        # If we change something and have an on_change call it
        if on_update is not None and self.json_output['changed']:
            if response is None:
                last_data = existing_item
            else:
                last_data = response['json']
            on_update(self, last_data)
        elif auto_exit:
            self.exit_json(**self.json_output)
        else:
            if response is None:
                last_data = existing_item
            else:
                last_data = response['json']
            return last_data

    def modify_associations(self, association_endpoint, new_association_list):
        # if we got None instead of [] we are not modifying the association_list
        if new_association_list is None:
            return

        # First get the existing associations
        response = self.get_all_endpoint(association_endpoint)
        existing_associated_ids = [association['id'] for association in response['json']['results']]

        # Disassociate anything that is in existing_associated_ids but not in new_association_list
        ids_to_remove = list(set(existing_associated_ids) - set(new_association_list))
        for an_id in ids_to_remove:
            response = self.post_endpoint(association_endpoint, **{'data': {'id': int(an_id), 'disassociate': True}})
            if response['status_code'] == 204:
                self.json_output['changed'] = True
            else:
                self.fail_json(msg="Failed to disassociate item {0}".format(response['json'].get('detail', response['json'])))

        # Associate anything that is in new_association_list but not in `association`
        for an_id in list(set(new_association_list) - set(existing_associated_ids)):
            response = self.post_endpoint(association_endpoint, **{'data': {'id': int(an_id)}})
            if response['status_code'] == 204:
                self.json_output['changed'] = True
            else:
                self.fail_json(msg="Failed to associate item {0}".format(response['json'].get('detail', response['json'])))

    def post_endpoint(self, endpoint, *args, **kwargs):
        # Handle check mode
        if self.check_mode:
            self.json_output['changed'] = True
            self.exit_json(**self.json_output)

        return self.make_request('POST', endpoint, **kwargs)

    def patch_endpoint(self, endpoint, *args, **kwargs):
        # Handle check mode
        if self.check_mode:
            self.json_output['changed'] = True
            self.exit_json(**self.json_output)

        return self.make_request('PATCH', endpoint, **kwargs)

    def get_all_endpoint(self, endpoint, *args, **kwargs):
        response = self.get_endpoint(endpoint, *args, **kwargs)
        if 'next' not in response['json']:
            raise RuntimeError('Expected list from API at {0}, got: {1}'.format(endpoint, response))
        next_page = response['json']['next']

        if response['json']['count'] > 10000:
            self.fail_json(msg='The number of items being queried for is higher than 10,000.')

        while next_page is not None:
            next_response = self.get_endpoint(next_page)
            response['json']['results'] = response['json']['results'] + next_response['json']['results']
            next_page = next_response['json']['next']
            response['json']['next'] = next_page
        return response