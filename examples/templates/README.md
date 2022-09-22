# Controller Configuration

A single playbook and multiple task and vars files which can be used to define your Tower or Controller configuration as code.  Update the vars files to define your objects and run the playbook to deploy your changes to your Tower / AAP 2.1 cluster(s).

If executed with the `alltags` tag then the playbook will create all objects defined in all vars files in the appropriate order.

Use of some tags may require that you include other tags; for example if adding a project but you haven't already added the correct SCM credential.

Available tags:

- alltags
- settings
- credtypes
- orgs
- users
- teams
- credentials
- projects
- labels
- inventory
- inventorysources
- instancegroups
- hosts
- groups
- ees
- notifications
- jobtemplates
- workflows
- schedules
- roles

## Requirements

This content utilizes the controller_configuration collection and the awx.awx or ansible.tower or ansible.controller collections.  You will need connectivity to a Private Automation Hub server which has synchronized these collections or to the internet so that the collections can be installed.

You will also need Tower or Controller credentials with sufficient permissions to create the objects you define as code.  This will need to be a local account within the cluster and not an externally (such as ldap) authenticated account.

## Variables

`controller_config.yml`:

    absent_present

        I suggest leaving `absent_present` set to "present".

    which_org

        You can update `which_org` to specify your org within the cluster and just create all objects in a single organization.  If you do not wish to use `which_org` then you will have to hard code the organization for each individual object replacing the variable `"{{ which_org }}"` with the organization name.

    CONTROLLER_VERIFY_SSL

        CONTROLLER_VERIFY_SSL it is recommended not to modify this variable.  By default Tower / AAP 2.1 is installed with a self-signed certificate.  If you do not replace the certificate then you will receive certificate errors which prevent creating your objects.

`vars/controller_credential_types.yml`:

    controller_credential_types

        Dictionary of credential types to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional credential types.

`vars/controller_credentials.yml`:

    controller_credentials

        Dictionary of credentials to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional credentials.

`vars/controller_groups.yml`:

    controller_groups

        Dictionary of (host) groups to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional groups.  You will need to ensure the inventory and hosts exists before you add groups.

`vars/controller_hosts.yml`:

    controller_hosts

        Dictionary of hosts to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional hosts.  You will need to ensure the inventory exists before you add hosts to it.

`vars/controller_inventories.yml`:

    controller_inventories

        Dictionary of inventories to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional inventories.

`vars/controller_inventory_sources.yml`:

    controller_inventory_sources

        Dictionary of inventory sources to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional inventory sources.  You will need to ensure the inventory exists before you add hosts to it.

`vars/controller_job_templates.yml`:

    controller_job_templates

        Dictionary of job templates to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional job templates.

`vars/controller_labels.yml`:

    controller_labels

        Dictionary of labels to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional labels.

`vars/controller_notification_templates.yml`:

    controller_notification_templates

        Dictionary of notification templates to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional notification templates.

`vars/controller_organizations_with_hub.yml`:

    controller_organizations

        Dictionary of organizations to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional organizations.

    You must associate Galaxy / Automation Hub credentials with an Organization before you sync projects.  Otherwise the project sync will fail. This particular vars file has the organization defined with the Galaxy / Automation Hub credentials.

    There is a check in the `tasks/manage_controller_organizations.yml` which checks to see if the organization is already defined.  If it is not defined then it creates the organization.

    However, you cannot associate a Galaxy / Private Automation Hub credential to an organization you are defining for the first time because those credentials for that organization have not been created yet.  So the organization is created, then credentials are added to the organization, and then the organization is updated to associate the Galaxy / Automation Hub credentials.

`vars/controller_organizations.yml`:

    controller_organizations

        Dictionary of organizations to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional organizations.

    This vars file has the organization defined without the Galaxy / Automation Hub credential.

`vars/controller_projects.yml`:

    controller_projects

        Dictionary of projects to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional projects.

`vars/controller_schedules.yml`:

    controller_schedules

        Dictionary of schedules to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional schedules.

`vars/controller_settings.yml`:

    controller_settings

        Dictionary of settings to create.  This file does not contain an example.  Check `tasks/manage_controller_settings.yml` for a link to documentation of the `controller_configuration` collection.

`vars/controller_teams.yml`:

    controller_teams

        Dictionary of teams to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional teams.

`vars/controller_users.yml`:

    Unless otherwise instructed, please refrain from adding local users.  Users should be added to the organization via LDAP mapping.

    controller_users

        Dictionary of local users to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional users.

`vars/controller_vars.yml`:

    DO NOT: populate this file with valid credentials and then commit the file to GitHub!

    controller_vars

        If using ansible-playbook, populate `controller_vars` your Tower or Controller hostname (or IP address), username, and password.  The variables are used for your connection to Tower / Controller to create the objects you define in these vars files.

        If you are going to create a Job Template in Tower / Controller to run the `controller_config.yml` playbook then do not populate this file and instead use either a Survey or extra_vars with your job template.

`vars/controller_workflows.yml`:

    controller_workflows

        Dictionary of workflows to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional workflows.

`vars/controller_execution_environments.yml`:

    controller_execution_environments

        Dictionary of execution environments to define.  One example exists that will need to be filled in.  You can also copy / paste the example for additional execution environments.

`vars/controller_notification_templates.yml`:

    controller_notification_templates

        Dictionary of notification templates to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional notification templates.

`vars/controller_roles.yml`:

    controller_roles

        Dictionary of roles to define.  One example exists that will need to be filled in.  You can also copy / paste the example for additional roles.

`vars/controller_instance_groups.yml`:

    controller_instance_groups

        Dictionary of instance groups to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional instance groups.

## Dependencies

A combination of `ansible.controller` or `ansible.tower` or `awx.awx` and
`controller_configuration` collections.

## Playbook Execution

You can run this playbook from ansible cli or as a Job Template in Tower / Controller.

From the command line to define all objects:

    ansible-playbook controller_config.yml --tags alltags

    or just to create new job templates:

    ansible-playbook controller_config.yaml --tags jobtemplates

## License

BSD

## Author Information

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
