"""Tests for Socratic OpenClaw Skill."""

import pytest


def test_import_skill():
    """Test that skill can be imported."""
    from socratic_openclaw_skill.skill import SocraticDiscoverySkill

    assert SocraticDiscoverySkill is not None


def test_import_config():
    """Test that config can be imported."""
    from socratic_openclaw_skill.config import SocraticOpenclawConfig

    assert SocraticOpenclawConfig is not None


def test_config_defaults():
    """Test that config has proper defaults."""
    from socratic_openclaw_skill.config import SocraticOpenclawConfig

    config = SocraticOpenclawConfig()
    assert config.model == "claude-opus-4-5"
    assert config.temperature == 0.7
    assert config.max_questions == 8
    assert config.min_responses == 3
