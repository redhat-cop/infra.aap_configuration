# infra.aap_configuration.collect_async_status

## Description

Ansible role that checks the status of asynchronous tasks and optionally collects errors.

This is an internal role that is not meant to be called directly by users of this collection.

## Variables

|Variable Name|Default Value|Required|Description|
|:---|:---:|:---:|:---|
|`cas_job_async_results_item`||yes|The asynchronous item to check the status of. This must be from the registered `async` task|
|`cas_error_list_var_name`||yes|The name of the dictionary key to use when collecting errors|
|`aap_configuration_collect_logs`|`false`|no|When enabled collects error messages and continues execution. Messages are collected in a variable called `aap_configuration_role_errors`|

### Secure Logging Variables

The following Variables complement each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add host task does not include sensitive information.
`controller_configuration_host_secure_logging` defaults to the value of `aap_configuration_secure_logging` if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|
|`cas_secure_logging`|`false`|no|Whether or not to include the sensitive host role tasks in the log. Set this value to `true` if you will be providing your sensitive values from elsewhere.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`cas_async_retries`|`{{ aap_configuration_async_retries }}`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`cas_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|

## License

[GPLv3+](https://github.com/redhat-cop/infra.aap_configuration/blob/devel/LICENSE)

## Author

[Brant Evans](https://github.com/branic/)
