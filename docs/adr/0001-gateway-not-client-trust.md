# ADR 0001: Enforce at the gateway, audit at the client
Status: accepted. Client settings can be changed by the developer, so they are audited but not trusted; the gateway enforces model, budget, context and secret rules. Consequence: direct provider egress must be blocked for enforcement to hold.
