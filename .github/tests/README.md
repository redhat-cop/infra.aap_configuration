# Private Automation Hub Configuration Example Playbook

A single playbook and multiple task and vars files which can be used to define your Private Automation Hub configuration as code.  Update the vars files to define your objects and run the playbook to deploy your changes to your Private Automation Hub cluster(s).

Use of some tags may require that you include other tags; for example if adding a collection but you haven't already added the correct collection namespace.

Available tags:

- groups
- users
- namespaces
- publish
- ee_images
- ee_namespaces
- registries
- indices
- regsync
- repos
- reposync

## Requirements

This content utilizes the ah_configuration collection.  You will need connectivity to a Private Automation Hub server which has synchronized these collections or to the internet so that the collections can be installed.

You will also need Private Automation Hub credentials with sufficient permissions to create the objects you define as code.  This will need to be a local account within the cluster and not an externally authenticated account.

## Variables

`pah_configure.yml`:

    target_state

        I suggest leaving `target_state` set to "present".

`vars/ah_collection_namespaces.yml`:

    ah_namespaces

        Dictionary of collection namespaces to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional namespace types.

`vars/ah_collection_publish.yml`:

    ah_collections

        Dictionary of collections to publish.  One example exists that will need to be filled in.  You can also copy / paste the example for additional collections.

`vars/ah_ee_images.yml`:

    ah_ee_images

        Dictionary of execution environment images to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional execution environments.

`vars/ah_ee_namespaces.yml`:

    ah_ee_namespaces

        Dictionary of EE namespaces to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional EE namespaces.

`vars/ah_ee_registries.yml`:

    ah_ee_registries

        Dictionary of EE registries to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional EE registries.

`vars/ah_ee_registry_indices.yml`:

    ah_ee_registries

        Dictionary of EE registries to index.  One example exists that will need to be filled in.  You can also copy / paste the example for additional EE registries to index.

`vars/ah_ee_registry_sync.yml`:

    ah_ee_registries

        Dictionary of EE registries to synchronize.  One example exists that will need to be filled in.  You can also copy / paste the example for additional EE registries to sync.

`vars/ah_ee_repositories.yml`:

    ah_ee_repositories

        Dictionary of EE Repositories to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional EE Repositories.

`vars/ah_ee_repository_sync.yml`:

    ah_ee_repositories

        Dictionary of EE Repositories to sync.  One example exists that will need to be filled in.  You can also copy / paste the example for additional EE Repositories to sync.

`vars/ah_groups.yml`:

    ah_groups

        Dictionary of Groups to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional Groups.

`vars/ah_users.yml`:

    ah_users

        Dictionary of users to create.  One example exists that will need to be filled in.  You can also copy / paste the example for additional users.

`vars/pah_vars.yml`:

    ah_host:

        Hostname of an Automation Hub cluster you wish to configure.

    ah_username:

        Username to access the Automation Hub defined as `ah_host`.

    ah_password:

        Password for the user defined as `ah_password`.

    ah_token:

        Rather than username and password you can provide a token to use instead.

    validate_certs: false

        Whether or not to validate the certificates when connecting to private automation hub.  This is false by default as Private Automation Hub installs with a self-signed certificate unless otherwise provided.

    ah_path_prefix:

        This is an optional variable.  Review the ah_configuration for information on it's use.  Omit if not needed.

## Dependencies

You will need the `ah_configuration` collection.

## Playbook Execution

You can run this playbook from ansible cli or as a Job Template (future use case) in AAP's Controller.

From the command line to define all objects:

    ansible-playbook pah_configure.yml

    or just to create new job templates:

    ansible-playbook pah_configure.yml --tags namespaces

    or with ansible-navigator:

    ansible-navigator run pah_configure.yml

## License

BSD

## Author Information

[Tony Reveal](https://github.com/tonyreveal)
