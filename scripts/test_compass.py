"""Offline consumer CLI checks. Fixtures are fictional and use temporary workspaces."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "helpers"))
from compass_lib import research, runs, timezones, workspaces
from compass_lib.common import Problem


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "helpers" / "compass.py"


class CompassCLI(unittest.TestCase):
    def invoke(self, command, payload, code=0, cli=CLI, env=None):
        completed = subprocess.run(
            [sys.executable, "-I", "-B", str(cli), command],
            input=json.dumps({"schema_version": 1, **payload}).encode("utf-8"),
            capture_output=True, check=False, env=env,
        )
        self.assertEqual(completed.returncode, code, completed.stderr.decode("utf-8"))
        return json.loads(completed.stdout if code == 0 else completed.stderr)

    def test_batch_preserves_order_and_regions(self):
        countries = [f"Example {n}" for n in range(17)]
        result = self.invoke("batch-partition", {"groups": [{"region": "Demo", "countries": countries}]})["result"]
        self.assertEqual([len(b["countries"]) for b in result["batches"]], [15, 2])
        self.assertEqual(result["expected"], countries)

    def test_raw_fx_range_and_context_only(self):
        result = self.invoke("compare", {
            "pay": {"low": "58250", "high": "60000", "currency": "EUR", "period": "annual", "basis": "gross_base"},
            "minimum": {"amount": "4900", "currency": "EUR", "period": "monthly", "basis": "gross_base", "hard_floor": True},
        })["result"]
        self.assertEqual(result["outcome"], "uncertain")

    def test_adjustment_confidence_cap(self):
        self.invoke("adjust-check", {"low": "5", "high": "8", "typical": "6.8", "label": "Moderate", "confidence": "High", "salary_evidence": "Low"}, 2)

    def test_state_is_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.invoke("state-check", {"workspace": directory, "workflow": "country-finder"})["result"]
            self.assertEqual(result["status"], "missing")
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_research_scope_retains_requested_countries_not_only_salary_rows(self):
        for filename in ("salary-calculator-01-research.md", "sc-step1-salary-research.md"):
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                root.joinpath(filename).write_text(
                    "## Research scope\n- 🇩🇪 Germany\n- 🇫🇷 France\n\nCountry: Germany\nDUMMY incomplete salary data\n",
                    encoding="utf-8")
                root.joinpath(".salary-calculator-state.json").write_bytes(b"DUMMY unfinished/corrupt state")
                before = {p.name: p.read_bytes() for p in root.iterdir()}
                result = self.invoke("research-scope", {"workspace": directory, "workflow": "salary-calculator"})["result"]
                self.assertEqual((result["status"], result["countries"], result["source"]),
                                 ("available", ["🇩🇪 Germany", "🇫🇷 France"], filename))
                self.assertFalse(result["human_confirmation_checked"])
                self.assertEqual({p.name: p.read_bytes() for p in root.iterdir()}, before)

    def test_research_scope_normalizes_legacy_lists_without_rewriting_them(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "sc-step1-salary-research.md")
            raw = "\ufeff## Research scope\r\nGermany 🇩🇪, France\r\n🇩🇪 GERMANY\r\nUSA\r\nUnited States\r\n\r\n```research\r\nCountry: Canada\r\n```\r\n".encode("utf-8")
            path.write_bytes(raw)
            result = self.invoke("research-scope", {"workspace": directory, "workflow": "salary-calculator",
                "aliases": {"USA": "United States"}})["result"]
            self.assertEqual(result["countries"], ["Germany 🇩🇪", "France", "USA"])
            self.assertEqual(path.read_bytes(), raw)

    def test_research_scope_missing_or_empty_never_infers_a_list_from_salary_data(self):
        for raw, status in ((None, "missing_file"), (self.salary_block(), "missing_scope"),
                            (b"## Research scope\nnone\n", "empty"), (b"## Research scope\n\n", "empty"),
                            (b"DUMMY prose\n## Research scope\nCanada\n", "missing_scope")):
            with self.subTest(status=status, raw=raw), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                if raw is not None:
                    root.joinpath("salary-calculator-01-research.md").write_bytes(raw)
                root.joinpath("salary-calculator-05b-final-results.md").write_bytes(b"DUMMY final table: Germany")
                before = {p.name: p.read_bytes() for p in root.iterdir()}
                result = self.invoke("research-scope", {"workspace": directory, "workflow": "salary-calculator"})["result"]
                self.assertEqual((result["status"], result["countries"]), (status, []))
                self.assertEqual({p.name: p.read_bytes() for p in root.iterdir()}, before)

    def test_research_scope_ambiguous_metadata_needs_clarification(self):
        for scope in ("Germany\nNotes: DUMMY old context\n", "none\nGermany\n", "Germany,\n",
                      "- \n", "| Country | Salary |\n", "Germany\n## Research scope\nFrance\n"):
            with self.subTest(scope=scope), tempfile.TemporaryDirectory() as directory:
                path = Path(directory, "salary-calculator-01-research.md")
                path.write_text("## Research scope\n" + scope, encoding="utf-8")
                before = path.read_bytes()
                self.invoke("research-scope", {"workspace": directory, "workflow": "salary-calculator"}, 4)
                self.assertEqual(path.read_bytes(), before)

    def test_research_scope_rejects_duplicate_filenames_and_unsafe_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for filename in ("salary-calculator-01-research.md", "sc-step1-salary-research.md"):
                root.joinpath(filename).write_bytes(b"## Research scope\nGermany\n")
            self.invoke("research-scope", {"workspace": directory, "workflow": "salary-calculator"}, 5)
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            target = Path(outside, "private.md")
            target.write_bytes(b"DUMMY private content")
            try:
                Path(directory, "salary-calculator-01-research.md").symlink_to(target)
            except OSError:
                self.skipTest("Symlink creation not permitted on this platform")
            self.invoke("research-scope", {"workspace": directory, "workflow": "salary-calculator"}, 2)
            self.assertEqual(target.read_bytes(), b"DUMMY private content")

    def test_salary_scope_handoff_keeps_country_finder_scope_independent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("sc-step1-salary-research.md").write_bytes(b"## Research scope\nGermany, France\n")
            root.joinpath("country-finder-01-criteria.md").write_bytes(b"DUMMY confirmed include: France, Canada; exclude: Germany\n")
            before = {p.name: p.read_bytes() for p in root.iterdir()}
            offered = self.invoke("research-scope", {"workspace": directory, "workflow": "salary-calculator"})["result"]
            self.assertEqual(offered["countries"], ["Germany", "France"])
            # The parent applies the user's changes/exclusions, not the scope reader.
            confirmed = ["France", "Canada"]
            batches = self.invoke("batch-partition", {"groups": [{"region": "Selected", "countries": confirmed}]})["result"]
            self.assertEqual(batches["expected"], confirmed)
            self.assertEqual(self.invoke("resolve-files", {"workspace": directory, "workflow": "country-finder"})["result"]["naming"], "current")
            self.assertEqual({p.name: p.read_bytes() for p in root.iterdir()}, before)

    def test_salary_ingestion_preserves_the_full_handoff_list_after_rejection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("salary-calculator-01-research.md").write_bytes(
                b"## Research scope\n- Germany\n- France\n\n" + self.salary_block() +
                b"\nCountry: France\nDUMMY missing both salary tiers\n")
            payload = {"workspace": directory, "workflow": "salary-calculator", "expected": ["Germany", "France"]}
            scan = self.invoke("research-scan", payload)["result"]
            ingested = self.invoke("ingest", {**payload, "source_hash": scan["source_hash"], "stored_hash": scan["stored_hash"],
                "decisions": [{"index": 0, "accept": True}, {"index": 1, "accept": False, "reason": "Missing salary tiers"}]})["result"]
            self.assertEqual(ingested["stored"], 1)
            before = {p.name: p.read_bytes() for p in root.iterdir()}
            offered = self.invoke("research-scope", {"workspace": directory, "workflow": "salary-calculator"})["result"]
            self.assertEqual(offered["countries"], ["Germany", "France"])
            self.assertEqual({p.name: p.read_bytes() for p in root.iterdir()}, before)

    def test_fresh_filename_resolution_is_read_only_and_workflow_scoped(self):
        for workflow, research_file, final_file in (
                ("country-finder", "country-finder-03-research.md", "country-finder-06-final-results.md"),
                ("salary-calculator", "salary-calculator-01-research.md", "salary-calculator-05b-final-results.md")):
            with self.subTest(workflow=workflow), tempfile.TemporaryDirectory() as directory:
                result = self.invoke("resolve-files", {"workspace": directory, "workflow": workflow})["result"]
                self.assertEqual(result["files"]["research"], research_file)
                self.assertEqual(result["files"]["final-results"], final_file)
                self.assertEqual((result["naming"], result["existing_outputs"]), ("current", []))
                self.assertEqual(list(Path(directory).iterdir()), [])

    def test_legacy_resume_keeps_remaining_filenames_without_copies(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("cf-step1-criteria.md").write_bytes(b"DUMMY criteria\r\n")
            before = {p.name: p.read_bytes() for p in root.iterdir()}
            result = self.invoke("resolve-files", {"workspace": directory, "workflow": "country-finder"})["result"]
            self.assertEqual(result["files"]["final-results"], "cf-step6-final-ranking.md")
            self.assertEqual(result["naming"], "legacy")
            other = self.invoke("resolve-files", {"workspace": directory, "workflow": "salary-calculator"})["result"]
            self.assertEqual(other["naming"], "current")
            self.assertEqual({p.name: p.read_bytes() for p in root.iterdir()}, before)

    def test_duplicate_filename_aliases_stop_even_when_identical(self):
        for content in (b"DUMMY original", b"DUMMY conflicting"):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                root.joinpath("cf-step6-final-ranking.md").write_bytes(b"DUMMY original")
                root.joinpath("country-finder-06-final-results.md").write_bytes(content)
                before = {p.name: p.read_bytes() for p in root.iterdir()}
                for command in ("resolve-files", "state-check"):
                    self.invoke(command, {"workspace": directory, "workflow": "country-finder"}, 5)
                self.assertEqual({p.name: p.read_bytes() for p in root.iterdir()}, before)

    def test_mixed_nonduplicate_names_keep_existing_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("sc-step1-salary-research.md").write_bytes(self.salary_block())
            root.joinpath("salary-calculator-02-validated-data.md").write_bytes(self.salary_block())
            result = self.invoke("resolve-files", {"workspace": directory, "workflow": "salary-calculator"})["result"]
            self.assertEqual(result["naming"], "mixed")
            self.assertEqual(result["files"]["validated-data"], "salary-calculator-02-validated-data.md")
            self.assertEqual(result["files"]["final-results"], "sc-step5b-final-verification.md")
            self.assertEqual(len(list(root.iterdir())), 2)

    def test_cross_workflow_completed_handoffs_choose_names_independently(self):
        registry = json.loads((ROOT / "data" / "workspace-files.json").read_text(encoding="utf-8"))["workflows"]
        for producer_style, consumer_style in (("legacy", "current"), ("current", "legacy")):
            with self.subTest(producer=producer_style), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                producer = registry["country-finder"]
                for artifact in producer["artifacts"].values():
                    root.joinpath(artifact[producer_style]).write_bytes(b"DUMMY saved country result\r\n")
                root.joinpath(producer["state"]).write_text(
                    '{"last_completed_step":6,"updated_at":"2026-10-22T00:00:00Z"}', encoding="utf-8")
                consumer = registry["salary-calculator"]
                root.joinpath(consumer["artifacts"]["research"][consumer_style]).write_bytes(self.salary_block())
                before = {p.name: p.read_bytes() for p in root.iterdir()}
                final = self.invoke("state-check", {"workspace": directory, "workflow": "country-finder"})["result"]
                destination = self.invoke("resolve-files", {"workspace": directory, "workflow": "salary-calculator"})["result"]
                self.assertTrue(final["completed"])
                self.assertEqual(final["files"]["final-results"], producer["artifacts"]["final-results"][producer_style])
                self.assertEqual(destination["files"]["final-results"], consumer["artifacts"]["final-results"][consumer_style])
                self.assertEqual({p.name: p.read_bytes() for p in root.iterdir()}, before)

    def test_missing_state_reports_orphan_final_and_ladder_without_creating_state(self):
        for filename in ("sc-step5a-career-ladder.md", "salary-calculator-05a-career-ladder.md",
                         "sc-step5b-final-verification.md", "salary-calculator-05b-final-results.md"):
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as directory:
                path = Path(directory, filename)
                path.write_bytes(b"DUMMY imported result\r\n")
                result = self.invoke("state-check", {"workspace": directory, "workflow": "salary-calculator"})["result"]
                self.assertEqual((result["status"], result["completed"], result["existing_outputs"]), ("missing", False, [filename]))
                self.assertEqual([p.name for p in Path(directory).iterdir()], [filename])

    def test_alias_added_after_scan_blocks_ingestion_without_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("salary-calculator-01-research.md").write_bytes(self.salary_block())
            payload = {"workspace": directory, "workflow": "salary-calculator", "expected": ["Germany"]}
            scan = self.invoke("research-scan", payload)["result"]
            root.joinpath("sc-step1-salary-research.md").write_bytes(self.salary_block())
            before = {p.name: p.read_bytes() for p in root.iterdir()}
            self.invoke("ingest", {**payload, "source_hash": scan["source_hash"], "stored_hash": scan["stored_hash"],
                "decisions": [{"index": 0, "accept": True}]}, 5)
            self.assertEqual({p.name: p.read_bytes() for p in root.iterdir()}, before)

    def test_current_discovery_uses_candidates_without_ingestion(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "country-finder-02-candidates.md")
            path.write_bytes(b"Country: Germany\nRemote:\n- Suitable: yes\nSponsorship:\n- Suitable: yes\n")
            result = self.invoke("research-scan", {"workspace": directory, "workflow": "country-finder",
                "stage": "discovery", "expected": ["Germany"]})["result"]
            self.assertEqual(result["blocks"][0]["country"], "Germany")
            self.assertEqual([p.name for p in Path(directory).iterdir()], [path.name])

    def test_filename_resolution_rejects_unsafe_aliases_and_uncheckpointed_workflows(self):
        for filename in ("country-finder-06-final-results.md", "cf-step6-final-ranking.md"):
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
                target = Path(outside, "private.md")
                target.write_bytes(b"DUMMY private text")
                try:
                    Path(directory, filename).symlink_to(target)
                except OSError:
                    self.skipTest("Symlink creation not permitted on this platform")
                self.invoke("resolve-files", {"workspace": directory, "workflow": "country-finder"}, 2)
                self.assertEqual(target.read_bytes(), b"DUMMY private text")
        with tempfile.TemporaryDirectory() as directory:
            for workflow in ("portal-finder", "job-screener", "../country-finder"):
                self.invoke("resolve-files", {"workspace": directory, "workflow": workflow}, 2)
            Path(directory, "country-finder-01-criteria.md").mkdir()
            self.invoke("resolve-files", {"workspace": directory, "workflow": "country-finder"}, 2)

    def test_checkpoint_completion_supports_both_filename_families(self):
        registry = json.loads((ROOT / "data" / "workspace-files.json").read_text(encoding="utf-8"))
        for workflow, definition in registry["workflows"].items():
            for spelling in ("current", "legacy"):
                for step in range(1, max(a["step"] for a in definition["artifacts"].values()) + 1):
                    with self.subTest(workflow=workflow, spelling=spelling, step=step), tempfile.TemporaryDirectory() as directory:
                        root = Path(directory)
                        for artifact in definition["artifacts"].values():
                            if artifact["step"] <= step:
                                root.joinpath(artifact[spelling]).write_bytes(b"DUMMY saved result\r\n")
                        root.joinpath(definition["state"]).write_text(json.dumps({
                            "last_completed_step": step, "updated_at": "2026-10-22T00:00:00Z"}), encoding="utf-8")
                        before = {p.name: p.read_bytes() for p in root.iterdir()}
                        result = self.invoke("state-check", {"workspace": directory, "workflow": workflow})["result"]
                        self.assertEqual(result["status"], "complete" if step == max(a["step"] for a in definition["artifacts"].values()) else "in_progress")
                        self.assertEqual({p.name: p.read_bytes() for p in root.iterdir()}, before)

    def test_final_checkpoints_reject_empty_or_missing_required_artifacts(self):
        registry = json.loads((ROOT / "data" / "workspace-files.json").read_text(encoding="utf-8"))
        for workflow, definition in registry["workflows"].items():
            artifacts = definition["artifacts"]
            defects = ["empty final"] + (["missing career ladder"] if workflow == "salary-calculator" else [])
            for spelling in ("current", "legacy"):
                for defect in defects:
                    with self.subTest(workflow=workflow, spelling=spelling, defect=defect), tempfile.TemporaryDirectory() as directory:
                        root = Path(directory)
                        for artifact in artifacts.values():
                            root.joinpath(artifact[spelling]).write_bytes(b"DUMMY saved result\r\n")
                        root.joinpath(definition["state"]).write_text(json.dumps({
                            "last_completed_step": max(a["step"] for a in artifacts.values()),
                            "updated_at": "2026-10-28T00:00:00Z"}), encoding="utf-8")
                        missing = artifacts["final-results" if defect == "empty final" else "career-ladder"][spelling]
                        if defect == "empty final":
                            root.joinpath(missing).write_bytes(b" \r\n\t")
                        else:
                            root.joinpath(missing).unlink()
                        before = {p.name: p.read_bytes() for p in root.iterdir()}
                        result = self.invoke("state-check", {"workspace": directory, "workflow": workflow})["result"]
                        self.assertEqual(result["status"], "inconsistent")
                        self.assertIs(result["completed"], False)
                        self.assertEqual(result["missing"], [missing])
                        self.assertEqual({p.name: p.read_bytes() for p in root.iterdir()}, before)

    def test_current_research_ingestion_preserves_bytes_and_uses_no_legacy_copies(self):
        for workflow, source_name, stored_name, raw, tracks in (
                ("salary-calculator", "salary-calculator-01-research.md", "salary-calculator-02-validated-data.md", self.salary_block(), {}),
                ("country-finder", "country-finder-03-research.md", "country-finder-04-validated-data.md", self.country_block(), {"Germany": ["remote", "sponsorship"]})):
            with self.subTest(workflow=workflow), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                root.joinpath(source_name).write_bytes(raw)
                payload = {"workspace": directory, "workflow": workflow, "expected": ["Germany"]}
                if tracks:
                    payload["required_tracks"] = tracks
                for iteration in range(2):
                    scan = self.invoke("research-scan", payload)["result"]
                    result = self.invoke("ingest", {**payload, "source_hash": scan["source_hash"], "stored_hash": scan["stored_hash"],
                        "decisions": [{"index": 0, "accept": True}]})["result"]
                    self.assertEqual(root.joinpath(stored_name).read_bytes(), raw)
                    if iteration:
                        self.assertEqual(result["written_paths"], [])
                self.assertEqual({p.name for p in root.iterdir()}, {source_name, stored_name})

    def test_saved_render_checks_resolve_current_and_legacy_names(self):
        for kind, request, current, legacy in (
                ("salary", self.salary_request(), "salary-calculator-04-salary-table.md", "sc-step4-salary-table.md"),
                ("salary", self.salary_request(), "salary-calculator-05b-final-results.md", "sc-step5b-final-verification.md"),
                ("country", self.country_request(), "country-finder-06-final-results.md", "cf-step6-final-ranking.md")):
            rendered = self.invoke("render-" + ("salary" if kind == "salary" else "cf"), request)["result"]["markdown"]
            for existing in (current, legacy):
                with self.subTest(kind=kind, existing=existing), tempfile.TemporaryDirectory() as directory:
                    path = Path(directory, existing)
                    path.write_text(rendered, encoding="utf-8")
                    before = path.read_bytes()
                    for requested in (current, legacy):
                        self.assertTrue(self.invoke("check-saved", {"workspace": directory, "file": requested,
                            "kind": kind, "render_input": request})["result"]["valid"])
                    self.assertEqual((path.read_bytes(), len(list(Path(directory).iterdir()))), (before, 1))

    def test_strict_schema(self):
        self.invoke("batch-partition", {"groups": [], "unexpected": True}, 2)

    def test_strict_wire_inputs(self):
        for raw in (b'{"schema_version":1,"schema_version":1}', b'{"schema_version":true}',
                    b'{"schema_version":1,"groups":NaN}', b'{"schema_version":1,"groups":[{"region":"\\ud800","countries":[]}]}',
                    b'[]', b'\xff', b'[' * 40 + b'0' + b']' * 40):
            with self.subTest(raw=raw):
                result = subprocess.run([sys.executable, "-I", "-B", str(CLI), "batch-partition"], input=raw, capture_output=True)
                self.assertEqual((result.returncode, result.stdout), (2, b""))
                self.assertEqual(json.loads(result.stderr)["error"]["kind"], "invalid_input")

    def test_batch_duplicate_alias(self):
        self.invoke("batch-partition", {"groups": [{"region": "Demo", "countries": ["Germany 🇩🇪", "🇩🇪 GERMANY"]}]}, 2)
        self.invoke("batch-partition", {"groups": [{"region": "Demo", "countries": ["USA", "United States"]}], "aliases": {"USA": "United States"}}, 2)

    def test_batch_properties(self):
        for count in (0, 1, 15, 16, 17, 37, 100):
            with self.subTest(count=count):
                groups = [{"region": "A", "countries": [f"Example {i}" for i in range(count)]}, {"region": "B", "countries": ["Other"]}]
                result = self.invoke("batch-partition", {"groups": groups})["result"]
                self.assertEqual([c for b in result["batches"] for c in b["countries"]], [c for g in groups for c in g["countries"]])
                self.assertTrue(all(len(b["countries"]) <= 15 for b in result["batches"]))

    @staticmethod
    def comparison():
        return {"pay": {"low": "12000", "high": "24000", "currency": "EUR", "period": "annual", "basis": "gross_base"},
                "minimum": {"amount": "1000", "currency": "EUR", "period": "monthly", "basis": "gross_base", "hard_floor": True}}

    def test_comparison_outcomes(self):
        for amount, expected, failed in (("1000", "pass", False), ("1500", "uncertain", False),
                                         ("2000", "uncertain", False), ("2000.00001", "fail", True)):
            with self.subTest(amount=amount):
                payload = self.comparison()
                payload["minimum"]["amount"] = amount
                result = self.invoke("compare", payload)["result"]
                self.assertEqual(result["outcome"], expected)
                self.assertIs(result["hard_floor_failed"], failed)
                payload["minimum"]["hard_floor"] = False
                self.assertFalse(self.invoke("compare", payload)["result"]["hard_floor_failed"])

    def test_fx_exact_reciprocal_and_cross(self):
        payload = self.comparison()
        payload["minimum"]["currency"] = "USD"
        payload["quotes"] = [{"base": "EUR", "quote": "USD", "rate": "3", "date": "2026-10-21", "source": "https://example.invalid/dummy"}]
        self.assertEqual(self.invoke("compare", payload)["result"]["normalized_minimum"], "4000")
        payload["quotes"] = [
            {"base": "USD", "quote": "JPY", "rate": "150", "date": "2026-10-21", "source": "https://example.invalid/dummy"},
            {"base": "EUR", "quote": "JPY", "rate": "180", "date": "2026-10-21", "source": "https://example.invalid/dummy"}]
        self.assertEqual(self.invoke("compare", payload)["result"]["fx_multiplier"], "5/6")
        payload["multiple"] = "3/2"
        self.assertEqual(self.invoke("compare", payload)["result"]["normalized_minimum"], "15000")
        payload["quotes"][1]["date"] = "2026-10-20"
        self.invoke("compare", payload, 2)

    def test_unverified_comparison_does_not_fail(self):
        for field in ("basis", "period", "currency"):
            payload = self.comparison()
            payload["minimum"][field] = None
            result = self.invoke("compare", payload)["result"]
            self.assertEqual(result["outcome"], "unverified")
            self.assertIs(result["hard_floor_failed"], False)
        payload = self.comparison()
        payload["minimum"]["basis"] = "net"
        result = self.invoke("compare", payload)["result"]
        self.assertEqual(result["outcome"], "unverified")
        self.assertIs(result["hard_floor_failed"], False)
        payload = self.comparison()
        payload["minimum"]["currency"] = "USD"
        result = self.invoke("compare", payload)["result"]
        self.assertEqual(result["outcome"], "unverified")
        self.assertIs(result["hard_floor_failed"], False)

    def test_invalid_comparisons(self):
        for value in ("NaN", "Infinity", "1e9", "1/0", -1, 1.5, True, " 100", "-1"):
            payload = self.comparison()
            payload["minimum"]["amount"] = value
            self.invoke("compare", payload, 2)

    def test_adjustment_bands_and_evidence(self):
        for value, label in (("0", "Small"), ("5", "Small"), ("5.001", "Moderate"), ("10", "Moderate"), ("10.001", "Significant"), ("15", "Significant")):
            payload = {"low": "0", "high": "15", "typical": value, "label": label, "confidence": "Medium", "salary_evidence": "Low", "evidence": "DUMMY evidence only"}
            self.assertEqual(self.invoke("adjust-check", payload)["result"]["evidence_substantive"], "not_checked")
        payload["evidence"] = ""
        self.invoke("adjust-check", payload, 2)

    @staticmethod
    def salary_request():
        return {"rows": [{"country": "Germany 🇩🇪", "calculation": {
            "schema_version": 1, "country": "Germany", "currency": "EUR", "pay_basis": "gross_base",
            "segments": {"mainstream": {"market_midpoint": "62500", "adjustment_percent": "6.8"},
                         "premium": {"market_midpoint": "80000", "adjustment_percent": "6.8"}}},
            "visa": {"state": "Verified numeric", "amount": "58275", "period": "annual", "currency": "EUR", "pay_basis": "gross_base"}}]}

    def test_salary_golden_raw_warning(self):
        result = self.invoke("render-salary", self.salary_request())["result"]
        self.assertIn("| 🇩🇪 Germany (EUR) | 58,275/yr ⚠️ | 58,500 | 74,500 | 4,850 | 6,200 |\n", result["markdown"])
        self.assertEqual(result["calculations"][0]["segments"]["mainstream"]["raw_annual"], "58250")

    def test_salary_rows_follow_priority_aliases_then_alphabetic_extras(self):
        payload = {"rows": [], "priority_order": ["NL", "DE"], "aliases": {"NL": "Netherlands", "DE": "Germany"}}
        for country, display in (("Germany", "Germany 🇩🇪"), ("France", "France 🇫🇷"),
                                 ("Netherlands", "🇳🇱 Netherlands"), ("Austria", "🇦🇹 Austria")):
            row = self.salary_request()["rows"][0]
            row["country"] = display
            row["calculation"]["country"] = country
            payload["rows"].append(row)
        result = self.invoke("render-salary", payload)["result"]
        self.assertEqual([line.split("|")[1].strip() for line in result["table_markdown"].splitlines()[2:]],
                         ["🇳🇱 Netherlands (EUR)", "🇩🇪 Germany (EUR)", "🇦🇹 Austria (EUR)", "🇫🇷 France (EUR)"])

    def test_visa_states(self):
        for state, label in (("Unknown", "Unknown"), ("Blocked", "Blocked"), ("No fixed threshold", "No fixed minimum"), ("Not applicable", "Not applicable")):
            payload = self.salary_request()
            payload["rows"][0]["visa"] = {"state": state, "reason": "DUMMY paused category"}
            result = self.invoke("render-salary", payload)["result"]
            self.assertIn("| " + label + " |", result["markdown"])
        payload = self.salary_request()
        payload["rows"][0]["visa"]["amount"] = "58250"
        self.assertNotIn("⚠️", self.invoke("render-salary", payload)["result"]["markdown"])

    def test_unverified_monthly_basis_keeps_salary_without_visa_pass(self):
        payload = self.salary_request()
        row = payload["rows"][0]
        row["calculation"]["segments"] = {"mainstream": {"raw_annual_target": "60000"}, "premium": {"raw_annual_target": "84000"}}
        row["visa"] = {"state": "Unknown"}
        result = self.invoke("render-salary", payload)["result"]
        self.assertIn("| 🇩🇪 Germany (EUR) | Unknown | 60,000 | 84,000 | 5,000 | 7,000 |", result["markdown"])
        self.assertEqual(result["calculations"][0]["segments"]["mainstream"]["comparisons"], {})

    @staticmethod
    def country_request():
        return {"expected": ["Germany", "Netherlands", "Canada"], "early_exclusions": {"Germany": {"remote": "outside timezone limit"}}, "decisions": [
            {"country": "Germany 🇩🇪", "remote": "Excluded", "sponsorship": "Moderate", "priority": "🥉 Monitor", "limitation": "Remote timezone", "ingestion": "stored", "remote_reason": "outside timezone limit"},
            {"country": "🇳🇱 Netherlands", "remote": "not scored (no data)", "sponsorship": "not scored (no data)", "priority": "Pending evidence", "limitation": "Missing research", "ingestion": "rejected", "ingestion_reason": "Missing sources", "remote_reason": "Missing sources", "sponsorship_reason": "Missing sources"},
            {"country": "🇨🇦 Canada", "remote": "Weak", "sponsorship": "Excluded", "priority": "🎗️ Deprioritize", "limitation": "Limited role market", "ingestion": "stored", "sponsorship_reason": "DUMMY unavailable route"}]}

    def test_country_golden_and_coverage(self):
        result = self.invoke("render-cf", self.country_request())["result"]
        self.assertIn("| 🇩🇪 Germany | 🥉 Monitor | Excluded | Moderate | Remote timezone |", result["table_markdown"])
        self.assertIn("Researched but not ingested", result["summary_markdown"])
        self.assertNotIn("| 🇳🇱 Netherlands |", result["summary_markdown"])
        self.assertEqual(result["counts"]["remote"], {"scored": 1, "excluded": 1, "not_scored": 1})
        self.assertIn("outside timezone limit", " ".join(result["audit_notes"]))

    def test_country_priority_order_is_stable_with_alphabetic_pending_rows(self):
        payload = {"expected": ["ZA", "Netherlands", "Canada", "DE", "Austria", "France", "Japan"],
                   "aliases": {"ZA": "South Africa", "DE": "Germany"}, "early_exclusions": {}, "decisions": []}
        for country, priority, remote, sponsorship in (
            ("🇿🇦 South Africa", "Pending evidence", "not scored (no data)", "not scored (no data)"),
            ("🇳🇱 Netherlands", "🥇 Focus", "Strong", "Moderate"),
            ("🇨🇦 Canada", "Pending evidence", "not scored (no data)", "not scored (no data)"),
            ("Germany 🇩🇪", "🥉 Monitor", "Moderate", "Weak"),
            ("Austria 🇦🇹", "🥇 Focus", "Strong", "Strong"),
            ("🇫🇷 France", "🎗️ Deprioritize", "Weak", "Weak"),
            ("🇯🇵 Japan", "🥈 Selective", "Moderate", "Weak"),
        ):
            decision = {"country": country, "priority": priority, "remote": remote, "sponsorship": sponsorship,
                        "ingestion": "stored", "limitation": "DUMMY evidence-based order"}
            if priority == "Pending evidence":
                decision.update(ingestion="not_supplied", remote_reason="DUMMY missing research",
                                sponsorship_reason="DUMMY missing research", ingestion_reason="DUMMY missing research")
            payload["decisions"].append(decision)
        result = self.invoke("render-cf", payload)["result"]
        self.assertEqual([line.split("|")[1].strip() for line in result["table_markdown"].splitlines()[2:]],
                         ["🇳🇱 Netherlands", "🇦🇹 Austria", "🇯🇵 Japan", "🇩🇪 Germany", "🇫🇷 France", "🇨🇦 Canada", "🇿🇦 South Africa"])

    def test_country_contradictions(self):
        for action in (lambda p: p["decisions"][0].update(remote="Weak"),
                       lambda p: p["decisions"][1].update(priority="🥇 Focus"),
                       lambda p: p["decisions"].pop(),
                       lambda p: p["decisions"].append(p["decisions"][0])):
            payload = self.country_request()
            action(payload)
            self.invoke("render-cf", payload, 2)
        payload = self.country_request()
        payload["early_exclusions"]["🇩🇪 Germany"] = {"sponsorship": "other reason"}
        self.invoke("render-cf", payload, 2)

    def test_country_scored_track_requires_stored_research_with_an_exclusion(self):
        for excluded, scored in (("remote", "sponsorship"), ("sponsorship", "remote")):
            for fit, priority in (("Strong", "🥇 Focus"), ("Moderate", "🥉 Monitor"), ("Weak", "🎗️ Deprioritize")):
                for ingestion in ("stored", "not_supplied", "rejected", "unknown"):
                    with self.subTest(excluded=excluded, scored=fit, ingestion=ingestion):
                        decision = {"country": "Germany 🇩🇪", excluded: "Excluded", scored: fit,
                                    "priority": priority, "limitation": "DUMMY track limitation", "ingestion": ingestion,
                                    excluded + "_reason": "DUMMY early exclusion"}
                        payload = {"expected": ["Germany"], "early_exclusions": {"Germany": {excluded: "DUMMY early exclusion"}},
                                   "decisions": [decision]}
                        response = self.invoke("render-cf", payload, 0 if ingestion == "stored" else 2)
                        if ingestion == "stored":
                            self.assertEqual(response["result"]["counts"][excluded], {"scored": 0, "excluded": 1, "not_scored": 0})
                            self.assertEqual(response["result"]["counts"][scored], {"scored": 1, "excluded": 0, "not_scored": 0})
                        else:
                            self.assertEqual(response["error"]["kind"], "invalid_input")
                            self.assertEqual(response["error"]["message"], "Scored tracks need stored research")

    def test_country_nonstored_exclusions_remain_valid(self):
        for ingestion in ("stored", "not_supplied", "rejected", "unknown"):
            for excluded in ("remote", "sponsorship", "both"):
                with self.subTest(ingestion=ingestion, excluded=excluded):
                    decision = {"country": "Germany 🇩🇪", "priority": "Pending evidence", "limitation": "DUMMY research gap",
                                "ingestion": ingestion, "remote": "not scored (no data)", "sponsorship": "not scored (no data)",
                                "remote_reason": "DUMMY missing research", "sponsorship_reason": "DUMMY missing research"}
                    early = {}
                    for track in ("remote", "sponsorship"):
                        if excluded in (track, "both"):
                            decision[track] = "Excluded"
                            decision[track + "_reason"] = "DUMMY early " + track + " exclusion"
                            early[track] = decision[track + "_reason"]
                    if excluded == "both":
                        decision["priority"] = "🎗️ Deprioritize"
                    result = self.invoke("render-cf", {"expected": ["Germany"], "early_exclusions": {"Germany": early},
                                                       "decisions": [decision]})["result"]
                    for track in ("remote", "sponsorship"):
                        self.assertEqual(result["counts"][track], {"scored": 0, "excluded": int(track in early),
                                                                  "not_scored": int(track not in early)})
                        self.assertIn("🇩🇪 Germany " + track + ": " + decision[track + "_reason"], result["audit_notes"])
                    expected = "| 🇩🇪 Germany | " + decision["remote"] + " | " + decision["sponsorship"] + " |"
                    self.assertIn(expected, result["summary_markdown"])

    def test_saved_content_mismatch(self):
        for kind, request, filename in (("salary", self.salary_request(), "sc-step4-salary-table.md"), ("country", self.country_request(), "cf-step6-final-ranking.md")):
            with tempfile.TemporaryDirectory() as directory:
                rendered = self.invoke("render-" + ("salary" if kind == "salary" else "cf"), request)["result"]["markdown"]
                path = Path(directory, filename)
                path.write_text("# DUMMY audit\n\n" + rendered + "\n## Other\nPreserved.\n", encoding="utf-8")
                check = {"workspace": directory, "file": filename, "kind": kind, "render_input": request}
                self.assertTrue(self.invoke("check-saved", check)["result"]["valid"])
                path.write_text(path.read_text(encoding="utf-8").replace("Germany", "Wrong country"), encoding="utf-8")
                self.invoke("check-saved", check, 2)

    @staticmethod
    def salary_block(country="Germany"):
        return (f"Country: {country}\r\n\r\nMid-size / Mainstream Local-Market tier:\r\n- Low: 50000 EUR\r\n"
                "- Realistic: 62500 EUR\r\n- Strong: 70000 EUR\r\n- Sources: DUMMY https://example.invalid/a\r\n"
                "Premium / International / Remote-first tier:\r\n- Low: 70000 EUR\r\n- Realistic: 80000 EUR\r\n"
                "- Strong: 90000 EUR\r\n- Sources: DUMMY https://example.invalid/b\r\n").encode("utf-8")

    def test_ingest_byte_preservation_idempotency_and_duplicate(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory, "sc-step1-salary-research.md")
            original = self.salary_block()
            raw = b"## Research scope\r\nGermany, France\r\n\r\n" + original + self.salary_block("GERMANY 🇩🇪")
            source.write_bytes(raw)
            payload = {"workspace": directory, "workflow": "salary-calculator", "expected": ["Germany", "France"]}
            scan = self.invoke("research-scan", payload)["result"]
            ingest = {**payload, "source_hash": scan["source_hash"], "stored_hash": scan["stored_hash"], "decisions": [{"index": 0, "accept": True}, {"index": 1, "accept": True}]}
            result = self.invoke("ingest", ingest)["result"]
            self.assertEqual(result["expected_not_stored"], ["France"])
            self.assertEqual(Path(directory, "sc-step2-salary-data.md").read_bytes(), original)
            self.assertTrue(source.read_bytes().startswith(raw))
            self.invoke("ingest", ingest, 5)
            before = source.read_bytes()
            scan = self.invoke("research-scan", payload)["result"]
            ingest.update(source_hash=scan["source_hash"], stored_hash=scan["stored_hash"])
            self.assertEqual(self.invoke("ingest", ingest)["result"]["written_paths"], [])
            self.assertEqual(source.read_bytes(), before)

    def test_research_boundaries(self):
        for raw, expected, code in (
            (b'```research\nCountry: Germany\nCountry: France\n```\n', 1, 0),
            (b'```text\nCountry: Germany\n```\n```text\nCountry: France\n```\n', 2, 0),
            (b'Country: Germany\n> Country: quoted\n```json\nCountry: example\n```\nCountry: France\n', 2, 0),
            (b'Germany salary data without a delimiter', 0, 4),
            (b'```research\nCountry: Germany\n', 0, 4)):
            with self.subTest(raw=raw), tempfile.TemporaryDirectory() as directory:
                Path(directory, "sc-step1-salary-research.md").write_bytes(raw)
                result = self.invoke("research-scan", {"workspace": directory, "workflow": "salary-calculator", "expected": ["Germany", "France"]}, code)
                if code == 0:
                    self.assertEqual(len(result["result"]["blocks"]), expected)

    def test_ingest_rejects_structural_issues_despite_acceptance(self):
        for label, invalid, country, reason, valid_country, expected, missing in (
            ("multiple countries in one dataset", b"```research\nCountry: Germany\nCountry: France\n```\n\n",
             "Germany", "Explicit dataset must contain exactly one country", "Netherlands",
             ["Germany", "France", "Netherlands"], ["Germany", "France"]),
            ("flag without a country name", self.salary_block("🇩🇪"), "🇩🇪", "Unrecognizable country",
             "Germany", ["Germany"], []),
        ):
            with self.subTest(case=label), tempfile.TemporaryDirectory() as directory:
                source = Path(directory, "sc-step1-salary-research.md")
                valid = self.salary_block(valid_country) + b"\n"
                raw = invalid + valid
                source.write_bytes(raw)
                payload = {"workspace": directory, "workflow": "salary-calculator", "expected": expected}
                scan = self.invoke("research-scan", payload)["result"]
                self.assertEqual(len(scan["blocks"]), 2)
                self.assertEqual(scan["blocks"][0]["issues"], [reason])
                result = self.invoke("ingest", {**payload, "source_hash": scan["source_hash"], "stored_hash": None,
                    "decisions": [{"index": index, "accept": True, "reviewed_fields": True} for index in (0, 1)]})["result"]
                self.assertEqual(result["stored"], 1)
                self.assertEqual(result["rejected"], [{"index": 0, "country": country, "reason": reason}])
                self.assertEqual(result["expected_not_stored"], missing)
                self.assertEqual(Path(directory, "sc-step2-salary-data.md").read_bytes(), valid)
                self.assertEqual(source.read_bytes().partition(b"## Validation report\n")[0], raw)

    def test_ingest_rejects_ineligible_country_despite_acceptance(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory, "cf-step3-country-research.md")
            valid = self.country_block() + b"\n"
            invalid = valid.replace(b"Country: Germany", b"Country: Canada", 1)
            raw = invalid + valid
            source.write_bytes(raw)
            payload = {"workspace": directory, "workflow": "country-finder", "expected": ["Canada", "Germany"],
                       "required_tracks": {"Germany": ["remote", "sponsorship"]}}
            scan = self.invoke("research-scan", payload)["result"]
            self.assertEqual(len(scan["blocks"]), 2)
            self.assertEqual(scan["blocks"][0]["issues"], ["Country not eligible on either track"])
            result = self.invoke("ingest", {**payload, "source_hash": scan["source_hash"], "stored_hash": None,
                "decisions": [{"index": index, "accept": True, "reviewed_fields": True} for index in (0, 1)]})["result"]
            self.assertEqual(result["stored"], 1)
            self.assertEqual(result["rejected"], [{"index": 0, "country": "Canada", "reason": "Country not eligible on either track"}])
            self.assertEqual(result["expected_not_stored"], ["Canada"])
            self.assertEqual(Path(directory, "cf-step4-country-data.md").read_bytes(), valid)
            self.assertEqual(source.read_bytes().partition(b"## Validation report\n")[0], raw)

    def test_provenance_notes_preserve_raw_and_legacy_compatibility(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = self.salary_block() + self.salary_block("Netherlands").replace(
                b"- Sources:", b"- Benchmark basis: DUMMY national full-time annual gross base\r\n- Estimate method: DUMMY analyst selection, not a published median\r\n- Sources:")
            Path(directory, "sc-step1-salary-research.md").write_bytes(raw)
            payload = {"workspace": directory, "workflow": "salary-calculator", "expected": ["Germany", "Netherlands"]}
            scan = self.invoke("research-scan", payload)["result"]
            self.assertTrue(all(not block["missing_fields"] for block in scan["blocks"]))
            self.invoke("ingest", {**payload, "source_hash": scan["source_hash"], "stored_hash": None,
                "decisions": [{"index": 0, "accept": True}, {"index": 1, "accept": True}]})
            self.assertEqual(Path(directory, "sc-step2-salary-data.md").read_bytes(), raw)

    def test_empty_ingestion_is_a_record_not_a_completed_salary_run(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "sc-step1-salary-research.md").write_bytes(self.salary_block())
            payload = {"workspace": directory, "workflow": "salary-calculator", "expected": ["Germany"]}
            scan = self.invoke("research-scan", payload)["result"]
            result = self.invoke("ingest", {**payload, "source_hash": scan["source_hash"], "stored_hash": None,
                "decisions": [{"index": 0, "accept": False, "reason": "DUMMY unusable research"}]})["result"]
            self.assertEqual((result["stored"], Path(directory, "sc-step2-salary-data.md").read_bytes()), (0, b""))
            Path(directory, ".salary-calculator-state.json").write_text('{"last_completed_step":2,"updated_at":"2026-10-21T00:00:00Z"}', encoding="utf-8")
            state = self.invoke("state-check", {"workspace": directory, "workflow": "salary-calculator"})["result"]
            self.assertEqual((state["status"], state["completed"]), ("in_progress", False))

    def test_appended_research_after_report_is_not_deleted(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = self.salary_block() + b"\n## Validation report\nLegacy generated report.\nCountry: France\nNew findings.\n"
            source = Path(directory, "sc-step1-salary-research.md")
            source.write_bytes(raw)
            self.invoke("research-scan", {"workspace": directory, "workflow": "salary-calculator", "expected": ["Germany", "France"]}, 4)
            self.assertEqual(source.read_bytes(), raw)

    def test_reversed_salary_tiers_and_unicode_separator(self):
        raw = self.salary_block().decode("utf-8")
        header, rest = raw.split("\r\n", 1)
        first, second = rest.split("Premium / International / Remote-first tier:", 1)
        swapped = header + "\nPremium / International / Remote-first tier:" + second + first
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "sc-step1-salary-research.md")
            path.write_text(swapped + "\nNotes: example\u2028Country: Not-a-dataset\n", encoding="utf-8")
            result = self.invoke("research-scan", {"workspace": directory, "workflow": "salary-calculator", "expected": ["Germany"]})["result"]
            self.assertEqual(len(result["blocks"]), 1)
            self.assertEqual(result["blocks"][0]["missing_fields"], [])

    def test_cf_tracks_cannot_be_omitted(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "cf-step3-country-research.md").write_text("Country: Germany\nRemote Track:\n", encoding="utf-8")
            self.invoke("research-scan", {"workspace": directory, "workflow": "country-finder", "expected": ["Germany"]}, 2)
            self.assertFalse(Path(directory, "cf-step4-country-data.md").exists())

    @staticmethod
    def country_block():
        return ("Country: Germany\nRemote Track:\n- Confirmed salary range: DUMMY 50000 EUR annual gross base\n"
                "- Hiring prevalence evidence: DUMMY\n- Payment structure norms: DUMMY employee\n"
                "- Sources: DUMMY https://example.invalid/remote\nSponsorship Track:\n"
                "- Visa or pathway name: DUMMY route\n- Minimum salary threshold: Unknown\n"
                "- Employer willingness: DUMMY\n- Processing time: Unknown\n- Quota or cap limitations: Unknown\n"
                "- Family or dependent provisions: Unknown\n- Citizenship-specific considerations: Unknown\n"
                "- Sources: DUMMY https://example.invalid/sponsor\n").encode("utf-8")

    def test_cf_required_fields_are_track_scoped(self):
        raw = self.country_block().replace(b"- Sources: DUMMY https://example.invalid/sponsor\n", b"")
        self.assertIn("sponsorship: sources:", research.missing_fields(
            {"raw": raw}, "country-finder", ["remote", "sponsorship"]))

    def test_salary_required_sources_exclude_trailing_metadata(self):
        for trailer in (b"Notes: sources: DUMMY\n", b"Sponsorship salary threshold: Unknown; sources: DUMMY\n",
                        b"Evidence grade: Low; sources: DUMMY\n"):
            with self.subTest(trailer=trailer):
                raw = self.salary_block().replace(b"- Sources: DUMMY https://example.invalid/b\r\n", b"") + trailer
                self.assertIn("premium / international / remote-first tier: sources:",
                              research.missing_fields({"raw": raw}, "salary-calculator", []))

    def test_required_labels_in_quoted_or_fenced_evidence_do_not_count(self):
        for quote in (b"> - Sources: DUMMY\n", b"```text\n- Sources: DUMMY\n```\n",
                      b"~~~markdown\n- Sources: DUMMY\n~~~\n", b"- Reason: Example Sources: DUMMY\n"):
            with self.subTest(quote=quote):
                raw = self.country_block().replace(b"- Sources: DUMMY https://example.invalid/sponsor\n", quote)
                self.assertIn("sponsorship: sources:", research.missing_fields(
                    {"raw": raw}, "country-finder", ["remote", "sponsorship"]))

    def test_common_field_emphasis_and_template_headings(self):
        for workflow, raw, tracks in (("country-finder", self.country_block(), ["remote", "sponsorship"]),
                                      ("salary-calculator", self.salary_block(), [])):
            for bullet in ("-", "*", "+"):
                with self.subTest(workflow=workflow, bullet=bullet):
                    value = raw.decode("utf-8").replace("Remote Track:", "Remote Track (include only if applicable):").replace(
                        "Sponsorship Track:", "Sponsorship Track (include only if applicable):")
                    value = "\n".join((bullet + " **" + line[2:].split(":", 1)[0] + ":**" + line.split(":", 1)[1]
                                       if line.startswith("- ") else "**" + line.rstrip("\r") + "**"
                                       if "tier:" in line.casefold() or "track (" in line.casefold() else line)
                                      for line in value.split("\n"))
                    self.assertEqual(research.missing_fields({"raw": value.encode("utf-8")}, workflow, tracks), [])

    def test_legacy_fields_need_review_and_preserve_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = self.salary_block().replace(b"- Sources:", b"- References:")
            path = Path(directory, "sc-step1-salary-research.md")
            path.write_bytes(raw)
            payload = {"workspace": directory, "workflow": "salary-calculator", "expected": ["Germany"]}
            scan = self.invoke("research-scan", payload)["result"]
            request = {**payload, "source_hash": scan["source_hash"], "stored_hash": None,
                       "decisions": [{"index": 0, "accept": True}]}
            self.invoke("ingest", request, 4)
            request["decisions"][0]["reviewed_fields"] = True
            self.invoke("ingest", request)
            self.assertEqual(Path(directory, "sc-step2-salary-data.md").read_bytes(), raw)

    def test_cf_zero_eligible_scope_is_an_accountable_record(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory, "cf-step3-country-research.md")
            source.write_text("## Research scope\nnone\n", encoding="utf-8")
            payload = {"workspace": directory, "workflow": "country-finder", "expected": [], "required_tracks": {}}
            scan = self.invoke("research-scan", payload)["result"]
            result = self.invoke("ingest", {**payload, "source_hash": scan["source_hash"], "stored_hash": None,
                                            "decisions": []})["result"]
            self.assertEqual((result["stored"], Path(directory, "cf-step4-country-data.md").read_bytes()), (0, b""))

    def test_unusable_stored_cf_track_stays_unknown(self):
        payload = self.country_request()
        payload["decisions"][2].update(remote="not scored (no data)", remote_reason="DUMMY evidence inapplicable",
                                       priority="Pending evidence", limitation="Remote evidence inapplicable")
        result = self.invoke("render-cf", payload)["result"]
        self.assertIn("| 🇨🇦 Canada | Pending evidence | Unknown | Excluded |", result["table_markdown"])

    def test_metadata_only_scope_reports_missing_results(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "sc-step1-salary-research.md").write_text("## Research scope\nGermany\n", encoding="utf-8")
            result = self.invoke("research-scan", {"workspace": directory, "workflow": "salary-calculator", "expected": ["Germany"]})["result"]
            self.assertEqual(result["expected_not_supplied"], ["Germany"])
            self.assertEqual(result["blocks"], [])
            Path(directory, "sc-step1-salary-research.md").write_text("## Research scope\nGermany\nUnlabelled legacy salary research follows.\n", encoding="utf-8")
            self.invoke("research-scan", {"workspace": directory, "workflow": "salary-calculator", "expected": ["Germany"]}, 4)

    def test_mixed_reject_then_accept_retry_keeps_attribution(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "sc-step1-salary-research.md").write_bytes(b"Country: Germany\nIncomplete first block\n" + self.salary_block())
            payload = {"workspace": directory, "workflow": "salary-calculator", "expected": ["Germany"]}
            for iteration in range(2):
                scan = self.invoke("research-scan", payload)["result"]
                result = self.invoke("ingest", {**payload, "source_hash": scan["source_hash"], "stored_hash": scan["stored_hash"],
                    "decisions": [{"index": 0, "accept": False, "reason": "Missing both tiers"}, {"index": 1, "accept": True}]})["result"]
                self.assertEqual(result["rejected"], [{"index": 0, "country": "Germany", "reason": "Missing both tiers"}])
                if iteration:
                    self.assertEqual(result["written_paths"], [])

    def test_explicit_fence_preamble_not_discarded(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "sc-step1-salary-research.md")
            path.write_bytes(b"```research\nImportant caveat before the country\n" + self.salary_block() + b"```\n")
            self.invoke("research-scan", {"workspace": directory, "workflow": "salary-calculator", "expected": ["Germany"]}, 4)

    def test_edited_generated_report_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "sc-step1-salary-research.md")
            path.write_bytes(self.salary_block())
            payload = {"workspace": directory, "workflow": "salary-calculator", "expected": ["Germany"]}
            scan = self.invoke("research-scan", payload)["result"]
            self.invoke("ingest", {**payload, "source_hash": scan["source_hash"], "stored_hash": None, "decisions": [{"index": 0, "accept": True}]})
            edited = path.read_bytes().replace(b"Stored: 1", b"Stored: 2")
            path.write_bytes(edited)
            self.invoke("research-scan", payload, 4)
            self.assertEqual(path.read_bytes(), edited)

    def test_explicit_render_alias(self):
        payload = self.country_request()
        payload["expected"][0] = "DE"
        payload["aliases"] = {"DE": "Germany"}
        self.assertEqual(self.invoke("render-cf", payload)["result"]["counts"]["remote"]["excluded"], 1)

    def test_malformed_quotes_do_not_bypass_validation(self):
        payload = self.comparison()
        payload["minimum"]["basis"] = None
        payload["quotes"] = [{"base": "USD", "quote": "EUR", "rate": "0", "date": "2026-10-21", "source": "DUMMY"}]
        self.invoke("compare", payload, 2)

    def test_flag_only_country_is_per_block_issue(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "sc-step1-salary-research.md").write_bytes(self.salary_block("🇩🇪") + self.salary_block())
            result = self.invoke("research-scan", {"workspace": directory, "workflow": "salary-calculator", "expected": ["Germany"]})["result"]
            self.assertTrue(result["blocks"][0]["issues"])
            self.assertEqual(result["blocks"][1]["country"], "Germany")

    def test_non_newline_original_remains_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "sc-step1-salary-research.md").write_bytes(self.salary_block().rstrip(b"\r\n"))
            payload = {"workspace": directory, "workflow": "salary-calculator", "expected": ["Germany"]}
            for iteration in range(2):
                scan = self.invoke("research-scan", payload)["result"]
                result = self.invoke("ingest", {**payload, "source_hash": scan["source_hash"], "stored_hash": scan["stored_hash"], "decisions": [{"index": 0, "accept": True}]})["result"]
                self.assertEqual(result["rejected"], [])
                if iteration:
                    self.assertEqual(result["written_paths"], [])

    def test_saved_eof_and_windows_line_endings(self):
        payload = self.salary_request()
        rendered = self.invoke("render-salary", payload)["result"]["markdown"]
        for value in (rendered.rstrip("\n"), rendered.replace("\n", "\r\n")):
            with tempfile.TemporaryDirectory() as directory:
                Path(directory, "sc-step4-salary-table.md").write_bytes(value.encode("utf-8"))
                self.assertTrue(self.invoke("check-saved", {"workspace": directory, "file": "sc-step4-salary-table.md", "kind": "salary", "render_input": payload})["result"]["valid"])

    def test_mistyped_timezone_is_invalid_data(self):
        try:
            from zoneinfo import ZoneInfo
            ZoneInfo("UTC")
        except (ImportError, KeyError):
            self.skipTest("No system tzdata")
        self.invoke("tz-offsets", {"zones": ["Europe/Berlinn", "UTC"], "instants": ["2026-10-21T00:00:00Z"]}, 2)

    def test_ingest_partial_write_safe_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "sc-step1-salary-research.md").write_bytes(self.salary_block())
            payload = {"workspace": directory, "workflow": "salary-calculator", "expected": ["Germany"]}
            scan = research.scan(payload)
            request = {**payload, "source_hash": scan["source_hash"], "stored_hash": scan["stored_hash"], "decisions": [{"index": 0, "accept": True}]}
            original_replace = research.replace
            def fail_report(path, raw):
                if path.name == "sc-step1-salary-research.md":
                    raise PermissionError("DUMMY second-write failure")
                original_replace(path, raw)
            with patch.object(research, "replace", side_effect=fail_report), self.assertRaises(Problem) as failure:
                research.ingest(request)
            self.assertEqual(failure.exception.details["written_paths"], ["sc-step2-salary-data.md"])
            after = research.scan(payload)
            request.update(source_hash=after["source_hash"], stored_hash=after["stored_hash"])
            research.ingest(request)
            self.assertEqual(Path(directory, "sc-step2-salary-data.md").read_bytes(), self.salary_block())
            self.assertEqual(len(list(Path(directory).iterdir())), 2)

    def test_symlink_and_plugin_workspace_refused(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as other:
            target = Path(other, "secret.md")
            target.write_bytes(self.salary_block())
            try:
                Path(directory, "sc-step1-salary-research.md").symlink_to(target)
            except OSError:
                self.skipTest("Symlink creation not permitted on this platform")
            self.invoke("research-scan", {"workspace": directory, "workflow": "salary-calculator", "expected": []}, 2)
        self.invoke("state-check", {"workspace": str(ROOT), "workflow": "country-finder"}, 2)

    def test_corrupt_and_missing_output_state(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, ".salary-calculator-state.json")
            for state in ({"last_completed_step": True, "updated_at": ""}, {"last_completed_step": 6, "updated_at": ""}, {"last_completed_step": 1, "updated_at": ""}):
                path.write_text(json.dumps(state), encoding="utf-8")
                self.invoke("state-check", {"workspace": directory, "workflow": "salary-calculator"}, 2)
            path.write_text('{"last_completed_step":5,"updated_at":"2026-10-21T00:00:00Z"}', encoding="utf-8")
            result = self.invoke("state-check", {"workspace": directory, "workflow": "salary-calculator"})["result"]
            self.assertEqual(result["status"], "inconsistent")
            self.assertFalse(result["completed"])

    def test_timezones_supplied_instants_and_gap_fold(self):
        try:
            from zoneinfo import ZoneInfo
            ZoneInfo("Europe/Berlin")
        except (ImportError, KeyError):
            self.skipTest("No system IANA timezone data; unavailable path is tested separately")
        result = self.invoke("tz-offsets", {"zones": ["Asia/Manila", "Europe/Berlin"], "instants": ["2026-01-15T00:00:00Z", "2026-07-15T00:00:00Z"]})["result"]
        self.assertEqual([row["absolute_difference_seconds"] for row in result["evaluations"]], [25200, 21600])
        self.assertEqual(result["seasonal_coverage"], "unverified")
        for start, end in (("2026-03-29T02:30:00", "2026-03-29T04:00:00"), ("2026-10-25T02:30:00", "2026-10-25T04:00:00")):
            self.invoke("tz-offsets", {"zones": ["Europe/Berlin", "Asia/Manila"], "instants": [], "schedules": [[{"start": start, "end": end}, {"start": "2026-03-29T08:00:00", "end": "2026-03-29T16:00:00"}]]}, 4)

    def test_missing_tzdata(self):
        from zoneinfo import ZoneInfoNotFoundError
        with patch.object(timezones, "ZoneInfo", side_effect=ZoneInfoNotFoundError("DUMMY missing database")), self.assertRaises(Problem) as failure:
            timezones.offsets({"zones": ["Asia/Manila", "Europe/Berlin"], "instants": ["2026-10-21T00:00:00Z"]})
        self.assertEqual(failure.exception.kind, "runtime_unavailable")

    def test_overnight_schedule(self):
        try:
            from zoneinfo import ZoneInfo
            ZoneInfo("Europe/Berlin")
        except (ImportError, KeyError):
            self.skipTest("No system IANA timezone data")
        payload = {"zones": ["Asia/Manila", "Europe/Berlin"], "instants": [], "schedules": [[
            {"start": "2026-10-21T22:00:00", "end": "2026-10-22T06:00:00"},
            {"start": "2026-10-21T16:00:00", "end": "2026-10-22T00:00:00"}]]}
        self.assertEqual(self.invoke("tz-offsets", payload)["result"]["overlap_seconds"], [28800])

    def test_old_interpreter_is_distinct(self):
        result = subprocess.run([sys.executable, "-I", "-B", "-c",
            "import runpy,sys;sys.version_info=(3,10);sys.argv=sys.argv[1:];runpy.run_path(sys.argv[0],run_name='__main__')",
            str(CLI), "batch-partition"], input=b'{"schema_version":1,"groups":[]}', capture_output=True)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stderr)["error"]["kind"], "runtime_unavailable")

    def test_relocated_package_non_utf8_console(self):
        with tempfile.TemporaryDirectory() as directory:
            install = Path(directory, "installed plügïn")
            install.mkdir()
            shutil.copytree(ROOT / "helpers", install / "helpers", ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copytree(ROOT / "data", install / "data")
            env = {**os.environ, "LC_ALL": "C", "PYTHONIOENCODING": "ascii"}
            result = self.invoke("render-salary", self.salary_request(), cli=install / "helpers" / "compass.py", env=env)
            self.assertIn("🇩🇪", result["result"]["markdown"])
            consumer = Path(directory, "candidate wörkspace")
            consumer.mkdir()
            consumer.joinpath("cf-step6-final-ranking.md").write_bytes(b"DUMMY legacy final\r\n")
            for workflow in ("country-finder", "salary-calculator"):
                result = self.invoke("resolve-files", {"workspace": str(consumer), "workflow": workflow},
                                     cli=install / "helpers" / "compass.py", env=env)["result"]
                self.assertEqual(result["naming"], "legacy" if workflow == "country-finder" else "current")
            consumer.joinpath("sc-step1-salary-research.md").write_text("## Research scope\n- 🇩🇪 Germany\n- 🇫🇷 France\n", encoding="utf-8")
            offered = self.invoke("research-scope", {"workspace": str(consumer), "workflow": "salary-calculator"},
                                  cli=install / "helpers" / "compass.py", env=env)["result"]
            self.assertEqual(offered["countries"], ["🇩🇪 Germany", "🇫🇷 France"])
            self.assertEqual(sorted(p.name for p in consumer.iterdir()), ["cf-step6-final-ranking.md", "sc-step1-salary-research.md"])
            self.assertFalse(list(install.rglob("__pycache__")))


class RunWorkspaces(unittest.TestCase):
    def setUp(self):
        home_patch = patch.object(workspaces.Path, 'home')
        self.home = home_patch.start()
        self.addCleanup(home_patch.stop)

    def request(self, root, chat="codex:chat-a", **extra):
        self.home.return_value = Path(root)
        return {"workspace": str(Path(root)/'Agent Compass'), "chat_id": chat, **extra}

    def start(self, root, chat="codex:chat-a", command="country-finder", name="Fictional Person A", **extra):
        return runs.start(self.request(root, chat, workflow=command, person_label=name, **extra))

    def snapshot(self, root):
        return {str(p.relative_to(root)): p.read_bytes() for p in Path(root).rglob('*') if p.is_file()}

    def finish(self, run):
        root = Path(run["workspace"])
        spec = json.loads((ROOT / 'data/workspace-files.json').read_text())["workflows"][run["workflow"]]
        for artifact in spec["artifacts"].values():
            (root / artifact['current']).write_text('Fictional saved result.\n')
        step = max(a['step'] for a in spec['artifacts'].values())
        (root / spec['state']).write_text(json.dumps({'last_completed_step': step, 'updated_at': '2026-10-29T12:00:00Z'}))

    def test_new_chat_does_not_replay_completed_run_or_root_files(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            (root / 'profile.md').write_text('Fictional old root candidate')
            (root / '.country-finder-state.json').write_text('{"last_completed_step":6}')
            first = self.start(root)
            self.finish(first)
            before = self.snapshot(root)
            self.assertTrue(runs.list_runs(self.request(root))['active_runs'][0]['completed'])
            self.assertEqual(runs.list_runs(self.request(root, 'codex:chat-b'))['active_runs'], [])
            self.assertEqual(self.snapshot(root), before)
            second = self.start(root, 'codex:chat-b')
            self.assertNotEqual(first['person_id'], second['person_id'])
            self.assertNotEqual(first['workspace'], second['workspace'])
            self.assertFalse((Path(second['workspace'])/'profile.md').exists())
            for name, raw in before.items():
                self.assertEqual((root/name).read_bytes(), raw)

    def test_new_person_same_chat_does_not_inherit_profile_or_checkpoint(self):
        with tempfile.TemporaryDirectory() as root:
            first = self.start(root)
            (Path(first['workspace'])/'profile.md').write_text('Fictional person A')
            self.finish(first)
            second = self.start(root, name='Fictional Person B')
            self.assertNotEqual(first['person_id'], second['person_id'])
            self.assertFalse((Path(second['workspace'])/'profile.md').exists())
            statuses = runs.list_runs(self.request(root))['active_runs']
            self.assertEqual(len(statuses), 2)
            self.assertEqual({r['person_id']:r['status'] for r in statuses}[second['person_id']], 'missing')

    def test_start_fresh_requires_selected_baseline_and_preserves_old_results(self):
        for command in ('country-finder','salary-calculator'):
            with self.subTest(command=command), tempfile.TemporaryDirectory() as root:
                old = self.start(root, command=command)
                self.finish(old)
                before = self.snapshot(root)
                with self.assertRaises(Problem):
                    self.start(root, command=command, person_id=old['person_id'])
                new = self.start(root, command=command, person_id=old['person_id'], previous_run_id=old['run_id'])
                latest = runs.list_runs(self.request(root, person_id=old['person_id'], workflow=command))['active_runs']
                self.assertEqual([r['run_id'] for r in latest], [new['run_id']])
                self.assertEqual(latest[0]['status'], 'missing')
                self.assertFalse(latest[0]['completed'])
                for name, raw in before.items():self.assertEqual((Path(root)/name).read_bytes(), raw)
                with self.assertRaises(Problem):
                    self.start(root, command=command, person_id=old['person_id'], previous_run_id=old['run_id'])

    def test_history_is_read_only_and_does_not_promote_old_completed_runs(self):
        with tempfile.TemporaryDirectory() as root:
            old = self.start(root)
            raw = b'Fictional confirmed profile\r\n'
            (Path(old['workspace'])/'profile.md').write_bytes(raw)
            self.finish(old)
            middle = self.start(root, person_id=old['person_id'], previous_run_id=old['run_id'])
            current = self.start(root, person_id=old['person_id'], previous_run_id=middle['run_id'])
            before = self.snapshot(root)
            normal = runs.list_runs(self.request(root))
            self.assertNotIn('history_runs', normal)
            self.assertEqual([(r['run_id'], r['completed']) for r in normal['active_runs']], [(current['run_id'], False)])
            history = runs.list_runs(self.request(root, include_history=True))
            self.assertEqual(history['active_runs'], normal['active_runs'])
            self.assertEqual([(r['run_id'], r['is_active'], r['superseded_by']) for r in history['history_runs']],
                             [(current['run_id'], True, None), (middle['run_id'], False, current['run_id']),
                              (old['run_id'], False, middle['run_id'])])
            self.assertEqual(self.snapshot(root), before)
            self.assertTrue(runs.check({'workspace': old['workspace'], 'workflow': 'country-finder'})['completed'])
            self.assertEqual(runs.list_runs(self.request(root))['active_runs'], normal['active_runs'])
            with self.assertRaises(Problem):
                self.start(root, person_id=old['person_id'], previous_run_id=old['run_id'])
            selected = self.start(root, command='salary-calculator', person_id=old['person_id'], profile_source_run=old['run_id'])
            self.assertEqual((Path(selected['workspace'])/'profile.md').read_bytes(), raw)

    def test_history_filters_and_missing_chat_preserve_files(self):
        with tempfile.TemporaryDirectory() as root:
            first = self.start(root)
            latest = self.start(root, person_id=first['person_id'], previous_run_id=first['run_id'])
            self.start(root, command='salary-calculator', person_id=first['person_id'])
            self.start(root, name='Fictional Person B', command='job-screener')
            self.start(root, chat='claude:another-chat')
            before = self.snapshot(root)
            history = runs.list_runs(self.request(root, person_id=first['person_id'], workflow='country-finder', include_history=True))
            self.assertEqual([r['run_id'] for r in history['history_runs']], [latest['run_id'], first['run_id']])
            self.assertEqual([r['run_id'] for r in history['active_runs']], [latest['run_id']])
            self.assertEqual(runs.list_runs(self.request(root, chat='codex:missing-chat', include_history=True))['history_runs'], [])
            for invalid in (None, 1, 'true'):
                with self.assertRaisesRegex(ValueError, 'include_history'):
                    runs.list_runs(self.request(root, include_history=invalid))
            self.assertEqual(self.snapshot(root), before)
        with tempfile.TemporaryDirectory() as root:
            self.assertEqual(runs.list_runs(self.request(root, include_history=True))['history_runs'], [])
            self.assertEqual(list(Path(root).iterdir()), [])

    def test_cross_command_reuses_only_same_person_confirmed_profiles(self):
        with tempfile.TemporaryDirectory() as root:
            cf = self.start(root)
            profile = b'Fictional Person A\r\n'
            situation = b'Fictional confirmed circumstances\r\n'
            (Path(cf['workspace'])/'profile.md').write_bytes(profile)
            (Path(cf['workspace'])/'situational-profile.md').write_bytes(situation)
            self.finish(cf)
            sc = self.start(root, command='salary-calculator', person_id=cf['person_id'], profile_source_run=cf['run_id'])
            self.assertEqual((Path(sc['workspace'])/'profile.md').read_bytes(), profile)
            self.assertEqual((Path(sc['workspace'])/'situational-profile.md').read_bytes(), situation)
            self.assertEqual(set(p.name for p in Path(sc['workspace']).iterdir()),
                             {'.compass-run.json','profile.md','situational-profile.md'})
            self.assertIsNone(sc['previous_run_id'])
            other = self.start(root, name='Fictional Person B')
            with self.assertRaises(ValueError):
                self.start(root, command='salary-calculator', name='Fictional Person B',
                           person_id=other['person_id'], profile_source_run=cf['run_id'])
            self.assertEqual(len(runs.list_runs(self.request(root, person_id=cf['person_id']))['active_runs']), 2)

    def test_missing_or_empty_profile_copy_preserves_source_and_creates_no_run(self):
        cases = ((None, None), (b'', None), (b' \t\r\n', None), (b'Fictional confirmed profile', b' \n'))
        for command in ('country-finder', 'salary-calculator', 'job-screener'):
            for profile, situation in cases:
                with self.subTest(command=command, profile=profile, situation=situation), tempfile.TemporaryDirectory() as root:
                    source = self.start(root)
                    path = Path(source['workspace'])
                    if profile is not None:(path/'profile.md').write_bytes(profile)
                    if situation is not None:(path/'situational-profile.md').write_bytes(situation)
                    before = self.snapshot(root)
                    folders = set(path.parent.iterdir())
                    baseline = {'previous_run_id': source['run_id']} if command == 'country-finder' else {}
                    with self.assertRaisesRegex(ValueError, 'Profile source'):
                        self.start(root, command=command, person_id=source['person_id'],
                                   profile_source_run=source['run_id'], **baseline)
                    self.assertEqual(self.snapshot(root), before)
                    self.assertEqual(set(path.parent.iterdir()), folders)

    def test_unfinished_resume_and_completed_view_are_read_only(self):
        with tempfile.TemporaryDirectory() as root:
            run = self.start(root)
            path = Path(run['workspace'])
            (path/'country-finder-01-criteria.md').write_text('Fictional criteria')
            (path/'.country-finder-state.json').write_text(json.dumps({'last_completed_step':1,'updated_at':'2026-10-29T12:00:00Z'}))
            before = self.snapshot(root)
            current = runs.list_runs(self.request(root))['active_runs'][0]
            self.assertEqual((current['status'],current['state']['last_completed_step']), ('in_progress',1))
            self.assertEqual(self.snapshot(root), before)
            self.finish(run)
            before = self.snapshot(root)
            self.assertTrue(runs.list_runs(self.request(root))['active_runs'][0]['completed'])
            self.assertEqual(self.snapshot(root), before)

    def test_corrupt_checkpoint_is_not_reported_complete_and_can_start_fresh(self):
        with tempfile.TemporaryDirectory() as root:
            old = self.start(root)
            (Path(old['workspace'])/'.country-finder-state.json').write_text('broken')
            record = runs.list_runs(self.request(root))['active_runs'][0]
            self.assertEqual(record['status'],'inconsistent')
            self.assertFalse(record['completed'])
            new = self.start(root, person_id=old['person_id'], previous_run_id=old['run_id'])
            self.assertNotEqual(old['workspace'], new['workspace'])
            self.assertEqual((Path(old['workspace'])/'.country-finder-state.json').read_text(),'broken')

    def test_rejects_foreign_person_ids_missing_metadata_and_symlink_roots(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as outside:
            run = self.start(root)
            with self.assertRaises(ValueError):self.start(root,'codex:another-chat',person_id=run['person_id'])
            metadata = Path(run['workspace'])/'.compass-run.json'
            original = metadata.read_bytes()
            metadata.write_bytes(original.replace(b'"schema_version": 1',b'"schema_version": 99'))
            with self.assertRaises(ValueError):runs.list_runs(self.request(root))
            metadata.write_bytes(original)
            if hasattr(os,'symlink'):
                with tempfile.TemporaryDirectory() as malicious:
                    (Path(malicious)/'Agent Compass').mkdir()
                    try:(Path(malicious)/'Agent Compass'/'runs').symlink_to(outside,target_is_directory=True)
                    except OSError:pass
                    else:
                        with self.assertRaises(ValueError):self.start(malicious)
                        self.assertEqual(list(Path(outside).iterdir()),[])

    def test_cli_and_relocated_package(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as install:
            install = Path(install)
            for component in ('helpers','data'):
                shutil.copytree(ROOT/component,install/component)
            def invoke(command, payload):
                result = subprocess.run([sys.executable,'-I','-B',str(install/'helpers/compass.py'),command],
                                        input=json.dumps({'schema_version':1,**payload}),text=True,capture_output=True,
                                        env={**os.environ, 'HOME': root, 'USERPROFILE': root})
                self.assertEqual(result.returncode,0,result.stderr)
                return json.loads(result.stdout)['result']
            expected = str(Path(root).resolve()/'Agent Compass')
            self.assertEqual(invoke('workspace-base',{}), {'workspace': expected, 'exists': False})
            self.assertEqual(invoke('workspace-base',{'create': True}), {'workspace': expected, 'exists': True})
            self.assertEqual(list(Path(expected).iterdir()), [])
            run = invoke('run-start',self.request(root,'claude:fictional-session',workflow='salary-calculator',person_label='Fictional Person A'))
            self.assertEqual(invoke('run-list',self.request(root,'claude:fictional-session'))['active_runs'][0]['run_id'],run['run_id'])
            self.assertEqual(invoke('run-list',self.request(root,'claude:other-session'))['active_runs'],[])
            js = invoke('run-start', self.request(root, 'claude:fictional-session', workflow='job-screener',
                                               person_label='Fictional Person A', person_id=run['person_id']))
            active = invoke('run-list', self.request(root, 'claude:fictional-session', workflow='job-screener'))['active_runs']
            self.assertEqual((active[0]['run_id'], active[0]['status']), (js['run_id'], 'profile_missing'))
            historical = invoke('run-list', self.request(root, 'claude:fictional-session', workflow='job-screener', include_history=True))
            self.assertEqual([(r['run_id'], r['is_active']) for r in historical['history_runs']], [(js['run_id'], True)])
            self.assertFalse(list(install.rglob('__pycache__')))

    def test_fixed_base_resolution_creation_and_override_rejection(self):
        with tempfile.TemporaryDirectory() as home, tempfile.TemporaryDirectory() as other:
            self.home.return_value = Path(home)
            expected = Path(home).resolve()/'Agent Compass'
            self.assertEqual(workspaces.resolve({}), {'workspace': str(expected), 'exists': False})
            self.assertEqual(runs.list_runs(self.request(home))['active_runs'], [])
            self.assertFalse(expected.exists())
            for payload in ({'workspace': other}, {'create': 'true'}):
                with self.assertRaises(ValueError):workspaces.resolve(payload)
            payload = self.request(home, workflow='country-finder', person_label='Fictional Person')
            with self.assertRaisesRegex(ValueError, 'fixed'):
                runs.start({**payload, 'workspace': other})
            self.assertFalse(expected.exists())
            self.assertEqual(list(Path(other).iterdir()), [])
            self.assertEqual(workspaces.resolve({'create': True}), {'workspace': str(expected), 'exists': True})
            self.assertEqual(list(expected.iterdir()), [])
            expected.rmdir()
            expected.write_text('Fictional existing user file')
            with self.assertRaisesRegex(ValueError, 'occupied'):workspaces.resolve({'create': True})
            self.assertEqual(expected.read_text(), 'Fictional existing user file')

    def test_job_screener_new_chat_and_person_do_not_reuse_profiles(self):
        with tempfile.TemporaryDirectory() as home:
            self.request(home)
            base = Path(workspaces.resolve({'create': True})['workspace'])
            (base/'profile.md').write_text('Fictional legacy root profile')
            first = self.start(home, command='job-screener')
            self.assertEqual(set(p.name for p in Path(first['workspace']).iterdir()), {'.compass-run.json'})
            initial = runs.list_runs(self.request(home))['active_runs'][0]
            self.assertEqual((initial['status'], initial['completed']), ('profile_missing', False))
            (Path(first['workspace'])/'profile.md').write_text('Fictional confirmed Person A')
            before = self.snapshot(home)
            self.assertEqual(runs.list_runs(self.request(home, 'claude:different-chat'))['active_runs'], [])
            self.assertEqual(self.snapshot(home), before)
            other_chat = self.start(home, 'claude:different-chat', command='job-screener')
            spouse = self.start(home, command='job-screener', name='Fictional Person B')
            for run in (other_chat, spouse):
                self.assertNotEqual(run['person_id'], first['person_id'])
                self.assertFalse((Path(run['workspace'])/'profile.md').exists())
            for name, raw in before.items():self.assertEqual((Path(home)/name).read_bytes(), raw)

    def test_job_screener_continue_and_fresh_preserve_profiles_without_checkpoints(self):
        with tempfile.TemporaryDirectory() as home:
            old = self.start(home, command='job-screener')
            path = Path(old['workspace'])
            (path/'profile.md').write_text('Fictional confirmed profile')
            before = self.snapshot(home)
            current = runs.list_runs(self.request(home, workflow='job-screener'))['active_runs'][0]
            self.assertEqual((current['run_id'], current['status'], current['completed']),
                             (old['run_id'], 'ready', False))
            self.assertIsNone(current['state'])
            self.assertEqual(self.snapshot(home), before)
            with self.assertRaises(Problem):
                self.start(home, command='job-screener', person_id=old['person_id'])
            new = self.start(home, command='job-screener', person_id=old['person_id'], previous_run_id=old['run_id'])
            active = runs.list_runs(self.request(home, workflow='job-screener'))['active_runs'][0]
            self.assertEqual((active['run_id'], active['status']), (new['run_id'], 'profile_missing'))
            for name, raw in before.items():self.assertEqual((Path(home)/name).read_bytes(), raw)
            self.assertEqual(set(p.name for p in path.iterdir()), {'.compass-run.json', 'profile.md'})
            with self.assertRaises(ValueError):runs.check({'workspace': str(path), 'workflow': 'job-screener'})

    def test_job_screener_same_person_profile_transfer_keeps_command_baselines_separate(self):
        with tempfile.TemporaryDirectory() as home:
            cf = self.start(home)
            raw = b'Fictional confirmed same-person profile\r\n'
            (Path(cf['workspace'])/'profile.md').write_bytes(raw)
            self.finish(cf)
            js = self.start(home, command='job-screener', person_id=cf['person_id'], profile_source_run=cf['run_id'])
            self.assertEqual((Path(js['workspace'])/'profile.md').read_bytes(), raw)
            self.assertEqual(set(p.name for p in Path(js['workspace']).iterdir()), {'.compass-run.json', 'profile.md'})
            active = {r['workflow']: r for r in runs.list_runs(self.request(home, person_id=cf['person_id']))['active_runs']}
            self.assertEqual(active['country-finder']['run_id'], cf['run_id'])
            self.assertTrue(active['country-finder']['completed'])
            self.assertEqual(active['job-screener']['status'], 'ready')
            spouse = self.start(home, name='Fictional Person B')
            with self.assertRaises(ValueError):
                self.start(home, command='job-screener', name='Fictional Person B', person_id=spouse['person_id'],
                           profile_source_run=cf['run_id'])
            with self.assertRaises(ValueError):self.start(home, command='portal-finder')

    def test_missing_final_and_same_name_people_are_not_reused(self):
        with tempfile.TemporaryDirectory() as root:
            first = self.start(root, chat='local:19a1df27-8a5d-4ad8-97cc-504094005c61')
            self.finish(first)
            (Path(first['workspace'])/'country-finder-06-final-results.md').unlink()
            second = self.start(root, chat='local:19a1df27-8a5d-4ad8-97cc-504094005c61')
            self.assertNotEqual(first['person_id'], second['person_id'])
            current = runs.list_runs(self.request(root, 'local:19a1df27-8a5d-4ad8-97cc-504094005c61'))['active_runs']
            statuses = {r['run_id']: r for r in current}
            self.assertEqual(statuses[first['run_id']]['status'], 'inconsistent')
            self.assertFalse(statuses[first['run_id']]['completed'])
            self.assertEqual(runs.list_runs(self.request(root, 'local:efcfaf7e-3dca-4166-85a7-a118c965596a'))['active_runs'], [])

    def test_chat_tokens_reject_placeholders_and_malformed_local_ids(self):
        with tempfile.TemporaryDirectory() as root:
            for chat in ('chat-a', 'local:example', 'local:00000000-0000-0000-0000-000000000000',
                         'claude:${CLAUDE_SESSION_ID}', 'codex:two words', 'unknown:session', 'claude:'):
                with self.subTest(chat=chat), self.assertRaises(ValueError):
                    self.start(root, chat=chat)
                self.assertEqual(list(Path(root).iterdir()), [])
            chat = 'local:' + str(uuid.uuid4())
            run = self.start(root, chat=chat)
            self.assertEqual(runs.list_runs(self.request(root, chat))['active_runs'][0]['run_id'], run['run_id'])

    def test_os_metadata_does_not_block_or_modify_saved_runs(self):
        for name in ('.DS_Store', 'desktop.ini', 'Thumbs.db', 'DESKTOP.INI'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as root:
                first = self.start(root)
                self.finish(first)
                metadata = Path(first['workspace']).parent/name
                metadata.write_bytes(b'Fictional OS metadata')
                before = self.snapshot(root)
                self.assertTrue(runs.list_runs(self.request(root))['active_runs'][0]['completed'])
                self.assertEqual(self.snapshot(root), before)
                self.start(root, person_id=first['person_id'], previous_run_id=first['run_id'])
                for old, raw in before.items():self.assertEqual((Path(root)/old).read_bytes(), raw)
                metadata.unlink()
                metadata.mkdir()
                with self.assertRaisesRegex(ValueError, 'Unsafe OS metadata'):runs.list_runs(self.request(root))

    def test_os_metadata_exception_does_not_allow_symlinks_or_unknown_files(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as outside:
            run = self.start(root)
            folder = Path(run['workspace']).parent
            unexpected = folder/'notes.txt'
            unexpected.write_text('Fictional user file')
            with self.assertRaisesRegex(ValueError, 'Unexpected occupant'):runs.list_runs(self.request(root))
            self.assertEqual(unexpected.read_text(), 'Fictional user file')
            unexpected.unlink()
            target = Path(outside)/'private.txt'
            target.write_text('Fictional unrelated private content')
            for name in ('.DS_Store', 'desktop.ini', 'Thumbs.db'):
                link = folder/name
                try:link.symlink_to(target)
                except OSError:self.skipTest('Symlinks unavailable')
                with self.assertRaisesRegex(ValueError, 'Unsafe OS metadata'):runs.list_runs(self.request(root))
                self.assertEqual(target.read_text(), 'Fictional unrelated private content')
                link.unlink()

    def test_forked_baselines_and_cycles_require_reconciliation(self):
        with tempfile.TemporaryDirectory() as root:
            old = self.start(root)
            new = self.start(root, person_id=old['person_id'], previous_run_id=old['run_id'])
            source = Path(new['workspace'])
            fork_id = 'f' * 32
            fork = source.parent / ('run-' + fork_id)
            fork.mkdir()
            record = json.loads((source/'.compass-run.json').read_text())
            record['run_id'] = fork_id
            (fork/'.compass-run.json').write_text(json.dumps(record))
            before = self.snapshot(root)
            with self.assertRaises(Problem):runs.list_runs(self.request(root))
            with self.assertRaises(Problem):runs.list_runs(self.request(root, include_history=True))
            with self.assertRaises(Problem):
                self.start(root, person_id=old['person_id'], previous_run_id=new['run_id'])
            self.assertEqual(self.snapshot(root), before)
            record['previous_run_id'] = fork_id
            (fork/'.compass-run.json').write_text(json.dumps(record))
            with self.assertRaisesRegex(ValueError, 'cycle'):runs.list_runs(self.request(root))

    def test_person_labels_are_validated_and_not_reassigned(self):
        for name in ('', ' Fictional Person', 'Fictional Person ', 'A'*201, 'Fictional\nPerson', 5, None):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as root:
                with self.assertRaisesRegex(ValueError, 'person label'):
                    self.start(root, name=name)
                self.assertEqual(list(Path(root).iterdir()), [])
        with tempfile.TemporaryDirectory() as root:
            run = self.start(root)
            before = self.snapshot(root)
            with self.assertRaisesRegex(ValueError, 'Person label differs'):
                self.start(root, name='Fictional Person B', person_id=run['person_id'], previous_run_id=run['run_id'])
            self.assertEqual(self.snapshot(root), before)

    def test_tampered_run_metadata_is_rejected_without_writes(self):
        def tamper(run, **changes):
            path = Path(run['workspace'])/'.compass-run.json'
            path.write_text(json.dumps({**json.loads(path.read_text()), **changes}))
        # Each case receives a country-finder run for person A and returns the changes for another saved run.
        cases = (
            ('Run identity mismatch', lambda run: ('salary-calculator', {}, dict(chat_key='0'*64))),
            ('Run identity mismatch', lambda run: ('salary-calculator', {}, dict(run_id='e'*32))),
            ('Run time needs a timezone', lambda run: ('salary-calculator', {}, dict(created_at='2026-10-29T12:00:00'))),
            ('Referenced run is missing', lambda run: ('salary-calculator', {}, dict(previous_run_id='a'*32))),
            ('Cross-person run reference', lambda run: ('country-finder', dict(name='Fictional Person B'), dict(profile_source_run=run['run_id']))),
            ('Cross-command baseline reference', lambda run: ('salary-calculator', {}, dict(previous_run_id=run['run_id']))))
        for index, (message, build) in enumerate(cases):
            with self.subTest(index=index, message=message), tempfile.TemporaryDirectory() as root:
                run = self.start(root)
                command, extra, changes = build(run)
                other = self.start(root, command=command, **({'person_id': run['person_id']} if not extra else extra))
                tamper(other, **changes)
                before = self.snapshot(root)
                with self.assertRaisesRegex(ValueError, message):
                    runs.list_runs(self.request(root))
                with self.assertRaisesRegex(ValueError, message):
                    self.start(root, person_id=run['person_id'], previous_run_id=run['run_id'])
                self.assertEqual(self.snapshot(root), before)

    def test_interrupted_run_staging_folder_is_ignored(self):
        with tempfile.TemporaryDirectory() as root:
            run = self.start(root)
            leftover = Path(run['workspace']).parent/'.creating-abandoned'/'run'
            leftover.mkdir(parents=True)
            (leftover/'profile.md').write_text('Fictional partial profile')
            before = self.snapshot(root)
            self.assertEqual([r['run_id'] for r in runs.list_runs(self.request(root))['active_runs']], [run['run_id']])
            self.assertEqual(self.snapshot(root), before)
            fresh = self.start(root, person_id=run['person_id'], previous_run_id=run['run_id'])
            self.assertNotEqual(fresh['workspace'], run['workspace'])
            self.assertEqual((leftover/'profile.md').read_text(), 'Fictional partial profile')

    def test_profile_symlink_is_not_copied(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as outside:
            first = self.start(root)
            target = Path(outside)/'profile.md'
            target.write_text('Fictional unrelated private profile')
            try:(Path(first['workspace'])/'profile.md').symlink_to(target)
            except OSError:self.skipTest('Symlinks unavailable')
            before = self.snapshot(root)
            with self.assertRaises(ValueError):
                self.start(root, command='salary-calculator', person_id=first['person_id'],
                           profile_source_run=first['run_id'])
            self.assertEqual(self.snapshot(root), before)
            self.assertEqual(target.read_text(), 'Fictional unrelated private profile')


if __name__ == "__main__":
    unittest.main()
