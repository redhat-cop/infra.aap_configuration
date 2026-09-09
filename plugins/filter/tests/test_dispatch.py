# Copyright: Contributors to the Ansible infra.aap_configuration collection
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Unit tests for dispatch_derive_labels filter."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "plugins", "filter"))

from dispatch import dispatch_derive_labels  # noqa: E402


class TestDispatchDeriveLabels(unittest.TestCase):
    def test_derives_from_templates_workflows_and_schedules(self):
        result = dispatch_derive_labels(
            [{"name": "Prod", "organization": "Default"}, {"name": "Manual", "organization": "Default"}],
            templates=[
                {"name": "jt1", "project": "Test Project", "labels": ["Prod", "Dev"]},
                {"name": "jt2", "organization": "Satellite", "project": "Sat Project", "labels": ["Prod"]},
                {
                    "name": "jt-export",
                    "project": "Test Project",
                    "related": {"labels": [{"name": "ExportLabel", "organization": {"name": "Default"}}]},
                },
            ],
            projects=[
                {"name": "Test Project", "organization": "Default"},
                {"name": "Sat Project", "organization": "Satellite"},
            ],
            workflows=[
                {
                    "name": "wf1",
                    "organization": "Default",
                    "labels": ["Prod"],
                    "simplified_workflow_nodes": [
                        {"identifier": "n1", "labels": ["differential", "differential2"]},
                    ],
                },
                {"name": "wf2", "organization": {"name": "Satellite"}, "labels": ["SatOnly"]},
            ],
            schedules=[
                {"name": "s1", "unified_job_template": "jt1", "labels": ["SchedLabel"]},
                {"name": "s2", "unified_job_template": "wf1", "labels": ["Prod"]},
                {"name": "s3", "unified_job_template": "missing", "labels": ["Orphan"]},
            ],
        )

        self.assertEqual(
            result["labels"],
            [
                {"name": "Prod", "organization": "Default"},
                {"name": "Manual", "organization": "Default"},
                {"name": "Dev", "organization": "Default"},
                {"name": "Prod", "organization": "Satellite"},
                {"name": "ExportLabel", "organization": "Default"},
                {"name": "differential", "organization": "Default"},
                {"name": "differential2", "organization": "Default"},
                {"name": "SatOnly", "organization": "Satellite"},
                {"name": "SchedLabel", "organization": "Default"},
            ],
        )
        self.assertEqual(result["unresolved"], [{"name": "Orphan", "source": "controller_schedules:s3"}])

    def test_empty_inputs(self):
        result = dispatch_derive_labels([])
        self.assertEqual(result, {"labels": [], "unresolved": []})

    def test_export_style_project_organization(self):
        result = dispatch_derive_labels(
            [],
            templates=[
                {
                    "name": "jt1",
                    "project": {"name": "Tower Config", "organization": {"name": "Satellite"}},
                    "labels": ["Prod"],
                }
            ],
        )
        self.assertEqual(result["labels"], [{"name": "Prod", "organization": "Satellite"}])
        self.assertEqual(result["unresolved"], [])


if __name__ == "__main__":
    unittest.main()
