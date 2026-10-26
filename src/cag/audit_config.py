"""Audit developer-machine assistant configs (synthetic) against policy."""

def audit(policy: dict, cfg: dict) -> list[str]:
    v = []
    if cfg.get("client") not in policy["approved_clients"]:
        v.append("unapproved_client")
    if cfg.get("base_url") != policy["gateway_base_url"]:
        v.append("bypasses_gateway")
    if cfg.get("personal_api_key"):
        v.append("personal_api_key")
    bad = [s for s in cfg.get("mcp_servers", []) if s not in policy["allowed_mcp_servers"]]
    if bad:
        v.append("unapproved_mcp_server")
    if cfg.get("auto_approve") and not policy["auto_approve_allowed"]:
        v.append("auto_approve_enabled")
    if cfg.get("model") not in policy["team_models"].get(cfg.get("team"), []):
        v.append("model_not_allowed_for_team")
    if cfg.get("telemetry_off"):
        v.append("audit_logging_disabled")
    return v
