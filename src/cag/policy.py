"""Load the org policy for coding assistants and desktop AI apps (fictional org: Quillstone Labs)."""
import fnmatch
import json
import pathlib

DEFAULT = pathlib.Path(__file__).resolve().parents[2] / "policies" / "policy.json"

def load(path=DEFAULT) -> dict:
    return json.loads(pathlib.Path(path).read_text())

def path_blocked(policy: dict, path: str) -> bool:
    name = path.split("/")[-1]
    return any(fnmatch.fnmatch(name, g) or fnmatch.fnmatch(path, g) or fnmatch.fnmatch(path, "*/" + g) for g in policy["blocked_context_globs"])

def command_decision(policy: dict, cmd: str) -> str:
    c = " ".join(cmd.split())
    if any(fnmatch.fnmatch(c, p) for p in policy["command_deny"]):
        return "deny"
    if any(fnmatch.fnmatch(c, p) for p in policy["command_needs_approval"]):
        return "needs_approval"
    return "allow"
