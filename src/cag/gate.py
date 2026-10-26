"""Gateway-side gate for coding-assistant requests: client, model, budget, context files, secrets, commands."""
from collections import defaultdict

from .policy import command_decision, path_blocked
from .secrets import scan


class Gate:
    def __init__(self, policy: dict):
        self.p = policy
        self.used = defaultdict(int)
        self.log: list[dict] = []

    def request(self, dev: str, team: str, client: str, model: str, files: dict[str, str], tokens: int) -> dict:
        reasons = []
        if client not in self.p["approved_clients"]:
            reasons.append("unapproved_client")
        if model not in self.p["team_models"].get(team, []):
            reasons.append("model_not_allowed")
        if self.used[team] + tokens > self.p["monthly_tokens"].get(team, 0):
            reasons.append("budget_exceeded")
        dropped = [f for f in files if path_blocked(self.p, f)]
        leaked = {f: s for f, body in files.items() if f not in dropped and (s := scan(body))}
        if leaked:
            reasons.append("secret_in_context")
        decision = "deny" if reasons else "allow"
        if decision == "allow":
            self.used[team] += tokens
        rec = {"dev": dev, "team": team, "client": client, "model": model, "decision": decision, "reasons": reasons,
               "files_dropped": dropped, "secret_findings": leaked}
        self.log.append(rec)
        return rec

    def command(self, dev: str, cmd: str) -> str:
        d = command_decision(self.p, cmd)
        self.log.append({"dev": dev, "command": cmd, "decision": d})
        return d
