"""SYNTHETIC fleet + labelled snippets (self-written regression set); measured on that synthetic data."""
import json, pathlib, sys
from collections import Counter
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from cag.audit_config import audit  # noqa: E402
from cag.fleet import COMMANDS, SECRET_SNIPPETS, fleet  # noqa: E402
from cag.gate import Gate  # noqa: E402
from cag.policy import load  # noqa: E402
from cag.secrets import scan  # noqa: E402

def main():
    p = load()
    devs = fleet()
    findings = {c["dev"]: audit(p, c) for c in devs}
    viol = Counter(v for vs in findings.values() for v in vs)
    compliant = sum(not v for v in findings.values())
    y = [s[1] for s in SECRET_SNIPPETS]; pred = [int(bool(scan(s[0]))) for s in SECRET_SNIPPETS]
    tp = sum(a and b for a, b in zip(y, pred)); fp = sum((not a) and b for a, b in zip(y, pred)); fn = sum(a and not b for a, b in zip(y, pred))
    g = Gate(p)
    cmd_ok = sum(g.command("dev01", c) == want for c, want in COMMANDS)
    reqs = [("dev01", "platform", "ide-assistant", "code-large", {"src/app.py": "print(1)", ".env": "X=1"}, 1000),
            ("dev02", "contractors", "cli-agent", "code-large", {"a.py": "x"}, 1000),
            ("dev03", "platform", "unvetted-desktop-app", "code-small", {}, 10),
            ("dev04", "platform", "cli-agent", "code-small", {"cfg.py": SECRET_SNIPPETS[0][0]}, 10),
            ("dev05", "contractors", "cli-agent", "code-small", {"b.py": "y"}, 400_000)]
    gate = [g.request(*r) for r in reqs]
    m = {
        "Developer configs audited": len(devs),
        "Fully compliant configs": f"{compliant}/{len(devs)} ({compliant / len(devs):.0%})",
        "Violations by type": ", ".join(f"{k}={v}" for k, v in sorted(viol.items())),
        "Secret scanner precision": f"{tp}/{tp + fp}", "Secret scanner recall": f"{tp}/{tp + fn}",
        "Command policy decisions matching expected": f"{cmd_ok}/{len(COMMANDS)}",
        "Gate demo requests denied": f"{sum(r['decision'] == 'deny' for r in gate)}/{len(gate)}",
        "Blocked files dropped from context": sum(len(r["files_dropped"]) for r in gate),
    }
    out = {"label": "SYNTHETIC fleet and self-written labelled snippets (regression check, not a benchmark)",
           "sample": f"{len(devs)} configs, {len(SECRET_SNIPPETS)} snippets, {len(COMMANDS)} commands",
           "metrics": m, "findings": findings, "gate": gate}
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results" / "results.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(m, indent=2))

if __name__ == "__main__":
    main()
