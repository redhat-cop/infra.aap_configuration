# Copyright: Contributors to the Ansible infra.aap_configuration collection
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Filters for the infra.aap_configuration.dispatch role."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


def _org_name(organization):
    """Return organization name from a string or export-style mapping."""
    if organization is None or organization is False:
        return None
    if isinstance(organization, dict):
        return organization.get("name") or None
    if isinstance(organization, str) and organization:
        return organization
    return None


def _label_entries(obj):
    """Yield (name, organization_or_none) from labels or related.labels on an object."""
    if not isinstance(obj, dict):
        return

    labels = None
    if isinstance(obj.get("labels"), list):
        labels = obj["labels"]
    else:
        related = obj.get("related")
        if isinstance(related, dict) and isinstance(related.get("labels"), list):
            labels = related["labels"]

    if not labels:
        return

    for label in labels:
        if isinstance(label, str) and label:
            yield label, None
        elif isinstance(label, dict) and label.get("name"):
            yield label["name"], _org_name(label.get("organization"))


def _project_org_map(projects):
    mapping = {}
    for project in projects or []:
        if not isinstance(project, dict) or not project.get("name"):
            continue
        org = _org_name(project.get("organization"))
        if org:
            mapping[project["name"]] = org
    return mapping


def _template_org(template, project_orgs):
    org = _org_name(template.get("organization"))
    if org:
        return org

    project = template.get("project")
    if isinstance(project, dict):
        org = _org_name(project.get("organization"))
        if org:
            return org
        project_name = project.get("name")
        return project_orgs.get(project_name) if project_name else None
    if isinstance(project, str) and project:
        return project_orgs.get(project)
    return None


def _template_org_map(templates, project_orgs):
    mapping = {}
    for template in templates or []:
        if not isinstance(template, dict) or not template.get("name"):
            continue
        org = _template_org(template, project_orgs)
        if org:
            mapping[template["name"]] = org
    return mapping


def _workflow_org_map(workflows):
    mapping = {}
    for workflow in workflows or []:
        if not isinstance(workflow, dict) or not workflow.get("name"):
            continue
        org = _org_name(workflow.get("organization"))
        if org:
            mapping[workflow["name"]] = org
    return mapping


def _add_label(derived, seen, unresolved, name, organization, source):
    if not name:
        return
    if not organization:
        unresolved.append({"name": name, "source": source})
        return
    key = (name, organization)
    if key in seen:
        return
    seen.add(key)
    derived.append({"name": name, "organization": organization})


def _resource_name(obj, default="unknown"):
    if isinstance(obj, dict):
        return obj.get("name") or obj.get("identifier") or default
    return default


def dispatch_derive_labels(existing_labels, templates=None, projects=None, workflows=None, schedules=None):
    """
    Derive controller_labels entries from labels used on templates, workflows, and schedules.

    Returns a dict with:
      - labels: merged list (explicit existing_labels first, then newly derived)
      - unresolved: label references that could not be mapped to an organization
    """
    project_orgs = _project_org_map(projects)
    template_orgs = _template_org_map(templates, project_orgs)
    workflow_orgs = _workflow_org_map(workflows)

    derived = []
    unresolved = []
    seen = set()

    for template in templates or []:
        if not isinstance(template, dict):
            continue
        default_org = _template_org(template, project_orgs)
        source = "controller_templates:{0}".format(_resource_name(template))
        for name, label_org in _label_entries(template):
            _add_label(derived, seen, unresolved, name, label_org or default_org, source)

    for workflow in workflows or []:
        if not isinstance(workflow, dict):
            continue
        default_org = _org_name(workflow.get("organization"))
        source = "controller_workflows:{0}".format(_resource_name(workflow))
        for name, label_org in _label_entries(workflow):
            _add_label(derived, seen, unresolved, name, label_org or default_org, source)

        nodes = workflow.get("simplified_workflow_nodes")
        if not isinstance(nodes, list):
            nodes = workflow.get("workflow_nodes")
        if not isinstance(nodes, list):
            nodes = []

        for node in nodes:
            if not isinstance(node, dict):
                continue
            node_source = "{0}/node:{1}".format(source, _resource_name(node))
            for name, label_org in _label_entries(node):
                _add_label(derived, seen, unresolved, name, label_org or default_org, node_source)

    for schedule in schedules or []:
        if not isinstance(schedule, dict):
            continue
        ujt = schedule.get("unified_job_template")
        ujt_name = ujt.get("name") if isinstance(ujt, dict) else ujt
        default_org = None
        if ujt_name:
            default_org = template_orgs.get(ujt_name) or workflow_orgs.get(ujt_name)
        source = "controller_schedules:{0}".format(_resource_name(schedule))
        for name, label_org in _label_entries(schedule):
            _add_label(derived, seen, unresolved, name, label_org or default_org, source)

    # Preserve explicit controller_labels; append derived entries that are not already present.
    merged = []
    merged_seen = set()
    for item in existing_labels or []:
        if not isinstance(item, dict) or not item.get("name"):
            continue
        org = _org_name(item.get("organization"))
        if not org:
            # Keep malformed/partial entries as-is without attempting to dedupe.
            merged.append(item)
            continue
        key = (item["name"], org)
        if key in merged_seen:
            continue
        merged_seen.add(key)
        # Normalize organization to a string name for consistency with derived entries.
        normalized = dict(item)
        normalized["organization"] = org
        merged.append(normalized)

    for item in derived:
        key = (item["name"], item["organization"])
        if key not in merged_seen:
            merged_seen.add(key)
            merged.append(item)

    return {"labels": merged, "unresolved": unresolved}


class FilterModule(object):
    """Ansible filter plugin."""

    def filters(self):
        return {
            "dispatch_derive_labels": dispatch_derive_labels,
        }
