=========================================
redhat_cop.ah_configuration Release Notes
=========================================

.. contents:: Topics


v0.4.3
======

Minor Changes
-------------

- Added meta/runtime.yml file which is now a requirement for collections to be released on Galaxy
- Added requirements_file option to ah_repository module

v0.4.1
======

Bugfixes
--------

- Now retries auto-approving on the publish role in case there is a delay in the collection making it to be ready for approval.

v0.4.0
======

Major Changes
-------------

- Added ah_repository_sync module to sync remote repositories for Automation Hub.

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
