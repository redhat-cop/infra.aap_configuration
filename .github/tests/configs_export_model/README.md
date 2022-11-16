# Automation Controller Export Documentation

## Description

This is documentation on how to use a the Automation Controller export commands in development.

This command allows exporting all available endpoints for Automation Controller for use in importing, templates, backups and many other uses.

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
