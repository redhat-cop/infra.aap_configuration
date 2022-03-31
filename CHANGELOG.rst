=================================================
redhat_cop.controller_configuration Release Notes
=================================================

.. contents:: Topics


v2.1.4
======

Bugfixes
--------

- Fixes async to work on default execution enviroments.
- Fixes inventories hardcoded 'no_log' true on the async job check task.

v2.1.3
======

Minor Changes
-------------

- Added asynchronous to {organizations,credentials,credential_types,inventories,job_templates} task to speed up creation.
- Allow setting the organization when creating users.
- Update to controller_object_diff lookup plugin to better handle group, host, inventory, credential, workflow_job_template_node and user objects.
- Update to controller_object_diff lookup plugin to better handle organizations.

Breaking Changes / Porting Guide
--------------------------------

- galaxy credentials in the organization role now require assign_galaxy_organizations_to_org to be true.

Bugfixes
--------

- Fixes option of `survey_spec` on job_templates role.

v2.1.1
======

Minor Changes
-------------

- Allows for using the roles for deletion to only use required fields.
- Changed default to omit for several fields for notification templates and inventor sources.
- These changes are in line with the modules required fields.

Bugfixes
--------

- warn on default if the api list fed to controller_object_diff lookup is empty

v2.1.0
======

Major Changes
-------------

- added diff plugin and tests for diff plugin to aid in removal tasks

Minor Changes
-------------

- Added new options for adding manifest to Ansible Controller inc. from a URL and from b64 encoded content
- added tests for the project and inventory source skips

Bugfixes
--------

- Fixed readme's to point in right direction for workflows and the export model in examples
- Moved Example playbooks to the example directory
- Removes json_query which is not in a RH Certified collection so does not receive support and replaced with native ansible filters
- Updated workflow inventory option to be able to use workflows from the export model.
- added default to organization as null on project as it is not required for the module, but it is highly recommended.
- added when to skip inventory source update when item is absent
- added when to skip project update when item is absent

v2.0.0
======

Major Changes
-------------

- Created awx and controller playbook that users can invoke for using the collection

Minor Changes
-------------

- Additional module options have been added such as instance_groups and copy_from where applicable.
- All role tests have been converted to use one format.
- Created Readme for playbook in the playbooks directory
- Removed the playbook configs folder, it was previously moved to the .github/playbooks directory

Breaking Changes / Porting Guide
--------------------------------

- All references to tower have been changed to Controller.
- Changed all module names to be in line with changes to awx.awx as of 19.2.1.
- Changed variable names for all objects from tower_* to controller_*.
- Removed depreciated module options for notification Templates.

Bugfixes
--------

- Changed all references for ansible.tower to ansible.controller
- Fixed issue where `credential` was not working for project and instead the old `scm_credential` option remained.

v1.5.0
======

Major Changes
-------------

- Removed testing via playbook install that was removed in awx 18.0.0.
- Updated testing via playbook to use minikube + operator install.

Breaking Changes / Porting Guide
--------------------------------

- Examples can also be found in the playbooks/tower_configs_export_model/tower_workflows.yml
- If you do not change the data model, change the variable 'workflow_nodes' to 'simplified_workflow_nodes'.
- More information can be found either in the Workflow Job Template Readme or on the awx.awx.tower_workflow_job_template Documentation.
- The Tower export model is now the default to use under workflow nodes. This is documented in the workflow job templates Readme.
- Users using the tower export model previously, do not need to make any changes.
- Workflow Schemas to describe Workflow nodes have changed.

Bugfixes
--------

- Allow tower_hostname and tower_validate_certs to not be set in favour of environment variables being set as per module defaults.
- Changes all boolean variables to have their default values omitted rather than using the value 'default(omit, true)' which prevents a falsy value being supplied.

v1.4.1
======

Major Changes
-------------

- Added execution environments option for multiple roles.
- Added execution environments role.

Bugfixes
--------

- Fix tower_templates default

v1.3.0
======

Bugfixes
--------

- Fixed an issue where certain roles were not taking in tower_validate_certs

v1.2.0
======

Breaking Changes / Porting Guide
--------------------------------

- removed awx.awx implicit dependency, it will now be required to manually install awx.awx or ansible.tower collection

v1.1.0
======

Major Changes
-------------

- Added the following roles - ad_hoc_command, ad_hoc_command_cancel, inventory_source_update, job_launch, job_cancel, project_update, workflow_launch
- Updated collection to use and comply with ansible-lint v5

Minor Changes
-------------

- Fixed default filters to use true when neccessary and changed a few defaults to omit rather then a value or empty string.
- updated various Readmes to fix typos and missing information.

Breaking Changes / Porting Guide
--------------------------------

- Removed kind from to credentials role. This will be depreciated in a few months. Kind arguments are replaced by the credential_type and inputs fields.
- Updated to allow use of either awx.awx or ansible.tower

Bugfixes
--------

- Corrected README for tower_validate_certs variable defaults on all roles

v1.0.2
======

Minor Changes
-------------

- added alias option for survey to survey_spec in workflows.
- updated documentation on surveys for workflows and job templates

v1.0.0
======

Major Changes
-------------

- Updated Roles to use the tower_export model from the awx command line.
- credential_types Updated to use the tower_export model from the awx command line.
- credentials Updated to use the tower_export model from the awx command line.
- inventory Updated to use the tower_export model from the awx command line.
- inventory_sources Updated to use the tower_export model from the awx command line.
- job_templates Updated to use the tower_export model from the awx command line.
- projects Updated to use the tower_export model from the awx command line.
- teams Updated to use the tower_export model from the awx command line.
- users Updated to use the tower_export model from the awx command line.

Minor Changes
-------------

- updated to allow vars in messages for notifications.
- updated tower workflows related role `workflow_job_templates` to include `survey_enabled` defaulting to `false` which is a module default and `omit` the `survey_spec` if not passed.
- updated various roles to include oauth token and tower config file.

Breaking Changes / Porting Guide
--------------------------------

- Removed depreciated options in inventory sources role (source_regions, instance_filters, group_by)
- Renamed notifications role to notification_templates role as in awx.awx:15.0. The variable is not tower_notification_templates.

v0.2.1
======

Minor Changes
-------------

- Changelog release cycle

v0.2.0
======

Minor Changes
-------------

- Added pre-commit hook for local development and automated testing purposes
- Standardised and corrected all READMEs

Bugfixes
--------

- Removed defaulted objects for all roles so that they were not always run if using a conditional against the variable. (see https://github.com/redhat-cop/tower_configuration/issues/68)

v0.1.0
======

Major Changes
-------------

- Groups role - Added groups role to the collection
- Labels role - Added labels role to the collection
- Notifications role - Added many options to notifications role
- Workflow Job Templates role - Added many options to WJT role

Minor Changes
-------------

- GitHub Workflows - Added workflows to run automated linting and integration tests against the codebase
- Hosts role - Added new_name and enabled options to hosts role
- Housekeeping - Added CONTRIBUTING guide and pull request template
- Inventory Sources role - Added notification_templates_started, success, and error options. Also added verbosity and source_regions options.
- Teams role - Added new_name option to teams role
- Test Configs - Added full range of test objects for integration testing

Bugfixes
--------

- Fixed an issue where tower_validate_certs and validate_certs were both used as vars. Now changed to tower_validate_certs
