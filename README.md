# Vendor Onboarding Readiness Checker

Checks vendor onboarding evidence for requested controls, named ownership, expiry, and review status.

## Architecture

```text
JSON payload → domain algorithm → evidence-backed findings → human review
                              └→ OpenAI / CrewAI / Claude Code / Lyzr export surfaces
```

The core implementation is `agent.py` and exposes `analyze(payload)`. Tests include valid, malformed, boundary, and domain-specific cases.

## Run

```bash
python3 agent.py examples/good-input.json
python3 -m unittest discover -s tests -v
python3 tools/audit-vendor-onboarding-readiness-checker.py examples/good-input.json
```

## Limitations

This does not assess vendor trustworthiness, certify compliance, or replace procurement, legal, privacy, or security review.
