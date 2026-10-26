# Kimi pricing reference (checked 2026-10-26)

USD per million tokens. Source: https://platform.moonshot.ai/docs/pricing/chat

| Tier | Model | Input | Output | Applies to |
|---|---|---:|---:|---|
| T1 | Kimi K3.1 Pro (low effort) (`kimi-k3.1-pro`) | $2.00 | $10.00 | all prompt sizes |
| T2 | Kimi K3.1 Pro (`kimi-k3.1-pro`) | $2.00 | $10.00 | all prompt sizes |
| T3 | Kimi K3.1 Pro (`kimi-k3.1-pro`) | $2.00 | $10.00 | all prompt sizes |
| T4 | Kimi K3.1 Pro (max effort) (`kimi-k3.1-pro`) | $2.00 | $10.00 | all prompt sizes |

- Kimi API list prices. T1-T4 use K3.1 Pro because no supported cheaper micro model is available; savings come from tools, lower effort and smaller context, not model-price arbitrage.
- Kimi Code membership uses quota rather than these per-token API prices. Model IDs in Kimi Code omit the `kimi-` prefix: use `k3.1-pro`; check `/usage` for quota.
- K3.1 Pro requires thinking. T4 means max effort; Highspeed costs twice as much and is not used in the savings model.

Prices change. Re-check the source page before quoting numbers.