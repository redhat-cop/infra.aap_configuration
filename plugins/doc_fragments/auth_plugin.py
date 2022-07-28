# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Ansible by Red Hat, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    # Automation Platform Controller documentation fragment
    DOCUMENTATION = r"""
options:
  host:
    description: The network address of your Automation Hub host.
    env:
    - name: AH_HOST
  username:
    description: The user that you plan to use to access inventories on the AH.
    env:
    - name: AH_USERNAME
  password:
    description: The password for your controller user.
    env:
    - name: AH_PASSWORD
  oauth_token:
    description:
    - The OAuth token to use.
    env:
    - name: AH_OAUTH_TOKEN
  path_prefix:
    description:
    - API path used to access the api.
    - For galaxy_ng this is either 'automation-hub' or the custom prefix used on install with GALAXY_API_PATH_PREFIX
    - For Automation Hub this is 'galaxy'
  verify_ssl:
    description:
    - Specify whether Ansible should verify the SSL certificate of the AH host.
    - Defaults to True, but this is handled by the shared module_utils code
    type: bool
    env:
    - name: AH_VERIFY_SSL
    aliases: [ validate_certs ]
"""
