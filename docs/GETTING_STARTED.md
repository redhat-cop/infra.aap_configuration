# Getting Started with infra.aap_configuration

Welcome to the **infra.aap_configuration** collection. This guide will help you get started quickly with configuring your Ansible Automation Platform (AAP) using this collection.

## What is this Collection?

The `infra.aap_configuration` collection provides a comprehensive set of Ansible roles to configure and manage your AAP 2.5+ environment as code. It supports:

- **Automation Controller** - Job templates, projects, inventories, credentials, and more
- **Automation Hub** - Collections, execution environments, namespaces
- **Event-Driven Ansible (EDA)** - Rulebook activations, decision environments, projects
- **Automation Gateway** - Services, routes, authentication, and access management

## Prerequisites

Before you begin, ensure you have:

1. **Ansible** installed (version 2.15 or higher recommended)
2. **Access to an AAP 2.5+** environment
3. **API credentials** for your AAP instance (username/password or OAuth token)

## Installation

### Step 1: Create a Requirements File

Create a `requirements.yml` file with the necessary collections:

```yaml
---
collections:
  - name: ansible.platform
    version: ">=2.5.0" # for AAP 2.6 this should be 2.6.0
  - name: ansible.hub
    version: ">=1.0.0"
  - name: ansible.controller
    version: ">=4.6.0" # for AAP 2.6 this should be 4.7.0
  - name: ansible.eda
    version: ">=2.5.0"
  - name: infra.aap_configuration
```

### Step 2: Install the Collections

Install all required collections using ansible-galaxy:

```bash
ansible-galaxy collection install -r requirements.yml
```

Verify the installation:

```bash
 ansible-galaxy collection list | grep -E '(infra.|ansible.)'
```

## Quick Start

### Method 1: Using the Dispatch Role (Recommended)

The **dispatch role** is the recommended way to use this collection. It orchestrates all other roles in the correct order, making configuration management simple and consistent.

#### 1. Create Your Project Structure

Set up a basic directory structure for your configuration:

```bash
mkdir -p aap-config/configs
cd aap-config
```

#### 2. Create Authentication Variables

Create `configs/auth.yml` with your AAP credentials:

```yaml
---
# Connection details
aap_hostname: aap.example.com
aap_username: admin
aap_password: your-secure-password
aap_validate_certs: false  # Set to true in production

# Alternatively, use an OAuth token (recommended)
# aap_hostname: aap.example.com
# aap_token: your-oauth-token
# aap_validate_certs: true
```

> **Security Note:** Never commit credentials to version control! Use Ansible Vault to encrypt this file:
>
> ```bash
> ansible-vault encrypt configs/auth.yml
> ```

#### 3. Create Your First Configuration

Create `configs/organizations.yml`:

```yaml
---
aap_organizations:
  - name: MyOrg
    description: My First Organization
  - name: Development
    description: Development Environment Organization
```

Create `configs/projects.yml`:

```yaml
---
controller_projects:
  - name: Demo Project
    organization: MyOrg
    scm_type: git
    scm_url: https://github.com/ansible/ansible-examples.git
    scm_branch: main
    description: Demo project for getting started
```

#### 4. Create Your Playbook

Create `configure_aap.yml`:

```yaml
---
- name: Configure Ansible Automation Platform
  hosts: localhost
  connection: local
  gather_facts: false

  tasks:
    - name: Load all configuration files
      ansible.builtin.include_vars:
        dir: configs
        extensions:
          - yml
      tags:
        - always

    - name: Configure AAP using dispatch role
      ansible.builtin.include_role:
        name: infra.aap_configuration.dispatch
```

#### 5. Run Your Configuration

Execute the playbook:

```bash
# If using vault-encrypted credentials
ansible-playbook configure_aap.yml --ask-vault-pass

# Or without vault
ansible-playbook configure_aap.yml
```

### Method 2: Using Individual Roles

You can also use individual roles for more granular control:

```yaml
---
- name: Configure only Controller Projects
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    aap_hostname: aap.example.com
    aap_username: admin
    aap_password: password

    controller_projects:
      - name: My Project
        organization: Default
        scm_type: git
        scm_url: https://github.com/ansible/ansible-examples.git

  tasks:
    - name: Configure Controller Projects
      ansible.builtin.include_role:
        name: infra.aap_configuration.controller_projects
```

## Understanding the Dispatch Role

The dispatch role is a meta-role that runs multiple configuration roles in the correct order. This is important because AAP objects have dependencies (e.g., projects need organizations to exist first).

### Default Execution Order

When you use the dispatch role, it executes roles in this order:

1. **Gateway Configuration** - Authenticators, organizations, users, teams
2. **Hub Configuration** - Namespaces, collections, registries, execution environments
3. **Controller Configuration** - Settings, credentials, projects, inventories, job templates, workflows
4. **EDA Configuration** - Credentials, projects, decision environments, rulebook activations

### Running Specific Components

Use tags to run only specific parts of your configuration:

```bash
# Configure only projects
ansible-playbook configure_aap.yml --tags projects

# Configure only inventories and hosts
ansible-playbook configure_aap.yml --tags inventories,hosts

# Configure only job templates
ansible-playbook configure_aap.yml --tags job_templates
```

### Available Tags

Common tags include:

- `organizations` - Organizations
- `projects` - Projects
- `credentials` - Credentials
- `inventories` - Inventories
- `hosts` - Inventory hosts
- `job_templates` - Job templates
- `workflows` - Workflow job templates
- `schedules` - Schedules
- `settings` - Controller/Gateway settings

## Advanced Configuration

### Organizing Configuration Files

For larger deployments, organize your configuration by type and environment:

```text
aap-config/
├── configs/
│   ├── common/
│   │   ├── organizations.yml
│   │   ├── credential_types.yml
│   │   └── execution_environments.yml
│   ├── dev/
│   │   ├── projects.yml
│   │   ├── inventories.yml
│   │   └── job_templates.yml
│   └── prod/
│       ├── projects.yml
│       ├── inventories.yml
│       └── job_templates.yml
└── configure_aap.yml
```

Load configurations based on environment:

```yaml
---
- name: Configure AAP for specific environment
  hosts: localhost
  connection: local
  gather_facts: false

  tasks:
    - name: Load common configuration
      ansible.builtin.include_vars:
        dir: configs/common
        extensions:
          - yml

    - name: Load environment-specific configuration
      ansible.builtin.include_vars:
        dir: "configs/{{ environment }}"
        extensions:
          - yml

    - name: Apply configuration using dispatch
      ansible.builtin.include_role:
        name: infra.aap_configuration.dispatch
```

Run for different environments:

```bash
ansible-playbook configure_aap.yml -e environment=dev
ansible-playbook configure_aap.yml -e environment=prod
```

### Using Wildcard Variables

The dispatch role supports wildcard variable aggregation, which allows you to split configurations across multiple variables that get automatically merged:

```yaml
# configs/common/projects.yml
controller_projects_common:
  - name: Common Infrastructure Project
    organization: Default
    scm_type: git
    scm_url: https://github.com/example/common-infra.git

# configs/dev/projects.yml
controller_projects_dev:
  - name: Dev Application Project
    organization: Development
    scm_type: git
    scm_url: https://github.com/example/dev-app.git
```

Enable in your playbook:

```yaml
- name: Apply configuration using dispatch with wildcard vars
  ansible.builtin.include_role:
    name: infra.aap_configuration.dispatch
  vars:
    dispatch_include_wildcard_vars: true
```

This automatically merges `controller_projects_common` and `controller_projects_dev` into `controller_projects`.

### Error Handling and Logging

Enable error collection to see all failures at once rather than stopping at the first error:

```yaml
- name: Apply configuration with error collection
  ansible.builtin.include_role:
    name: infra.aap_configuration.dispatch
  vars:
    aap_configuration_collect_logs: true
```

This collects all errors in the `aap_configuration_role_errors` variable and displays them at the end.

## Common Configuration Examples

### Complete Controller Setup

Here's a more complete example showing organizations, credentials, projects, and job templates:

```yaml
---
# configs/controller_config.yml

aap_organizations:
  - name: Infrastructure
    description: Infrastructure Team Organization

controller_credential_types:
  - name: Custom SSH Key
    kind: cloud
    inputs:
      fields:
        - id: ssh_key
          type: string
          label: SSH Private Key
          secret: true
    injectors:
      extra_vars:
        custom_ssh_key: !unsafe "{{ ssh_key }}"

controller_credentials:
  - name: GitHub Access Token
    organization: Infrastructure
    credential_type: Source Control
    inputs:
      username: git-user
      password: ghp_yourpersonalaccesstoken

controller_projects:
  - name: Infrastructure Playbooks
    organization: Infrastructure
    scm_type: git
    scm_url: https://github.com/yourorg/infra-playbooks.git
    scm_credential: GitHub Access Token
    scm_update_on_launch: true
    scm_delete_on_update: true

controller_inventories:
  - name: Production Inventory
    organization: Infrastructure
    description: Production servers inventory

controller_templates:
  - name: Deploy Web Application
    organization: Infrastructure
    project: Infrastructure Playbooks
    playbook: deploy_webapp.yml
    inventory: Production Inventory
    credentials:
      - GitHub Access Token
    survey_enabled: false
    ask_variables_on_launch: true
```

### Hub Configuration

Configure Automation Hub with registries and execution environments:

```yaml
---
# configs/hub_config.yml

hub_namespaces:
  - name: my_organization
    description: My organization's namespace
    groups:
      - name: admins
        roles:
          - namespace_owner

hub_ee_registries:
  - name: quay_registry
    url: https://quay.io
    username: myuser
    password: mypassword

hub_ee_repositories:
  - name: my_custom_ee
    description: Custom execution environment
    registry: quay_registry
    upstream_name: myorg/my-custom-ee
```

### EDA Configuration

Set up Event-Driven Ansible:

```yaml
---
# configs/eda_config.yml

eda_projects:
  - name: EDA Rulebooks
    description: Event-driven automation rulebooks
    url: https://github.com/yourorg/eda-rulebooks.git
    credential: GitHub Access Token

eda_decision_environments:
  - name: Default Decision Environment
    description: Default decision environment for rulebooks
    image_url: quay.io/ansible/ansible-rulebook:latest

eda_rulebook_activations:
  - name: Monitor Infrastructure Events
    description: Respond to infrastructure monitoring events
    project: EDA Rulebooks
    rulebook: infrastructure_monitoring.yml
    decision_environment: Default Decision Environment
    enabled: true
```

## Best Practices

1. **Use Version Control**: Store all configuration files in Git for tracking changes and collaboration
2. **Encrypt Secrets**: Always use Ansible Vault for sensitive data like passwords and tokens
3. **Start Small**: Begin with basic configurations and gradually add complexity
4. **Use the Dispatch Role**: Let the dispatch role handle execution order and dependencies
5. **Tag Your Runs**: Use tags for faster iteration during development
6. **Test in Dev First**: Always test configuration changes in a development environment
7. **Document Your Configs**: Add comments to your YAML files explaining non-obvious configurations
8. **Use Idempotency**: The collection is designed to be idempotent - running it multiple times produces the same result

## Troubleshooting

### Module Not Found Errors

If you see errors like "couldn't resolve module/action":

1. Verify all collections are installed:

   ```bash
   ansible-galaxy collection list
   ```

2. Reinstall if needed:

   ```bash
   ansible-galaxy collection install -r requirements.yml --force
   ```

### Authentication Failures

If you get authentication errors:

1. Verify your credentials are correct
2. Check that `aap_hostname` includes the correct protocol (https://)
3. Test API access with curl:

   ```bash
   curl -k -u admin:password https://aap.example.com/api/v2/ping/
   ```

### Connection Timeout

If connections time out:

1. Check network connectivity to your AAP instance
2. Verify firewall rules allow access
3. Ensure the AAP instance is running

### Object Already Exists

The collection is idempotent. If an object already exists with the same name, it will be updated with the new configuration rather than creating a duplicate.

## Next Steps

- **Explore the Full Documentation**: Check out the [main README](../README.md) for detailed information
- **Review Individual Role Documentation**: Each role has its own README with specific parameters
- **Check the Examples**: Look at the [test configurations](../tests/configs/) for more examples
- **Use the Template**: Start with the [AAP Configuration Template](https://github.com/redhat-cop/aap_configuration_template)
- **Export Existing Config**: Use the [export functionality](EXPORT_README.md) to export your current AAP configuration

## Getting Help

- **Ansible Forums**: Use the [#infra-config-as-code tag](https://forum.ansible.com/tag/infra-config-as-code)
- **Matrix Chat**: Join the [AAP Config as Code room](https://matrix.to/#/#aap_config_as_code:ansible.com)
- **GitHub Issues**: Report bugs or request features on [GitHub](https://github.com/redhat-cop/infra.aap_configuration/issues)

## Additional Resources

- [Conversion Guide](CONVERSION_GUIDE.md) - Migrating from older versions
- [Export Guide](EXPORT_README.md) - Exporting existing configurations
- [Standards](STANDARDS.md) - Development standards and guidelines
- [Template Repository](https://github.com/redhat-cop/aap_configuration_template) - Ready-to-use project template

---
