# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Sean Sullivan <@sean-m-sullivan>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    # Ansible Galaxy documentation fragment
    DOCUMENTATION = r'''
options:
  galaxy_server:
    description:
    - URL to Ansible Galaxy or Automation Hub instance.
    - If value not set, will try environment variable C(GALAXY_SERVER)
    type: str
  galaxy_token:
    description:
    - The Ansible Galaxy or Automation Hub API token to use.
    - A string which is the token itself. (i.e. bqV5txm97wqJqtkxlMkhQz0pKhRMMX)
    - If value not set, will try environment variable C(GALAXY_API_TOKEN)
    type: str
  validate_certs:
    description:
    - Whether to allow insecure connections to Galaxy or Automation Hub Server.
    - If C(no), SSL certificates will not be validated.
    - This should only be used on personally controlled sites using self-signed certificates.
    - If value not set, will try environment variable C(GALAXY_VERIFY_SSL) and then config files
    type: bool
    aliases: [ galaxy_verify_ssl ]
'''
