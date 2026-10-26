# Interview points
- The biggest risk is bypass: personal keys straight to a provider. Base-URL override plus egress blocking fixes it.
- Filter context before it leaves the laptop or at the gateway: `.env`, keys, state files.
- Command policies help but glob matching is bypassable; sandboxing is the real boundary.
- I report scanner misses and false positives as tests, not hide them.
