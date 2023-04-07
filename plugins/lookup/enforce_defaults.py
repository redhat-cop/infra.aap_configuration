# (c) 2020 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
name: enforce_defaults
author: "Sean Sullivan (@sean-m-sullivan)"
version_added: "2.3.2"
short_description: Return difference for objects from Controller API
requirements:
  - None
description:
  - This plugin is used to return what the default value should be depending on conditions.
  - If enforce default is true, it will return the default value. Otherwise it will return the omit.
  - This is so the value used for the default filter can be turned on and off.
options:
  enforce_default:
    description: Whether to enforce the default value or use omit.
    type: bool
    default: False
  default_value:
    description:
      - Value to supply if enforce_default is True.
      - This should be empty value or some form of string.
    default: ''
  omit_value:
    description:
      - the omit value
    type: str
    default: ''
"""

EXAMPLES = """
- name: Test Filter
  ansible.builtin.debug:
    msg: "{{ nothing | default(lookup('infra.controller_configuration.enforce_defaults', enforce_default=false , default_value='', omit_value=omit), false) }}"

"""

RETURN = """
_raw:
  description:
    - Will either return the omit value, or the default value.
"""

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError, AnsibleLookupError
from ansible.module_utils._text import to_native
from ansible.utils.display import Display


class LookupModule(LookupBase):
    display = Display()

    def handle_error(self, **kwargs):
        raise AnsibleError(to_native(kwargs.get("msg")))

    def warn_callback(self, warning):
        self.display.warning(warning)

    def run(self, terms, variables=None, **kwargs):
        self.set_options(direct=kwargs)

        # Set Variables for user input
        enforce_default = self.get_option("enforce_default")
        default_value = self.get_option("default_value")
        omit_value = self.get_option("omit_value")

        if enforce_default:
            return [default_value]
        else:
            return [omit_value]
