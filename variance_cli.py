#!/usr/bin/env python3
"""Monthly variance analysis automation: command-line version.

Code does the numbers (intake, tiering, tie-out, evidence packs, number check).
The model only drafts the words, following PLAYBOOK.md. Nothing is posted.

Usage:
  python variance_cli.py --no-ai                       # checks only, no API key needed
  ANTHROPIC_API_KEY=... python variance_cli.py         # full run with AI drafts
  python variance_cli.py --inject-bad                  # prove the number check blocks a made-up draft
Options: --statement FILE --vouchers FILE --threshold N --model NAME --out DIR
Standard library only.
"""
import argparse, csv, json, os, re, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).parent
MON = ["January","February","March","April","May","June","July","August","September","October","November","December"]

def fmt(n):
    a = abs(n)
    if a >= 1e6: return f"${a/1e6:.1f}M"
    if a >= 1e3: return f"${a/1e3:.1f}k"
    return f"${a:.0f}"
def full(n): return f"${abs(n):,.2f}".rstrip("0").rstrip(".") if abs(n) % 1 else f"${abs(n):,.0f}"
def mname(m): return f"{MON[int(m[5:7])-1]} {m[:4]}"
def prev_month(m):
    y, k = int(m[:4]), int(m[5:7]) - 1
    if k == 0: y, k = y - 1, 12
    return f"{y}-{k:02d}"
def eff(delta, nat): return "increase" if (delta > 0 if nat == "debit" else delta < 0) else "decrease"
def side(x): return "$0" if x == 0 else fmt(x) + (" debit" if x > 0 else " credit")

def read_csv(p):
    with open(p, newline="", encoding="utf-8-sig") as f:
        return [{k.strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]

def analyze(stmt_path, vch_path, thr, naturals, notes=None):
    notes = notes or {}
    stmt, vch = read_csv(stmt_path), read_csv(vch_path)
    for need, rows, name in (( ["Account","Name","Prior Month","Current Month","Change"], stmt, "statement"),
                             (["Date","Account display value","Amount","Posting layer"], vch, "voucher detail")):
        miss = [k for k in need if not rows or k not in rows[0]]
        if miss: sys.exit(f"STOP: {name} is missing columns: {', '.join(miss)}")
    cur = [r for r in vch if r["Posting layer"] == "Current"]
    warns = []
    if len(vch) - len(cur): warns.append(f'{len(vch)-len(cur)} voucher row(s) excluded: posting layer is not "Current".')
    rows = [dict(acct=r["Account display value"][:4], m=r["Date"][:7], amt=float(r["Amount"]),
                 desc=r.get("Description", ""), cp=r.get("Name2") or "(unattributed)") for r in cur]
    months = sorted({r["m"] for r in rows})
    if len(months) < 2: sys.exit(f"STOP: need at least two months of voucher detail; found {len(months)}.")
    target = months[-1]; prior = prev_month(target)
    if prior not in months: sys.exit(f"STOP: prior month {prior} is missing from the voucher detail (found {months}).")
    codes = [r["Account"][:4] for r in stmt]
    dup = sorted({c for c in codes if codes.count(c) > 1})
    if dup: sys.exit(f"STOP: duplicate account rows {dup}; resolve before running.")
    out = []
    for r in stmt:
        code = r["Account"][:4]; name = r["Name"]
        p, c, chg = float(r["Prior Month"]), float(r["Current Month"]), float(r["Change"])
        nat = naturals.get(code, "credit" if code[0] == "4" else "debit")
        t1 = abs(chg) > thr
        against = c != 0 and ((nat == "debit" and c < 0) or (nat == "credit" and c > 0))
        tier = 1 if t1 else (2 if against else 0)
        if not tier: continue
        ents = [e for e in rows if e["acct"] == code]
        no_gl = not ents
        g = lambda m, e=ents: sum(x["amt"] for x in e if x["m"] == m)
        def comp(rep, gl):
            d = round(rep - gl, 2); return {"status": "tie" if abs(d) <= 0.01 else "mismatch", "diff": d}
        tie = ({k: {"status": "no_gl"} for k in ("cm", "pm", "variance")} if no_gl else
               {"cm": comp(c, g(target)), "pm": comp(p, g(prior)), "variance": comp(chg, g(target) - g(prior))})
        cps = sorted({e["cp"] for e in ents if e["m"] in (target, prior)}, key=lambda x: x)
        vendors = []
        for cp in cps:
            vp = sum(e["amt"] for e in ents if e["cp"] == cp and e["m"] == prior)
            vc = sum(e["amt"] for e in ents if e["cp"] == cp and e["m"] == target)
            d = vc - vp
            vendors.append((abs(d), {"counterparty": cp, mname(prior) + " net": side(vp), mname(target) + " net": side(vc),
                "change": "no change" if d == 0 else f"{eff(d, nat)} of {fmt(d)}",
                "current_month_entries": [{"description": e["desc"], "amount": fmt(e["amt"]), "side": "debit" if e["amt"] > 0 else "credit"}
                                          for e in ents if e["cp"] == cp and e["m"] == target]}))
        vendors = [v for _, v in sorted(vendors, key=lambda x: -x[0])]
        pack = {"account": code, "name": name, "statement": "Income Statement", "currency": "USD",
                "target_month": mname(target), "prior_month": mname(prior), "tier": tier,
                "tier_reason": f"change exceeds threshold of {fmt(thr)}" if tier == 1 else f"current month balance runs against natural {nat} balance",
                "natural_balance": nat, "prior_month_amount": fmt(p), "current_month_amount": fmt(c),
                "tie_out": {k: ({"status": v["status"], "difference": fmt(v["diff"]), "difference_full": full(v["diff"])} if v["status"] == "mismatch" else {"status": v["status"]}) for k, v in tie.items()},
                "no_gl": no_gl, "vendors": [] if no_gl else vendors}
        if notes.get(code): pack["account_note"] = notes[code]
        if tier == 1: pack["variance_phrase"] = f"{eff(chg, nat).capitalize()} of {fmt(chg)}" + ("" if no_gl else " due to")
        else: pack["unnatural_phrase"] = f"Current month balance of {fmt(c)} is a {'credit' if nat == 'debit' else 'debit'} on a {nat}-natural account in {mname(target)}"
        out.append({"code": code, "name": name, "prior": p, "cur": c, "chg": chg, "tier": tier, "tie": tie, "pack": pack})
    return {"target": target, "prior": prior, "n_accts": len(stmt), "warns": warns, "out": out}

def allowed(pack):
    s = set(re.findall(r"\$[\d,]+(?:\.\d+)?[kM]?", json.dumps(pack)))
    return s, {v["counterparty"] for v in pack["vendors"]}

def number_check(text, pack, all_cps):
    s, cps = allowed(pack); bad = []
    bad += ["amount " + x for x in re.findall(r"\$[\d,]+(?:\.\d+)?[kM]?", text) if x not in s]
    bad += ["name " + n for n in all_cps if n not in cps and n in text]
    bad += ["name " + n for n in re.findall(r"\b(?:Vendor|Firm|Customer) [A-Z]\b", text) if n not in cps]
    return sorted(set(bad))

def call_model(system, pack, model, key):
    body = json.dumps({"model": model, "max_tokens": 400, "system": system,
                       "messages": [{"role": "user", "content": "Evidence pack:\n" + json.dumps(pack, indent=2)}]}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body, method="POST",
        headers={"content-type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return "".join(c.get("text", "") for c in json.load(r)["content"]).strip()

def draft(item, all_cps, playbook, model, key, inject):
    log, bad, text = [], [], ""
    for attempt in (1, 2):
        extra = f"\n\nCORRECTION: your previous draft contained items not in the pack: {', '.join(bad)}. Rewrite using only amounts and names that appear in the pack." if attempt == 2 else ""
        text = call_model(playbook + extra, item["pack"], model, key)
        if inject and attempt == 1: text += " This was driven by a $187.4k one-time settlement with Vendor Z."
        bad = number_check(text, item["pack"], all_cps)
        log.append({"attempt": attempt, "text": text, "blocked": bad})
        if not bad: break
    return text, bad, log

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--statement", default=str(HERE / "demo_statement.csv"))
    ap.add_argument("--vouchers", default=str(HERE / "demo_vouchers.csv"))
    ap.add_argument("--threshold", type=float, default=25000)
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--out", default=str(HERE / "output"))
    ap.add_argument("--no-ai", action="store_true"); ap.add_argument("--inject-bad", action="store_true")
    a = ap.parse_args()
    cfg = json.load(open(HERE / "demo_config.json"))
    R = analyze(a.statement, a.vouchers, a.threshold, cfg["naturals"], cfg.get("notes", {}))
    print(f"Target {mname(R['target'])}, prior {mname(R['prior'])}. {R['n_accts']} accounts. "
          f"Tier 1: {sum(x['tier']==1 for x in R['out'])}, Tier 2: {sum(x['tier']==2 for x in R['out'])}.")
    for w in R["warns"]: print("Warning:", w)
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    use_ai = not a.no_ai and bool(key)
    if not a.no_ai and not key: print("No ANTHROPIC_API_KEY set: running checks only (use --no-ai to silence).")
    playbook = (HERE / "PLAYBOOK.md").read_text()
    all_cps = sorted({v["counterparty"] for x in R["out"] for v in x["pack"]["vendors"]})
    md = [f"# Variance analysis evidence\n\nTarget {mname(R['target'])}, prior {mname(R['prior'])}, threshold {fmt(a.threshold)}.\n"]
    rows = []
    for i, x in enumerate(R["out"]):
        v = x["tie"]["variance"]; st = v["status"]
        print(f"\n[{x['code']}] {x['name']}  Tier {x['tier']}  change {x['chg']:,.0f}  tie-out: {st}" + (f" (diff {v['diff']:,.2f})" if st == "mismatch" else ""))
        text, bad, log = "", [], []
        if use_ai:
            try: text, bad, log = draft(x, all_cps, playbook, a.model, key, a.inject_bad and i == 0)
            except Exception as e: text = f"[AI draft unavailable: {e}]"
            print("  Draft:", text); print("  Number check:", "pass" if not bad else "BLOCKED " + ", ".join(bad))
            if len(log) > 1 and not bad: print("  (first draft blocked:", ", ".join(log[0]["blocked"]) + "; passed after retry)")
        md.append(f"\n## {x['code']} {x['name']}\n- Tier {x['tier']}: {x['pack']['tier_reason']}\n- Beginning balance ({mname(R['prior'])}): {x['prior']:,.2f}\n- Ending balance ({mname(R['target'])}): {x['cur']:,.2f}\n- Tie-out (variance): {st}\n```json\n{json.dumps(x['pack'], indent=2)}\n```\n")
        for l in log: md.append(f"- Attempt {l['attempt']}: {l['text']} [{'blocked: ' + ', '.join(l['blocked']) if l['blocked'] else 'passed number check'}]\n")
        rows.append([x["code"], x["name"], x["tier"], x["prior"], x["cur"], x["chg"], st, text, "pass" if use_ai and not bad else ("blocked" if bad else "")])
    Path(a.out).mkdir(exist_ok=True)
    (Path(a.out) / "variance_evidence.md").write_text("".join(md))
    with open(Path(a.out) / "variance_results.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["Account", "Name", "Tier", "Beginning balance", "Ending balance", "Change", "Tie-out", "Draft explanation", "Number check"]); w.writerows(rows)
    print(f"\nWrote {a.out}/variance_evidence.md and variance_results.csv. Drafts are for accountant review; nothing is posted.")

if __name__ == "__main__": main()
