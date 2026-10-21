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
            self.assertFalse(list(install.rglob("__pycache__")))


if __name__ == "__main__":
    unittest.main()
