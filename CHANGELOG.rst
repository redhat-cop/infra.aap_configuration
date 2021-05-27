=========================================
redhat_cop.ah_configuration Release Notes
=========================================

.. contents:: Topics


v0.3.1
======

Bugfixes
--------

- Fixes issue in ah_repository where not specifying a requirements list causedd a failure.

v0.3.0
======

Major Changes
-------------

- Added ah_repository module to configure the remote repositories for Automation Hub.

v0.2.0
======

Major Changes
-------------

- Added ah_approval module to approve a colelction which has been uploaded.
- Added ah_collection_uploads module
- Publish role - Ability to approve role added
- Publish role - rewritten to use internal modules

Breaking Changes / Porting Guide
--------------------------------

- Publish role - repo_name variable renamed to collection_name.

v0.1.0
======

Major Changes
-------------

- Initial release of ansible_config, namespace, publish roles and ah_namespace, ah_token modules
