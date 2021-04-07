#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2020, Tom Page <@Tompage1994>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


ANSIBLE_METADATA = {"metadata_version": "1.1", "status": ["preview"], "supported_by": "community"}


DOCUMENTATION = """
---
module: ah_build
author: "Tom Page (@Tompage1994)"
short_description: Build a collection tar.
description:
    - Build a collection tar ready for Automation Hub. See
      U(https://www.ansible.com/) for an overview.
options:
    path:
      description:
        - Path to the collection(s) directory to build.
          This should be the directory that contains the galaxy.yml file.
          The default is the current working directory.
      required: False
      type: str
      default: "."
    force:
      description:
        - Whether to force the build to take place.
      required: False
      type: str
      default: false
    output_path:
      description:
        - he path in which the collection is built to. The default is the current working directory.
      required: False
      type: str
      default: "."

"""


EXAMPLES = """
- name: Build redhat_cop.ah_configuration:v1.0.0
  ah_build:
    path: /home/ansible/ah_configuration
    force: true
    output_path: /var/tmp

"""

from ..module_utils.ah_module import AHModule


def main():
    # Any additional arguments that are not fields of the item can be added here
    argument_spec = dict(path=dict(required=False, default="."), force=dict(type="bool"), output_path=dict(required=False, default="."))

    # Create a module for ourselves
    module = AHModule(argument_spec=argument_spec, require_auth=False)

    # Extract our parameters
    path = module.params.get("path")
    force = module.params.get("force")
    output_path = module.params.get("output_path")

    module.execute_build(path, force, output_path)


if __name__ == "__main__":
    main()
