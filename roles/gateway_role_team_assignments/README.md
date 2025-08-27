<!-- DOCSIBLE START -->

# 📃 Role overview

## gateway_role_team_assignments

```
Role belongs to infra/aap_configuration
Namespace - infra
Collection - aap_configuration
Version - 3.4.1-devel
Repository - https://github.com/redhat-cop/aap_configuration/
```

Description: An Ansible Role to create role_team_assignments in Ansible gateway.


| Field                | Value           |
|--------------------- |-----------------|
| Readme update        | 26/08/2025 |




<details>
<summary><b>🧩 Argument Specifications in meta/argument_specs</b></summary>

#### Key: main
**Description**: An Ansible Role to create role_team_assignments on Ansible gateway.


  - **aap_role_team_assignments**
    - **Required**: True
    - **Type**: list
    - **Default**: none
    - **Description**: Data structure describing your role_team_assignments
  
  
  
    
  

  - **role_team_assignments_async_retries**
    - **Required**: False
    - **Type**: 
    - **Default**: {{ aap_configuration_async_retries | default(30) }}
    - **Description**: This variable sets the number of retries to attempt for the role.
  
  
  

  - **aap_configuration_async_retries**
    - **Required**: False
    - **Type**: 
    - **Default**: 30
    - **Description**: This variable sets number of retries across all roles as a default.
  
  
  

  - **role_team_assignments_async_delay**
    - **Required**: False
    - **Type**: 
    - **Default**: {{ aap_configuration_async_delay | default(1) }}
    - **Description**: This variable sets delay between retries for the role.
  
  
  

  - **aap_configuration_async_delay**
    - **Required**: False
    - **Type**: 
    - **Default**: 1
    - **Description**: This variable sets delay between retries across all roles as a default.
  
  
  

  - **aap_configuration_async_dir**
    - **Required**: False
    - **Type**: 
    - **Default**: None
    - **Description**: Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.
  
  
  

  - **gateway_role_team_assignments_secure_logging**
    - **Required**: False
    - **Type**: bool
    - **Default**: {{ aap_configuration_secure_logging | default(false) }}
    - **Description**: Whether or not to include the sensitive tasks from this role in the log. Set this value to `true` if you will be providing your sensitive values from elsewhere.
  
  
  

  - **aap_configuration_secure_logging**
    - **Required**: False
    - **Type**: bool
    - **Default**: False
    - **Description**: This variable enables secure logging across all roles as a default.
  
  
  

  - **platform_state**
    - **Required**: False
    - **Type**: str
    - **Default**: present
    - **Description**: The state all objects will take unless overridden by object default
  
  
  

  - **aap_hostname**
    - **Required**: False
    - **Type**: str
    - **Default**: None
    - **Description**: URL to the Ansible gateway Server.
  
  
  

  - **aap_validate_certs**
    - **Required**: False
    - **Type**: str
    - **Default**: True
    - **Description**: Whether or not to validate the Ansible gateway Server's SSL certificate.
  
  
  

  - **aap_username**
    - **Required**: False
    - **Type**: str
    - **Default**: None
    - **Description**: Admin User on the Ansible gateway Server. Either username / password or oauthtoken need to be specified.
  
  
  

  - **aap_password**
    - **Required**: False
    - **Type**: str
    - **Default**: None
    - **Description**: Gateway Admin User's password on the Ansible gateway Server. This should be stored in an Ansible Vault at vars/gateway-secrets.yml or elsewhere and called from a parent playbook. Either username / password or oauthtoken need to be specified.
  
  
  

  - **aap_token**
    - **Required**: False
    - **Type**: str
    - **Default**: None
    - **Description**: Gateway Admin User's token on the Ansible gateway Server. This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook. Either username / password or oauthtoken need to be specified.
  
  
  



</details>


### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |Required    | Title       |
|--------------|--------------|-------------|-------------|-------------|
| [gateway_role_team_assignments](defaults/main.yml#L11)   | list   | `[]` |    n/a  |  n/a |
| [gateway_role_team_assignments_secure_logging](defaults/main.yml#L12)   | str   | `{{ aap_configuration_secure_logging ¦ default('false') }}` |    n/a  |  n/a |
| [gateway_role_team_assignments_async_retries](defaults/main.yml#L13)   | str   | `{{ aap_configuration_async_retries ¦ default(30) }}` |    n/a  |  n/a |
| [gateway_role_team_assignments_async_delay](defaults/main.yml#L14)   | str   | `{{ aap_configuration_async_delay ¦ default(1) }}` |    n/a  |  n/a |
| [gateway_role_team_assignments_enforce_defaults](defaults/main.yml#L15)   | str   | `{{ aap_configuration_enforce_defaults ¦ default(false) }}` |    n/a  |  n/a |
| [gateway_role_team_assignments_loop_delay](defaults/main.yml#L16)   | str   | `{{ aap_configuration_loop_delay ¦ default(0) }}` |    n/a  |  n/a |
| [aap_configuration_async_dir](defaults/main.yml#L17)   | NoneType   | `None` |    n/a  |  n/a |





### Tasks


#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Manage Gateway Role Team Assignments Block | block | False |
| Role Team Assignments ¦ Configuration | ansible.platform.role_team_assignment | False |
| Role Team Assignments ¦ Wait for finish the configuration | ansible.builtin.include_role | True |







## Author Information
David Danielsson

#### License

GPLv3

#### Minimum Ansible Version

2.16.0

#### Platforms

- **EL**: ['all']

<!-- DOCSIBLE END -->