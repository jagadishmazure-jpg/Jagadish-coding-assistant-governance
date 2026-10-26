# Implementation guide
1. Inventory assistants in use (endpoint scan, proxy logs). Approve a short list.
2. Stand up the gateway; issue per-developer virtual keys; block direct provider egress at the proxy.
3. Push base-URL settings via MDM or managed dotfiles; collect configs nightly and run the auditor.
4. Enable context filtering (blocked globs) and secret scanning at the gateway; deny on findings.
5. Turn off auto-approve for agentic CLIs; adopt the command deny/approval lists; run agents in a sandbox or dev container.
6. Set per-team model lists and budgets; contractors get smaller models and budgets.
7. Report weekly: compliance rate, violations by type, denied requests, spend by team.
