"""Secret detection for files/snippets before they are sent to an assistant as context.
Rules: known key formats + a Shannon-entropy check for quoted tokens near secret-like names."""
import math
import re

RULES = {
    "aws_access_key_id": re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b"),
    "private_key": re.compile(r"-----BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY-----"),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36}\b"),
    "slack_token": re.compile(r"\bxox[abpr]-[A-Za-z0-9-]{10,}\b"),
    "jwt": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    "conn_string_password": re.compile(r"(?i)(password|pwd)\s*=\s*[^;'\"\s]{6,}"),
}
NAME = re.compile(r"(?i)(secret|token|api[_-]?key|passwd|password|client[_-]?secret)\w*\s*[:=]\s*['\"]([^'\"]{16,})['\"]")
PLACEHOLDER = re.compile(r"(?i)(example|changeme|placeholder|your[_-]|xxxx|dummy|<.*>|\$\{)")

def entropy(s: str) -> float:
    from collections import Counter
    n = len(s)
    return -sum(c / n * math.log2(c / n) for c in Counter(s).values()) if n else 0.0

def scan(text: str) -> list[str]:
    found = [k for k, rx in RULES.items() if rx.search(text)]
    for m in NAME.finditer(text):
        val = m.group(2)
        if not PLACEHOLDER.search(val) and entropy(val) >= 3.5:
            found.append("high_entropy_assignment")
    return sorted(set(found))
