# Training module: governing coding assistants and desktop AI apps
**Audience:** platform, security and DevEx engineers, half a day.
## Learning objectives
1. Explain shadow-AI risk from personal keys and unvetted desktop apps.
2. Route every client through one gateway with virtual keys.
3. Write a context filter and secret scanner, and measure them honestly.
4. Design command policies for agentic CLIs and know their limits.
## Labs
| # | Lab | Done when |
|---|---|---|
| 1 | Run the eval; explain each violation type | Fleet table explained |
| 2 | Add a rule for API keys of another provider format | Parametrized test added |
| 3 | Catch `bash -c "rm -rf /"` | New deny test passes |
| 4 | Reduce the secret-name false positive without losing recall | Both known-failure tests updated honestly |
| 5 | Add a per-developer daily token cap | Gate test passes |
## Capstone
Write the policy for a fictional 200-developer firm with contractors, regenerate the README, and draft a rollout plan (shadow → warn → enforce) with the metrics you would report.
