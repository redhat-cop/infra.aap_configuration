# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Ansible by Red Hat, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    # Automation Platform EDA Controller documentation fragment
    DOCUMENTATION = r"""
options:
  host:
    description: The network address of your EDA Controller host.
    env:
    - name: EDA_HOST
  username:
    description: The user that you plan to use to access EDA Controller.
    env:
    - name: EDA_USERNAME
  password:
    description: The password for your EDA Controller user.
    env:
    - name: EDA_PASSWORD
  request_timeout:
    description:
    - Specify the timeout Ansible should use in requests to the EDA Controller host.
    - Defaults to 10 seconds
    type: float
    env:
    - name: EDA_REQUEST_TIMEOUT
  verify_ssl:
    description:
    - Specify whether Ansible should verify the SSL certificate of the EDA Controller host.
    - Defaults to True, but this is handled by the shared module_utils code
    type: bool
    env:
    - name: EDA_VERIFY_SSL
    aliases: [ validate_certs ]
"""
