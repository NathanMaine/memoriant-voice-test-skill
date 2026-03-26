"""Tests for src.runner.loader -- YAML and JSON test set loading."""

import json
import textwrap

import pytest
import yaml

from src.runner.loader import LoaderError, load_test_set


@pytest.fixture()
def yaml_file(tmp_path):
    """Write a minimal valid YAML test set and return its path."""
    data = {
        "test_set_id": "demo",
        "expected_label": "greeting",
        "utterances": [
            {"id": "u1", "text": "Hello there"},
            {"id": "u2", "text": "Hey"},
        ],
    }
    path = tmp_path / "demo.yaml"
    path.write_text(yaml.dump(data), encoding="utf-8")
    return path


@pytest.fixture()
def json_file(tmp_path):
    """Write a minimal valid JSON test set and return its path."""
    data = {
        "test_set_id": "demo-json",
        "expected_label": "greeting",
        "description": "JSON fixture",
        "utterances": [
            {"id": "u1", "text": "Hello"},
        ],
    }
    path = tmp_path / "demo.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


class TestLoadYAML:
    def test_loads_valid_yaml(self, yaml_file):
        ts = load_test_set(yaml_file)
        assert ts.test_set_id == "demo"
        assert ts.expected_label == "greeting"
        assert len(ts.utterances) == 2
        assert ts.utterances[0].id == "u1"
        assert ts.utterances[0].text == "Hello there"

    def test_loads_valid_yml_extension(self, tmp_path):
        data = {
            "test_set_id": "yml-test",
            "expected_label": "x",
            "utterances": [{"id": "u1", "text": "hi"}],
        }
        path = tmp_path / "test.yml"
        path.write_text(yaml.dump(data), encoding="utf-8")
        ts = load_test_set(path)
        assert ts.test_set_id == "yml-test"


class TestLoadJSON:
    def test_loads_valid_json(self, json_file):
        ts = load_test_set(json_file)
        assert ts.test_set_id == "demo-json"
        assert ts.description == "JSON fixture"
        assert len(ts.utterances) == 1


class TestLoaderErrors:
    def test_missing_file(self, tmp_path):
        with pytest.raises(LoaderError, match="not found"):
            load_test_set(tmp_path / "nope.yaml")

    def test_unsupported_extension(self, tmp_path):
        path = tmp_path / "data.txt"
        path.write_text("hello")
        with pytest.raises(LoaderError, match="Unsupported file format"):
            load_test_set(path)

    def test_missing_required_fields(self, tmp_path):
        path = tmp_path / "bad.yaml"
        path.write_text(yaml.dump({"test_set_id": "x"}))
        with pytest.raises(LoaderError, match="Missing required fields"):
            load_test_set(path)

    def test_empty_utterances(self, tmp_path):
        data = {
            "test_set_id": "x",
            "expected_label": "y",
            "utterances": [],
        }
        path = tmp_path / "empty.yaml"
        path.write_text(yaml.dump(data))
        with pytest.raises(LoaderError, match="non-empty list"):
            load_test_set(path)

    def test_utterance_missing_id(self, tmp_path):
        data = {
            "test_set_id": "x",
            "expected_label": "y",
            "utterances": [{"text": "no id here"}],
        }
        path = tmp_path / "noid.yaml"
        path.write_text(yaml.dump(data))
        with pytest.raises(LoaderError, match="missing 'id' or 'text'"):
            load_test_set(path)

    def test_invalid_yaml_syntax(self, tmp_path):
        path = tmp_path / "broken.yaml"
        path.write_text(":\n  - :\n    bad: [")
        with pytest.raises(LoaderError, match="Failed to parse YAML"):
            load_test_set(path)

    def test_invalid_json_syntax(self, tmp_path):
        path = tmp_path / "broken.json"
        path.write_text("{not json!}")
        with pytest.raises(LoaderError, match="Failed to parse JSON"):
            load_test_set(path)

    def test_non_dict_top_level_yaml(self, tmp_path):
        path = tmp_path / "list.yaml"
        path.write_text("- one\n- two\n")
        with pytest.raises(LoaderError, match="Expected a mapping"):
            load_test_set(path)

    def test_non_dict_top_level_json(self, tmp_path):
        path = tmp_path / "list.json"
        path.write_text('["a","b"]')
        with pytest.raises(LoaderError, match="Expected a mapping"):
            load_test_set(path)

    def test_directory_not_file(self, tmp_path):
        with pytest.raises(LoaderError, match="not a file"):
            load_test_set(tmp_path)
