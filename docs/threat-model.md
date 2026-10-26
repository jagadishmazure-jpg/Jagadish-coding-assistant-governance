# Threat model
| Threat | Control | Gap |
|---|---|---|
| Shadow AI / personal keys (data exfiltration) | Auditor flags bypass + personal keys | Needs egress blocking |
| Secrets sent as context (OWASP LLM02) | Blocked globs + secret scan | Low-entropy passwords |
| Destructive agent commands (LLM06 excessive agency) | Deny / approval lists, no auto-approve | Obfuscated commands |
| Rogue MCP server (LLM03 supply chain) | Approved MCP list | Server impersonation |
| Unbounded spend (LLM10) | Team budgets | In-memory |
