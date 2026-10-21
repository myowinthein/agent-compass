"""Offline consumer CLI checks. Fixtures are fictional and use temporary workspaces."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "helpers"))
from compass_lib import research, timezones
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
        for amount, expected in (("1000", "pass"), ("1500", "uncertain"), ("2000", "uncertain"), ("2000.00001", "fail")):
            with self.subTest(amount=amount):
                payload = self.comparison()
                payload["minimum"]["amount"] = amount
                result = self.invoke("compare", payload)["result"]
                self.assertEqual(result["outcome"], expected)
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
            self.assertEqual(self.invoke("compare", payload)["result"]["outcome"], "unverified")
        payload = self.comparison()
        payload["minimum"]["basis"] = "net"
        self.assertEqual(self.invoke("compare", payload)["result"]["outcome"], "unverified")
        payload["minimum"]["currency"] = "USD"
        self.assertFalse(self.invoke("compare", payload)["result"]["hard_floor_failed"])

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
            self.assertEqual([p.name for p in consumer.iterdir()], ["cf-step6-final-ranking.md"])
            self.assertFalse(list(install.rglob("__pycache__")))


if __name__ == "__main__":
    unittest.main()
