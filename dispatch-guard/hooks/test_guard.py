"""
Tests for dispatch-guard v0.2.0 guard.py validation logic.

Run: python3 -m pytest hooks/test_guard.py -v
(from the dispatch-guard repo root)
"""

import importlib.util
import os
import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Import guard module without executing main()
# ---------------------------------------------------------------------------

_guard_path = Path(__file__).parent / "guard.py"
_spec = importlib.util.spec_from_file_location("guard", _guard_path)
_guard = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(_guard)  # type: ignore[union-attr]

validate = _guard.validate


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _dispatch(subagent_type: str, model: str) -> dict:
    return validate({"subagent_type": subagent_type, "model": model})


def _is_block(result: dict) -> bool:
    return (
        result.get("hookSpecificOutput", {}).get("permissionDecision") == "deny"
    )


def _is_warn(result: dict) -> bool:
    return (
        "systemMessage" in result
        and "[dispatch-guard] WARN" in result["systemMessage"]
        and not _is_block(result)
    )


def _is_pass(result: dict) -> bool:
    return result == {}


# ---------------------------------------------------------------------------
# (a) Missing model
# ---------------------------------------------------------------------------

class TestMissingModel:
    def test_empty_model_is_blocked(self) -> None:
        result = validate({"subagent_type": "nova", "model": ""})
        assert _is_block(result)

    def test_absent_model_is_blocked(self) -> None:
        result = validate({"subagent_type": "nova"})
        assert _is_block(result)


# ---------------------------------------------------------------------------
# (b) Invalid model
# ---------------------------------------------------------------------------

class TestInvalidModel:
    def test_best_alias_is_blocked(self) -> None:
        result = _dispatch("nova", "best")
        assert _is_block(result)

    def test_gpt4_is_blocked(self) -> None:
        result = _dispatch("nova", "gpt-4")
        assert _is_block(result)


# ---------------------------------------------------------------------------
# (d) Sentinel + fable unconditional block
# ---------------------------------------------------------------------------

class TestSentinelFable:
    def test_sentinel_fable_is_blocked(self) -> None:
        result = _dispatch("sentinel", "fable")
        assert _is_block(result)
        assert "unconditionally blocked" in result["systemMessage"]

    def test_sentinel_opus_is_allowed(self) -> None:
        result = _dispatch("sentinel", "opus")
        assert _is_pass(result)

    def test_sentinel_sonnet_is_blocked(self) -> None:
        # sentinel is in HARD_OPUS_FLOOR
        result = _dispatch("sentinel", "sonnet")
        assert _is_block(result)

    def test_sentinel_fable_blocked_even_with_env_override(self, monkeypatch) -> None:
        monkeypatch.setenv("DISPATCH_GUARD_ALLOW_DOWNGRADE", "1")
        result = _dispatch("sentinel", "fable")
        # (d) fires before (c), so still blocked regardless of env
        assert _is_block(result)


# ---------------------------------------------------------------------------
# (c-hard) Hard-floor agents: atlas, sentinel, orchestrator
# ---------------------------------------------------------------------------

class TestHardFloor:
    def test_atlas_sonnet_blocked(self) -> None:
        result = _dispatch("atlas", "sonnet")
        assert _is_block(result)
        assert "hard-floor" in result["systemMessage"]

    def test_atlas_haiku_blocked(self) -> None:
        result = _dispatch("atlas", "haiku")
        assert _is_block(result)

    def test_atlas_opus_allowed(self) -> None:
        result = _dispatch("atlas", "opus")
        assert _is_pass(result)

    def test_atlas_fable_allowed(self) -> None:
        # Atlas may run at fable — "Atlas any task" is a Fable trigger
        result = _dispatch("atlas", "fable")
        assert _is_pass(result)

    def test_atlas_sonnet_blocked_even_with_env_override_off(self) -> None:
        # confirm default (no env var) still blocks
        result = _dispatch("atlas", "sonnet")
        assert _is_block(result)

    def test_atlas_sonnet_warn_allowed_with_env_override(self, monkeypatch) -> None:
        monkeypatch.setenv("DISPATCH_GUARD_ALLOW_DOWNGRADE", "1")
        result = _dispatch("atlas", "sonnet")
        assert _is_warn(result)
        assert "DISPATCH_GUARD_ALLOW_DOWNGRADE=1" in result["systemMessage"]

    def test_orchestrator_sonnet_blocked(self) -> None:
        result = _dispatch("orchestrator", "sonnet")
        assert _is_block(result)

    def test_orchestrator_opus_allowed(self) -> None:
        result = _dispatch("orchestrator", "opus")
        assert _is_pass(result)


# ---------------------------------------------------------------------------
# (c-soft) Soft-floor agents: cipher, scout, oracle
# ---------------------------------------------------------------------------

class TestSoftFloor:
    def test_scout_sonnet_allowed_with_advisory(self) -> None:
        result = _dispatch("scout", "sonnet")
        assert _is_warn(result)
        assert "sonnet" in result["systemMessage"]
        assert "Sonnet-OK" in result["systemMessage"]

    def test_scout_haiku_blocked(self) -> None:
        result = _dispatch("scout", "haiku")
        assert _is_block(result)
        assert "soft-floor" in result["systemMessage"]

    def test_scout_opus_allowed(self) -> None:
        result = _dispatch("scout", "opus")
        assert _is_pass(result)

    def test_scout_fable_allowed(self) -> None:
        result = _dispatch("scout", "fable")
        assert _is_pass(result)

    def test_cipher_sonnet_allowed_with_advisory(self) -> None:
        result = _dispatch("cipher", "sonnet")
        assert _is_warn(result)

    def test_cipher_haiku_blocked(self) -> None:
        result = _dispatch("cipher", "haiku")
        assert _is_block(result)

    def test_cipher_opus_allowed(self) -> None:
        result = _dispatch("cipher", "opus")
        assert _is_pass(result)

    def test_oracle_sonnet_allowed_with_advisory(self) -> None:
        result = _dispatch("oracle", "sonnet")
        assert _is_warn(result)

    def test_oracle_haiku_blocked(self) -> None:
        result = _dispatch("oracle", "haiku")
        assert _is_block(result)

    def test_oracle_opus_allowed(self) -> None:
        result = _dispatch("oracle", "opus")
        assert _is_pass(result)


# ---------------------------------------------------------------------------
# Happy-path: ordinary agents at any valid model
# ---------------------------------------------------------------------------

class TestOrdinaryAgents:
    def test_nova_sonnet_allowed(self) -> None:
        assert _is_pass(_dispatch("nova", "sonnet"))

    def test_viper_haiku_allowed(self) -> None:
        assert _is_pass(_dispatch("viper", "haiku"))

    def test_lana_opus_allowed(self) -> None:
        assert _is_pass(_dispatch("lana", "opus"))

    def test_forge_fable_allowed(self) -> None:
        assert _is_pass(_dispatch("forge", "fable"))
