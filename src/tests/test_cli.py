"""Tests for src.cli.main -- CLI integration tests."""

import json
import os

import pytest
from click.testing import CliRunner

from src.cli.main import cli


@pytest.fixture()
def runner():
    return CliRunner(mix_stderr=False)


@pytest.fixture()
def yaml_fixture():
    """Return path to the balance_inquiry YAML fixture."""
    path = os.path.join(os.path.dirname(__file__), "..", "fixtures", "balance_inquiry.yaml")
    return os.path.abspath(path)


@pytest.fixture()
def json_fixture():
    """Return path to the balance_inquiry JSON fixture."""
    path = os.path.join(os.path.dirname(__file__), "..", "fixtures", "balance_inquiry.json")
    return os.path.abspath(path)


class TestCLIRun:
    def test_run_text_format(self, runner, yaml_fixture, tmp_path):
        log_path = str(tmp_path / "evidence.jsonl")
        result = runner.invoke(
            cli,
            ["run", "--test-set", yaml_fixture, "--format", "text", "--log", log_path],
        )
        assert result.exit_code == 0
        assert "Robustness Report" in result.output
        assert "Pass rate" in result.output

    def test_run_json_format(self, runner, yaml_fixture, tmp_path):
        log_path = str(tmp_path / "evidence.jsonl")
        result = runner.invoke(
            cli,
            ["run", "--test-set", yaml_fixture, "--format", "json", "--log", log_path],
        )
        assert result.exit_code == 0
        parsed = json.loads(result.output)
        assert parsed["test_set_id"] == "balance-inquiry"
        assert "summary" in parsed
        assert "results" in parsed

    def test_run_json_fixture(self, runner, json_fixture, tmp_path):
        log_path = str(tmp_path / "evidence.jsonl")
        result = runner.invoke(
            cli,
            ["run", "--test-set", json_fixture, "--format", "json", "--log", log_path],
        )
        assert result.exit_code == 0
        parsed = json.loads(result.output)
        assert parsed["test_set_id"] == "balance-inquiry-json"

    def test_evidence_log_created(self, runner, yaml_fixture, tmp_path):
        log_path = tmp_path / "evidence.jsonl"
        runner.invoke(
            cli,
            ["run", "--test-set", yaml_fixture, "--log", str(log_path)],
        )
        assert log_path.exists()
        lines = log_path.read_text().strip().split("\n")
        assert len(lines) == 1
        record = json.loads(lines[0])
        assert record["test_set_id"] == "balance-inquiry"

    def test_note_recorded(self, runner, yaml_fixture, tmp_path):
        log_path = tmp_path / "evidence.jsonl"
        runner.invoke(
            cli,
            [
                "run",
                "--test-set", yaml_fixture,
                "--log", str(log_path),
                "--note", "experiment-1",
            ],
        )
        record = json.loads(log_path.read_text().strip())
        assert record["note"] == "experiment-1"

    def test_classifier_llm_option(self, runner, yaml_fixture, tmp_path):
        log_path = str(tmp_path / "evidence.jsonl")
        result = runner.invoke(
            cli,
            [
                "run",
                "--test-set", yaml_fixture,
                "--classifier", "llm",
                "--format", "json",
                "--log", log_path,
            ],
        )
        assert result.exit_code == 0
        parsed = json.loads(result.output)
        # LLM adapter returns ambiguous for everything without a key
        for r in parsed["results"]:
            assert r["outcome"] == "ambiguous"

    def test_missing_test_set(self, runner, tmp_path):
        result = runner.invoke(
            cli,
            ["run", "--test-set", str(tmp_path / "nope.yaml")],
        )
        assert result.exit_code != 0

    def test_verbose_flag(self, runner, yaml_fixture, tmp_path):
        log_path = str(tmp_path / "evidence.jsonl")
        result = runner.invoke(
            cli,
            ["-v", "run", "--test-set", yaml_fixture, "--log", log_path],
        )
        assert result.exit_code == 0
