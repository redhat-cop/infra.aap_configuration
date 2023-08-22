# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Chris Renwick <@crenwick93>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    # Ansible Galaxy documentation fragment
    DOCUMENTATION = r"""
options:
  eda_host:
    description:
    - URL to Ansible Galaxy or EDA Controller instance.
    - If value not set, will try environment variable C(EDA_HOST)
    - If value not specified by any means, the value of C(127.0.0.1) will be used
    type: str
    aliases: [ eda_hostname ]
  eda_username:
    description:
    - Username for your Ansible Galaxy or EDA Controller instance.
    - If value not set, will try environment variable C(EDA_USERNAME)
    type: str
  eda_password:
    description:
    - Password for your Ansible Galaxy or EDA Controller instance.
    - If value not set, will try environment variable C(EDA_PASSWORD)
    type: str
  eda_token:
    description:
    - The Ansible Galaxy or EDA Controller API token to use.
    - This value can be in one of two formats.
    - A string which is the token itself. (i.e. bqV5txm97wqJqtkxlMkhQz0pKhRMMX)
    - A dictionary structure as returned by the eda_token module.
    - If value not set, will try environment variable C(EDA_API_TOKEN)
    type: raw
  validate_certs:
    description:
    - Whether to allow insecure connections to Galaxy or EDA Controller Server.
    - If C(no), SSL certificates will not be validated.
    - This should only be used on personally controlled sites using self-signed certificates.
    - If value not set, will try environment variable C(EDA_VERIFY_SSL)
    type: bool
    aliases: [ eda_verify_ssl ]
  request_timeout:
    description:
    - Specify the timeout Ansible should use in requests to the Galaxy or EDA Controller host.
    - Defaults to 10s, but this is handled by the shared module_utils code
    type: float
"""
