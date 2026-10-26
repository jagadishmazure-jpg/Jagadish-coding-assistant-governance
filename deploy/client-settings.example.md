# Routing coding tools through the gateway (examples, WRITTEN, NOT RUN)

Most coding CLIs, IDE extensions and SDKs honour a base-URL override. Point them at the gateway and issue a per-developer virtual key from the gateway (never a personal provider key).

```bash
# OpenAI-compatible clients / SDKs
export OPENAI_BASE_URL="https://ai-gateway.quillstone.example/v1"
export OPENAI_API_KEY="<virtual key issued by the gateway>"
# Anthropic-compatible clients / SDKs
export ANTHROPIC_BASE_URL="https://ai-gateway.quillstone.example"
export ANTHROPIC_API_KEY="<virtual key issued by the gateway>"
```

Distribute via your device-management tool (MDM) or a managed dotfile, then verify with `audit_config.audit` on collected configs. Check each client's own documentation for the exact setting name; names change between versions.
