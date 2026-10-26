import json

import pytest

from cag.audit_config import audit
from cag.fleet import COMMANDS, SECRET_SNIPPETS, fleet
from cag.gate import Gate
from cag.policy import command_decision, load, path_blocked
from cag.secrets import entropy, scan

P = load()
GOOD = {"dev": "d", "team": "platform", "client": "cli-agent", "base_url": P["gateway_base_url"], "model": "code-small",
        "mcp_servers": ["repo-search"], "auto_approve": False, "personal_api_key": False, "telemetry_off": False}

def test_policy_is_valid_json_with_required_keys():
    assert {"gateway_base_url", "approved_clients", "command_deny", "blocked_context_globs"} <= set(P)

def test_good_config_compliant():
    assert audit(P, GOOD) == []

@pytest.mark.parametrize("change,violation", [
    ({"base_url": "https://api.public-llm.example/v1"}, "bypasses_gateway"),
    ({"personal_api_key": True}, "personal_api_key"),
    ({"mcp_servers": ["shady-mcp"]}, "unapproved_mcp_server"),
    ({"auto_approve": True}, "auto_approve_enabled"),
    ({"client": "unvetted-desktop-app"}, "unapproved_client"),
    ({"team": "contractors", "model": "code-large"}, "model_not_allowed_for_team"),
    ({"telemetry_off": True}, "audit_logging_disabled"),
])
def test_each_violation(change, violation):
    assert violation in audit(P, {**GOOD, **change})

@pytest.mark.parametrize("path", [".env", "deploy/prod.pem", "keys/id_rsa", "infra/terraform.tfstate", "secrets/db.txt"])
def test_blocked_paths(path):
    assert path_blocked(P, path)

@pytest.mark.parametrize("path", ["src/app.py", "README.md", "env.py"])
def test_allowed_paths(path):
    assert not path_blocked(P, path)

@pytest.mark.parametrize("cmd,want", COMMANDS)
def test_command_policy(cmd, want):
    assert command_decision(P, cmd) == want

def test_command_whitespace_normalised():
    assert command_decision(P, "rm   -rf   /") == "deny"

@pytest.mark.parametrize("text,label", [s for s in SECRET_SNIPPETS if s[0] not in ("password: 'Summer2026Summer2026'", "secret_name = 'payments-db-credentials-prod'")])
def test_secret_scanner(text, label):
    assert bool(scan(text)) == bool(label)

def test_known_miss_low_entropy_password():
    """Known failure kept visible: a human-chosen low-entropy password is not detected."""
    assert scan("password: 'Summer2026Summer2026'") == []

def test_known_false_positive_secret_name():
    assert scan("secret_name = 'payments-db-credentials-prod'") == ["high_entropy_assignment"]

def test_entropy():
    assert entropy("aaaa") == 0 and entropy("abcd") == 2

def test_gate_drops_env_and_allows():
    g = Gate(P); r = g.request("d", "platform", "ide-assistant", "code-large", {"a.py": "x", ".env": "K=1"}, 10)
    assert r["decision"] == "allow" and r["files_dropped"] == [".env"]

def test_gate_denies_secret():
    g = Gate(P); r = g.request("d", "platform", "cli-agent", "code-small", {"c.py": SECRET_SNIPPETS[0][0]}, 10)
    assert r["decision"] == "deny" and "aws_access_key_id" in r["secret_findings"]["c.py"]

def test_gate_budget():
    g = Gate(P)
    assert g.request("d", "contractors", "cli-agent", "code-small", {}, 299_000)["decision"] == "allow"
    assert "budget_exceeded" in g.request("d", "contractors", "cli-agent", "code-small", {}, 5_000)["reasons"]

def test_gate_model_and_client():
    r = Gate(P).request("d", "contractors", "unvetted-desktop-app", "code-large", {}, 1)
    assert set(r["reasons"]) == {"unapproved_client", "model_not_allowed"}

def test_gate_log_serialisable():
    g = Gate(P); g.request("d", "platform", "cli-agent", "code-small", {}, 1); g.command("d", "ls")
    assert len(json.loads(json.dumps(g.log))) == 2

def test_fleet_deterministic_and_sized():
    assert fleet() == fleet() and len(fleet()) == 40
