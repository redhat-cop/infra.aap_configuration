# Automation Controller Export Documentation

## Description

This is documentation on how to use a the Automation Controller export commands in development. You can also look at the [filetree_create](roles/filetree_create/README.md) role as another method to export data.

This command allows exporting all available endpoints for Automation Controller for use in importing, templates, backups and many other uses.

**NOTE:** If you use the awx export option it will NOT use the correct high level variable list naming that is expected by the rest of these roles you will need to correctly name them before being able to use the roles to import the data into your new Controller. See [#332](https://github.com/redhat-cop/controller_configuration/issues/332) for more details.

## Installation

```console
pip3 install awxkit
```

## Basic command options

```console
awx export --conf.host https://localhost --conf.username admin --conf.password ******** --conf.insecure --help
```

```console
awx export --conf.host https://localhost --conf.username admin --conf.password ******** --conf.insecure --job_templates
```

## Available options for this command

|Option|
|:---:|
|users|
|organizations|
|teams|
|credential_types|
|credentials|
|notification_templates|
|projects|
|inventory|
|inventory_sources|
|job_templates|
|workflow_job_templates|
