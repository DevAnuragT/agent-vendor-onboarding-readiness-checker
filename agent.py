
#!/usr/bin/env python3
"""Deterministic, local-only passport implementation."""
import json
import math
import sys
from pathlib import Path

DOMAIN = 'Vendor Onboarding Readiness Checker'

def _num(value, name, findings):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        findings.append(f"{name}: must be a finite number")
        return 0
    return value

def analyze(payload):
    if not isinstance(payload, dict):
        raise ValueError("payload must be an object")
    findings = []
    required=payload.get("required_controls"); evidence=payload.get("evidence")
    if not isinstance(required,list) or not isinstance(evidence,list): raise ValueError("required_controls and evidence are required")
    records={}
    for e in evidence:
        if not isinstance(e,dict): raise ValueError("evidence records must be objects")
        cid=e.get("control")
        if cid in records: findings.append(f"duplicate evidence for {cid}")
        records[cid]=e
    for cid in required:
        e=records.get(cid)
        if not e: findings.append(f"missing evidence for {cid}"); continue
        for k in ("artifact","owner"):
            if not isinstance(e.get(k),str) or not e[k].strip(): findings.append(f"{cid}: {k} missing")
        if e.get("reviewed") is not True: findings.append(f"{cid}: review incomplete")
        days=_num(e.get("days_until_expiry"),"days_until_expiry",findings)
        if days<0: findings.append(f"{cid}: evidence expired")
    return {"domain": DOMAIN, "status": "needs-review" if findings else "ready", "findings": findings}

if __name__ == "__main__":
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    payload = json.loads(source.read_text(encoding="utf-8") if source else sys.stdin.read())
    print(json.dumps(analyze(payload), indent=2, sort_keys=True))
