import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import (
    AuditResult,
    audit_project,
    demo_display_name,
    demo_project_paths,
    export_report,
    priority_presentation,
    report_display_chunks,
)


class RecoveryManagerTests(unittest.TestCase):
    def test_unavailable_folder_has_now_priority(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            missing = Path(temporary) / "does-not-exist"
            result = audit_project(missing)

        self.assertFalse(result.available)
        self.assertEqual("now", result.priority)
        self.assertIn("unavailable", " ".join(result.evidence).lower())

    def test_missing_readme_and_tests_has_evidence_and_four_stage_plan(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            Path(temporary, "main.py").touch()
            result = audit_project(temporary)

        evidence = " ".join(result.evidence).lower()
        self.assertIn("readme", evidence)
        self.assertIn("tests", evidence)
        self.assertEqual(
            ["Preserve", "Understand", "Verify", "Continue"],
            [stage for stage, _ in result.recovery_plan],
        )

    def test_secret_content_never_enters_report_or_prompt(self) -> None:
        secret = "ULTRA_PRIVATE_TOKEN_123456"
        with tempfile.TemporaryDirectory() as temporary:
            Path(temporary, ".env").write_text(
                f"API_TOKEN={secret}", encoding="utf-8"
            )
            Path(temporary, "main.py").touch()
            with patch.object(
                Path,
                "read_text",
                side_effect=AssertionError("Audit attempted to read file content"),
            ):
                result = audit_project(temporary)

        combined = result.to_markdown() + result.codex_prompt
        self.assertNotIn(secret, combined)
        self.assertIn("contents were not opened", combined)

    def test_export_omits_absolute_private_path_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            private_project = Path(temporary) / "safe-project-name"
            private_project.mkdir()
            result = audit_project(private_project)
            destination = Path(temporary) / "report.md"
            export_report(result, destination)
            report = destination.read_text(encoding="utf-8")

        self.assertNotIn(str(private_project), report)
        self.assertIn("safe-project-name", report)

    def test_synthetic_demos_need_no_credentials_or_services(self) -> None:
        demos = demo_project_paths()
        self.assertGreaterEqual(len(demos), 2)
        for demo in demos:
            result = audit_project(demo)
            self.assertTrue(result.available)
            text = result.to_markdown().lower()
            self.assertNotIn("api_key=", text)
            self.assertNotIn("password=", text)
            self.assertNotIn("token=", text)

    def test_demo_names_are_friendly_without_changing_folder_names(self) -> None:
        self.assertEqual("Healthy demo", demo_display_name("healthy_demo"))
        self.assertEqual("Needs recovery", demo_display_name("needs_recovery"))
        self.assertEqual(
            {"healthy_demo", "needs_recovery"},
            {item.name for item in demo_project_paths()},
        )

    def test_priority_presentations_have_labels_tags_and_explanations(self) -> None:
        expected = {
            "now": ("NOW", "priority_now"),
            "later": ("LATER", "priority_later"),
            "archive for confirmation": (
                "ARCHIVE FOR CONFIRMATION",
                "priority_archive",
            ),
        }
        for priority, (label, tag) in expected.items():
            actual_label, actual_tag, explanation = priority_presentation(priority)
            self.assertEqual(label, actual_label)
            self.assertEqual(tag, actual_tag)
            self.assertTrue(explanation)

    def test_desktop_report_text_has_no_raw_markdown_symbols(self) -> None:
        result = AuditResult(
            project_name="healthy_demo",
            available=True,
            priority="later",
            evidence=("No immediate gap.",),
            recovery_plan=(
                ("Preserve", "Confirm the folder for `healthy_demo`."),
                ("Understand", "Review README."),
                ("Verify", "Run one test."),
                ("Continue", "Choose one task."),
            ),
            codex_prompt="Plan first for `healthy_demo`, then verify.",
            metadata_summary=("File contents read: no.",),
        )
        display_text = "".join(text for text, _ in report_display_chunks(result))

        self.assertIn("Healthy demo", display_text)
        self.assertIn("LATER", display_text)
        self.assertNotIn("##", display_text)
        self.assertNotIn("**", display_text)
        self.assertNotIn("```", display_text)
        self.assertNotIn("`", display_text)


if __name__ == "__main__":
    unittest.main()
