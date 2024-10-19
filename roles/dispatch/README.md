# infra.aap_configuration.dispatch

## Description

An Ansible Role to run all roles in the infra.aap_configuration collection.

## Variables

Each role has its own variables, for information on those please see each role which this role will call. This role has one key variable `gateway_dispatch_roles` and its default value is shown below:

```yaml
gateway_dispatch_roles:
  - {role: settings, var: settings_list, tags: settings}
  - {role: users, var: users_list, tags: users}
  - {role: authenticators, var: authenticators_list, tags: authenticators}
  - {role: authenticator_maps, var: authenticator_maps_list, tags: authenticator_maps}
  - {role: http_ports, var: http_ports_list, tags: http_ports}
  - {role: organizations, var: organizations_list, tags: organizations}
  - {role: teams, var: platform_teams, tags: teams}
  - {role: service_clusters, var: gateway_service_clusters, tags: service_clusters}
  - {role: service_keys, var: service_keys_list, tags: service_keys}
  - {role: service_nodes, var: service_nodes_list, tags: service_nodes}
  - {role: services, var: services_list, tags: services}
  - {role: routes, var: gateway_routes, tags: routes}
  - {role: role_user_assignments, var: role_user_assignments_list, tags: role_user_assignments}
```

Note that each item has three elements:

- `role` which is the name of the role within infra.aap_configuration
- `var` which is the variable which is used in that role. We use this to prevent the role being called if the variable is not set
- `tags` the tags which are applied to the role so it is possible to apply tags to a playbook using the dispatcher with these tags.

It is possible to redefine this variable with a subset of roles or with different tags. In general we suggest keeping the same structure and perhaps just using a subset.

For more information about variables, see [top-level README](../../README.md).
For more information about roles, see each roles' README (also linked in the top-level README)

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)
