# controller_configuration.workflow_job_templates
## Description
An Ansible Role to create Workflow Job Templates on Ansible Controller.

## Requirements
ansible-galaxy collection install -r tests/collections/requirements.yml to be installed
Currently:
  awx.awx
  or
  ansible.controller

## Variables

### Authentication
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`controller_state`|"present"|no|The state all objects will take unless overridden by object default|'absent'|
|`controller_hostname`|""|yes|URL to the Ansible Controller Server.|127.0.0.1|
|`controller_validate_certs`|`True`|no|Whether or not to validate the Ansible Controller Server's SSL certificate.||
|`controller_username`|""|yes|Admin User on the Ansible Controller Server.||
|`controller_password`|""|yes|Controller Admin User's password on the Ansible Controller Server. This should be stored in an Ansible Vault at vars/controller-secrets.yml or elsewhere and called from a parent playbook.||
|`controller_oauthtoken`|""|yes|Controller Admin User's token on the Ansible Controller Server. This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`workflow_job_templates`|`see below`|yes|Data structure describing your workflow job templates described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add Workflow Job Templates task does not include sensitive information.
workflow_job_templates_secure_logging defaults to the value of controller_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of genie roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`workflow_job_templates_secure_logging`|`False`|no|Whether or not to include the sensitive Workflow Job Templates role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`controller_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

## Data Structure
### Variables For Workflow Job Template
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Name of Workflow Job Template|
|`new_name`|""|str|no|Setting this option will change the existing name (looked up via the name field).|
|`copy_from`|""|no|str|Name or id to copy the Workflow template from. This will copy an existing workflow and change any parameters supplied.|
|`description`|""|no|str|Description to use for the job template.|
|`organization`|""|""|no|list|Organization the workflow job template exists in. Used to lookup the object, cannot be changed with this module|
|`ask_inventory_on_launch`|""|no|bool|Prompt user for inventory on launch.|
|`ask_limit_on_launch`|""|no|bool|Prompt user for a limit on launch.|
|`ask_scm_branch_on_launch`|""|no|bool|Prompt user for scm branch on launch.|
|`ask_variables_on_launch`|""|no|bool|Prompt user for extra_vars on launch.|
|`extra_vars`|""|no|dict|Specify extra_vars for the template.|
|`allow_simultaneous`|""|no|bool|Allow simultaneous runs of the workflow job template.|
|`inventory`|""|no|str|Inventory applied as a prompt, assuming job template prompts for inventory|
|`limit`|""|no|str|Limit applied as a prompt, assuming job template prompts for limit|
|`labels`|""|no|str|The labels applied to this job template|
|`notification_templates_approvals`|""|no|list|The notifications on approval to use for this organization in a list.|
|`notification_templates_error`|""|no|list|The notifications on error to use for this organization in a list.|
|`notification_templates_started`|""|no|list|The notifications on started to use for this organization in a list.|
|`notification_templates_success`|""|no|list|The notifications on success to use for this organization in a list.|
|`scm_branch`|""|no|str|SCM branch applied as a prompt, assuming job template prompts for SCM branch|
|`state`|`present`|no|str|Desired state of the resource.|
|`schema`|""|no|dict|A json list of nodes and their corresponding options. The sub-options are in the module doc.|
|`destroy_current_schema`|""|no|dict|Set in order to destroy current schema on the workflow, used in cases where drastic changes to schema are happening.|
|`survey_enabled`|""|no|bool|Enable a survey on the job template.|
|`survey_spec`|""|no|dict|JSON/YAML dict formatted survey definition.|
|`survey`|""|no|dict|JSON/YAML dict formatted survey definition. Alias of survey_spec|
|`webhook_service`|""|no|str|Service that webhook requests will be accepted from (github, gitlab)|
|`webhook_credential`|""|no|str|Personal Access Token for posting back the status to the service API|

### Variables For Workflow Job Template Node
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`workflow_job_template`|""|yes|str|The workflow job template the node exists in. Used for looking up the node, cannot be modified after creation.|
|`identifier`|""|yes|str|An identifier for this node that is unique within its workflow. It is copied to workflow job nodes corresponding to this node. This functions the same as the name field for other resources, however if it is not set, it will be set to a random UUID4 value. Recommended to use Column and row numbers for identifiers such as Node401. [Refer to this documentation for more](https://github.com/ansible/awx/blob/devel/docs/workflow.md)|
|`unified_job_template`|""|no|str|Name of unified job template to run in the workflow. Can be a job template, project, inventory source, etc. This parameter is mutually exclusive with approval_node.|
|`approval_node`|""|no|str|A dictionary of Name, description, and timeout values for the approval node. This parameter is mutually exclusive with unified_job_template.|
|`organization`|""|no|str|The organization of the workflow job template the node exists in. Used for looking up the workflow, not a direct model field.|
|`all_parents_must_converge`|""|no|bool|If enabled then the node will only run if all of the parent nodes have met the criteria to reach this node|
|`always_nodes`|""|no|list|Nodes that will run after this node completes.|
|`failure_nodes`|""|no|list|Nodes that will run after this node completes.|
|`success_nodes`|""|no|list|Nodes that will run after this node completes.|
|`verbosity`|""|no|str|Verbosity applied as a prompt, if job template prompts for verbosity|
|`state`|""|no|str|Desired state of the resource|
|`credentials`|""|no|list|Credentials to be applied to job as launch-time prompts.|
|`diff_mode`|""|no|bool|Run diff mode, applied as a prompt, if job template prompts for diff mode|
|`extra_data`|""|no|dict|Variables to apply at launch time. Will only be accepted if job template prompts for vars or has a survey asking for those vars. extra_data are extra_vars at the node level and named so to match the module and the API. These are only for "ask extra vars on prompt" on a given job template.|
|`inventory`|""|no|str|Inventory applied as a prompt, if job template prompts for inventory|
|`job_tags`|""|no|str|NJob tags applied as a prompt, if job template prompts for job tags|
|`job_type`|""|no|str|Job type applied as a prompt, if job template prompts for job type|
|`limit`|""|no|str|Limit to act on, applied as a prompt, if job template prompts for limit|
|`scm_branch`|""|no|str|SCM branch applied as a prompt, if job template prompts for SCM branch|
|`skip_tags`|""|no|str|Tags to skip, applied as a prompt, if job template prompts for job tags|

### Approval node dictionary
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Name of this workflow approval template.|
|`description`|""|no|str|Optional description of this workflow approval template.|
|`timeout`|0|no|int|The amount of time (in seconds) before the approval node expires and fails.|

### Surveys
Refer to the [Controller Api Guide](https://docs.ansible.com/ansible-tower/latest/html/towerapi/api_ref.html#/Job_Templates/Job_Templates_job_templates_survey_spec_create) for more information about forming surveys
|Variable Name|Variable Description|
|:---:|:---:|
|`name`|Name of the survey|
|`description`|Description of the survey|
|`spec`|List of survey items, each a dictionary containing the following fields|
|`question_name`|Name of the field/item|
|`question_description`|Longer description|
|`required`|Boolean expressing if an answer is required|
|`type`|One of `text`, `password`, `integer`, `float`, `multiplechoice`or `multiselect`|
|`variable`|Name of Ansible Variable where to put the answer|
|`default`|Default value for the variable|
|`min`|Minimum value for a number type|
|`max`|Maximum value for a number type|
|`choices`|List of choices for a "multi" type|
|`new_question`|Boolean|

### Workflow Data Structures
This role accepts two data models.
#### Simplified Workflow nodes
A simple straightforward easy to maintain model using the var simplified_workflow_nodes.
However this is, not compatible with the schema option on the controller_workflow_job_template module and will result in errors.
Uses the variable 'simplified_workflow_nodes' to describe nodes as shown below.

#### Simplified Workflow Node Data structure model
##### Yaml Example
```yaml
---
controller_workflows:
  - name: Simple workflow schema
    description: a basic workflow
    extra_vars: ''
    survey_enabled: false
    allow_simultaneous: false
    ask_variables_on_launch: false
    inventory:
    limit:
    scm_branch:
    ask_inventory_on_launch: false
    ask_scm_branch_on_launch: false
    ask_limit_on_launch: false
    webhook_service: ''
    webhook_credential:
    organization: Default
    schedules: []
    simplified_workflow_nodes:
      - all_parents_must_converge: false
        identifier: node101
        unified_job_template: RHVM-01
        credentials: []
        success_nodes:
          - node201
        failure_nodes: []
        always_nodes: []
      - identifier: node201
        approval_node:
          name: Simple approval node name
          description: Approve this to proceed in workflow
          timeout: 900 # 15 minutes
      - all_parents_must_converge: false
        identifier: node301
        unified_job_template: test-template-1
        credentials: []
        success_nodes: []
        failure_nodes: []
        always_nodes: []
    notification_templates_started: []
    notification_templates_success: []
    notification_templates_error: []
    notification_templates_approvals: []
    survey_spec: {}

```

#### Controller Export Model
This model is based off of the output from awx.awx.export, that is based on the API.
This is more complicated, However it allows the user to use the schema input on the role which runs much faster compared to the simplified model.
This can be under the subvariable 'workflow_nodes' or under the subvariable 'related.workflow_nodes' which is the output of controller_export.

#### Controller Export Data structure model
##### Yaml Example
```yaml
---
controller_workflows:
  - name: Simple workflow schema
    description: a basic workflow
    extra_vars: ''
    survey_enabled: false
    allow_simultaneous: false
    ask_variables_on_launch: false
    inventory:
    limit:
    scm_branch:
    ask_inventory_on_launch: false
    ask_scm_branch_on_launch: false
    ask_limit_on_launch: false
    webhook_service: ''
    webhook_credential:
    organization:
      name: Default
    workflow_nodes:
      - all_parents_must_converge: false
        identifier: node101
        unified_job_template:
          name: RHVM-01
          type: job_template
          organization:
            name: Default
        related:
          success_nodes:
            - workflow_job_template:
                name: Simple workflow schema
              identifier: node201
      - all_parents_must_converge: false
        identifier: node201
        unified_job_template:
          name: test-template-1
          type: job_template
          organization:
            name: Default
      notification_templates_started: []
      notification_templates_success: []
      notification_templates_error: []
      notification_templates_approvals: []
      survey_spec:
        name: ''
        description: ''
        spec:
          - question_name: Basic Name
            question_description: Name
            required: true
            type: text
            variable: basic_name
            min: 0
            max: 1024
            default: ''
            choices: ''
            new_question: true

```

##### Json Example
```json
{
  "controller_workflows": [
    {
      "name": "Simple workflow schema",
      "description": "a basic workflow",
      "extra_vars": "",
      "survey_enabled": false,
      "allow_simultaneous": false,
      "ask_variables_on_launch": false,
      "inventory": null,
      "limit": null,
      "scm_branch": null,
      "ask_inventory_on_launch": false,
      "ask_scm_branch_on_launch": false,
      "ask_limit_on_launch": false,
      "webhook_service": "",
      "webhook_credential": null,
      "organization": {
        "name": "Default"
      },
      "related": {
        "schedules": [

        ],
        "workflow_nodes": [
          {
            "all_parents_must_converge": false,
            "identifier": "node101",
            "unified_job_template": {
              "name": "RHVM-01",
              "type": "job_template",
              "organization": { "name": "Default" }
            },
            "related": {
              "credentials": [

              ],
              "success_nodes": [
                {
                  "workflow_job_template": {
                    "name": "Simple workflow schema"
                  },
                  "identifier": "node201"
                }
              ],
              "failure_nodes": [

              ],
              "always_nodes": [

              ]
            }
          },
          {
            "all_parents_must_converge": false,
            "identifier": "node201",
            "unified_job_template": {
              "name": "test-template-1",
              "type": "job_template",
              "organization": { "name": "Default" }
            },
            "related": {
              "credentials": [

              ],
              "success_nodes": [

              ],
              "failure_nodes": [

              ],
              "always_nodes": [

              ]
            }
          }
        ],
        "notification_templates_started": [

        ],
        "notification_templates_success": [

        ],
        "notification_templates_error": [

        ],
        "notification_templates_approvals": [

        ],
        "survey_spec": {
        }
      }
    }
  ]
}
```


## Playbook Examples
### Standard Role Usage
```yaml
---
- name: Playbook to configure ansible controller post installation
  hosts: localhost
  connection: local
  # Define following vars here, or in controller_configs/controller_auth.yml
  # controller_hostname: ansible-controller-web-svc-test-project.example.com
  # controller_username: admin
  # controller_password: changeme
  pre_tasks:
    - name: Include vars from controller_configs directory
      include_vars:
        dir: ./yaml
        ignore_files: [controller_config.yml.template]
        extensions: ["yml"]
  roles:
    - {role: redhat_cop.controller_configuration.workflow_job_templates, when: controller_workflows is defined}

```
## License
[MIT](LICENSE)

## Author
[Sean Sullivan](https://github.com/sean-m-sullivan)
