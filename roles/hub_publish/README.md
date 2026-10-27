# infra.aap_configuration.hub_publish

## Description

An Ansible Role to publish collections to Automation Hub or Galaxies.

## Variables

|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`aap_hostname`|""|yes|URL to the Ansible Automation Platform Server.|127.0.0.1|
|`aap_username`|""|no|Admin User on the Ansible Automation Platform Server. Either username / password or oauthtoken need to be specified.||
|`aap_password`|""|no|Platform Admin User's password on the Server.  This should be stored in an Ansible Vault at vars/platform-secrets.yml or elsewhere and called from a parent playbook.||
|`hub_token`|""|no|Admin User's token on the Automation Hub Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`aap_validate_certs`|`true`|no|Whether or not to validate the Ansible Automation Platform Server's SSL certificate.||
|`aap_request_timeout`|`10`|no|Specify the timeout Ansible should use in requests to the Galaxy or Automation Hub host.||
|`aap_configuration_collect_logs`|`false`|no|Specify whether to collect async results and continue for all failed async tasks instead of failing on the first error. Collected results are available in the `aap_configuration_role_errors` variable.||
|`aap_configuration_register`|""|no|Specify a variable to register the values of all aap_configuration tasks. This will create an object with each aap object as an element containing a list of each item created.||
|`hub_path_prefix`|""|no|API path used to access the api. Either galaxy, automation-hub, or custom||
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.||
|`aap_configuration_working_dir`|`/var/tmp`|no|The working directory where the built artifacts live, or where the artifacts will be built.||
|`hub_auto_approve`|`false`|no|Whether the collection will be automatically approved in Automation Hub. This will only work if the account being used has correct privileges.||
|`hub_overwrite_existing`|`false`|no|Whether the collection will be automatically overwrite an existing collection in Automation Hub. This will only work if the account being used has correct privileges.||
|`hub_skip_existing_collections`|`true`|no|Skip clone, build, and upload when the collection version already exists in Automation Hub. Set `hub_overwrite_existing` to `true` to force re-publishing. Set to `false` to restore the previous always-build behavior.||
|`hub_repository`|`staging`|no|Name of the destination repository to publish collections to. Defaults to `staging`.||
|`hub_custom_collections`|`see below`|no|Data structure describing your collections, mutually exclusive to hub_collection_list, described below.||
|`hub_collection_list`|`list`|no|Data structure file paths to pre built collections, mutually exclusive with hub_custom_collections.||

### Secure Logging Variables

The following Variables complement each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add publish collections task does not include sensitive information.
hub_configuration_publish_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`hub_configuration_publish_secure_logging`|`false`|no|Whether or not to include the sensitive publish collections role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_timeout`|1000|no|This variable sets the async timeout for the role globally.|
|`hub_configuration_publish_async_timeout`|`aap_configuration_async_timeout`|no|This variable sets the async timeout for the role.|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`hub_configuration_publish_async_retries`|`aap_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_loop_delay`|1000|no|This variable sets the loop_delay for the role globally.|
|`hub_configuration_publish_loop_delay`|`aap_configuration_loop_delay`|no|This variable sets the loop_delay for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`hub_configuration_publish_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|

## Data Structure

### hub_custom_collections Variables

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`collection_name`|""|yes|str|Name of collection, normally the last part before the / in a git url.|
|`git_url`|""|no|str|Url to git repo. Required if collection_local_path not set|
|`version`|""|no|str|Git ref to pull. Will default to default branch if unset. Can specify tag, branch or commit ref here.|
|`key_path`|""|no|str|Path to ssh key for authentication.|
|`ssh_opts`|""|no|str|Options git will pass to ssh when used as protocol.|
|`collection_local_path`|""|no|str|Path to collection stored locally. Required if git_url not set. This value will be used rather than git_url if set.|
|`namespace`|""|no|str|Collection namespace. When combined with `name` and `collection_version`, enables a pre-clone Hub check to skip git checkout on re-runs.|
|`name`|""|no|str|Collection name. When combined with `namespace` and `collection_version`, enables a pre-clone Hub check to skip git checkout on re-runs.|
|`collection_version`|""|no|str|Collection version from `galaxy.yml`. Distinct from the git `version` ref. Enables pre-clone skip checks when set with `namespace` and `name`.|
|`overwrite_existing`|`false`|no|bool|Per-item override of `hub_overwrite_existing`.|
|`force`|`false`|no|bool|Alias for per-item `overwrite_existing: true`.|
|`register`|""|no|str|Variable to set based on the result of the object creation/modification|

The same per-item fields also apply to dictionary entries in `hub_collection_list` when publishing from a local source path.

### Skip Existing Collections

When `hub_skip_existing_collections` is `true` (default), the role queries Automation Hub for each collection version before cloning, building, or uploading. If the version already exists, those steps are skipped for that item.

- The existence check uses the global collection version API endpoint, matching `ansible.hub.ah_collection` behavior. It does not verify repository membership in `hub_repository`.
- Provide `namespace`, `name`, and `collection_version` on an item to enable a pre-clone skip check without reading `galaxy.yml`.
- Set `hub_skip_existing_collections: false` to always clone and build, matching pre-4.7 behavior.
- Per-item `overwrite_existing` or `force` disables the skip check for that item and passes the overwrite flag through to upload.

### Standard Project Data Structure

#### Yaml Example

```yaml
---
hub_custom_collections:
  - collection_name: ansible.utils
    git_url: https://github.com/ansible-collections/ansible.utils
    namespace: ansible
    name: utils
    collection_version: "4.1.0"
    version: "v4.1.0"

hub_auto_approve: true
hub_skip_existing_collections: true
```

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Build and add collection to Automation Hub
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    aap_validate_certs: false
  # Define following vars here, or in ah_configs/ah_auth.yml
  # ah_host: ansible-ah-web-svc-test-project.example.com
  # hub_token: changeme
  pre_tasks:
    - name: Include vars from ah_configs directory
      ansible.builtin.include_vars:
        dir: ./vars
        extensions: ["yml"]
      tags:
        - always
  roles:
    - infra.aap_configuration.hub_publish
```

## License

[GPLv3+](https://github.com/redhat-cop/infra.aap_configuration/blob/devel/LICENSE)

## Author

[Sean Sullivan](https://github.com/sean-m-sullivan/)
