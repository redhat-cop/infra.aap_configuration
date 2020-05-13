# ansible_tower_genie_job_templates
## Description
An Ansible Role to deploy job templates in Ansible Tower.
## Variables
|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_url`|""|yes|URL to the Ansible Tower Server.|
|`tower_verify_ssl`|False|no|Whether or not to validate the Ansible Tower Server's SSL certificate.|
|`tower_secrets`|False|yes|Whether or not to include variables stored in vars/tower-secrets.yml.  Set this value to `False` if you will be providing your sensitive values from elsewhere.|
|`tower_user`|""|yes|Admin User on the Ansible Tower Server.|
|`tower_pass`|""|yes|Tower Admin User's password on the Ansible Tower Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.|
|`tower_jt_name`|""|yes|Name of the job template to create in Ansible Tower.|
|`tower_jt_desc`||no|Description of the job template to create in Ansible Tower.|
|`tower_jt_job_type`|"run"|yes|Type of job template to define in Ansible Tower.  Choices are `run`, `check`, and `scan`.|
|`tower_jt_inventory`|""|no|Name of the inventory to associate with the job template in Ansible Tower.|
|`tower_jt_proj`|""|yes|Name of the project to associate with the job template in Ansible Tower.|
|`tower_jt_playbook`|""|yes|Path of the playbook yaml file for the job template to use, relative to its path in the source control project.|
|`tower_jt_cred`|""|no|Name of the credential to associate with the job template in Ansible Tower.|
|`tower_jt_vault_cred`||no|Name of the vault credential to associate with the job template in Ansible Tower.|
|`tower_jt_forks`|"0"|no|The number of simultaneous connections to make during a job template execution.  "0" is default and picked up from your ansible.cfg.|
|`tower_jt_limit`|""|no|Comma separated string of inventory targets to be associated with the job template in Ansible Tower.|
|`tower_jt_verbosity`|"0"|no|Verbosity level of standard out during a job template execution.  Default (normal) is used when not specified.  Choices are one of the following integers: 0 - normal, 1 - verbose, 2 - more verbose, 3 - debug, or 4 - connection debug.|
|`tower_jt_extra_vars_path`|""|no|Extra variables yaml file for the job template to use.|
|`tower_jt_job_tags`|""|no|Comma separated list of job tags to run during execution in the job template's associated playbook.|
|`tower_jt_force_handlers`|False|no|Whether or not to force playbook handlers to run.|
|`tower_jt_skip_tags`|""|no|Comma separated list of job tags to skip during execution in the job template's associated playbook.|
|`tower_jt_start_at_task`|""|no|Start at a particular task name in your playbook.|
|`tower_jt_timeout`|"0"|no|Timout of the playbook run.|
|`tower_jt_fact_caching`|False|no|Whether or not to use fact caching with this job template.|
|`tower_jt_host_conf_key`|""|no|Key to use during provisioning callbacks to this job template.|
|`tower_jt_ask_diff_mode`|False|no|Whether or not to prompt on launch for diff mode.|
|`tower_jt_ask_extra_vars`|False|no|Whether or not to prompt on launch for extra variable definitions.|
|`tower_jt_ask_limit`|False|no|Whether or not to prompt on launch for a job limit.|
|`tower_jt_ask_tags`|False|no|Whether or not to prompt on launch for a list of playbook tags to run.|
|`tower_jt_ask_skip_tags`|False|no|Whether or not to prompt on launch for a list of tags to skip.|
|`tower_jt_ask_job_type`|False|no|Whether or not to prompt on launch to choose a job run type.|
|`tower_jt_ask_verbosity`|False|no|Whether or not to prompt on launch for a verbosity setting.|
|`tower_jt_ask_inventory`|False|no|Whether or not to prompt on launch for an inventory.|
|`tower_jt_ask_cred`|False|no|Whether or not to prompt on launch for a credential.|
|`tower_jt_survey`|False|no|Whether or not to enable a survey on this job template.|
|`tower_jt_become`|False|no|Whether or not to enable become during job template execution.|
|`tower_jt_diff_mode`|False|no|Whether or not to enable diff mode on the job template.|
|`tower_jt_concurrent_jobs`|False|Whether or not to enable simultaneous job runs of this job template.|
## Playbook Examples
### Standard Role Usage
```yaml
---
- hosts: all
  vars_files:
    - "vars/myvault.yml"
  roles:
    - role: "genie-job-templates"
      tower_url: "https:/my-tower-server.foo.bar"
      tower_verify_ssl: False
      tower_secrets: False
      tower_user: "admin"
      tower_pass: "{{ my_tower_vault_pass }}"
      tower_jt_name: "My Job Template"
      tower_jt_desc: "Deploy my application stack"
      tower_jt_job_type: "run"
      tower_jt_inventory: "Dev Servers"
      tower_jt_proj: "My Cool Code Repository"
      tower_jt_playbook: "playbooks/deploy_app_stack.yml"
      tower_jt_limit: "App_Servers"
```      
## License
[MIT](LICENSE)

## Author
[Andrew J. Huffman](https://github.com/ahuffman)
