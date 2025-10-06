# Role Alias Support Documentation

This document lists Ansible roles that support variable name aliases for backward compatibility.

## Controller Roles with Alias Support

### controller_credentials
- **Primary Variable**: `controller_credentials`
- **Alias**: `credentials`
- **Implementation**: `{{ credentials if credentials is defined else controller_credentials }}`
- **Purpose**: Allows users to use the shorter `credentials` variable name

### controller_workflow_job_templates
- **Primary Variable**: `controller_workflows`
- **Aliases**: `workflow_job_templates`
- **Implementation**:
  - Loop: `{{ controller_workflows | default(workflow_job_templates) }}`
  - Alternative: `{{ workflow_job_templates if workflow_job_templates is defined else controller_workflows }}`
- **Purpose**: Supports both naming conventions for workflow job templates

## Notes

- Most roles do not support aliases and require the exact variable name as defined in their argument specifications
- Alias support is provided for backward compatibility with existing playbooks
- When using aliases, ensure the primary variable name is not also defined to avoid conflicts
