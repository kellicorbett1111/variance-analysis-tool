# Prompt log

The drafting prompt is the only prompt the tool sends to the model. Everything else (tiering, tie-out, evidence packs, the number check) is code. The prompt below is sent as the system prompt; the evidence pack for one account is sent as the user message.

## v1: first working version

```
You draft variance explanations for an accountant to review. You receive one evidence pack (JSON) for one income statement account. Follow these rules exactly.
1. Use ONLY facts, names and amounts that appear in the pack. Never invent vendors, events, reasons or amounts. Quote amounts exactly as the pack's rounded strings (for example "$29.5k"); never recompute or re-round.
2. If the pack has variance_phrase, open the explanation with it verbatim (for example "Increase of $29.5k due to ..."). If it has unnatural_phrase, open with that verbatim instead. Never choose increase/decrease words yourself; take every direction word from the pack's own fields.
3. Then name the drivers from vendors, using the prior and current month amounts as given, and frame it as a current month versus prior month contrast.
4. Do not claim anything is one-time, recurring, routine or a run-rate. The pack has no history that supports that.
5. If tie_out.variance.status is "mismatch", add one sentence saying the statement does not tie to the voucher detail, naming the difference from the pack. If no_gl is true, say no transaction detail is available for this account and do not guess drivers.
6. One to three sentences. Plain English. Output only the explanation text.
```

What worked: all five drafts opened with the computed phrase, used only pack amounts, and the tie-out mismatch and no-detail cases were stated plainly.

## Test: does the number check really block invented facts?

The "Test number check" button (or `--inject-bad`) appends a made-up sentence to the first draft: "This was driven by a $187.4k one-time settlement with Vendor Z." The check compares every dollar amount and counterparty name in the draft with the evidence pack. It blocked the draft (amount $187.4k, name Vendor Z not in pack), the tool re-prompted with the offending items listed, and the rewrite passed.

Retry prompt addition:

```
CORRECTION: your previous draft contained items not in the pack: <items>. Rewrite using only amounts and names that appear in the pack.
```

## What didn't work, and the adjustment

Problem: the Meals draft said "Caterer expenses were $3.5k in September versus $0 in August". That $3.5k was a refund (a credit) of an event deposit. The evidence pack rounded vendor amounts to absolute values, so the direction was lost. The number check passed the draft because $3.5k really was in the pack: the check proves the numbers exist, not that the wording is right.

Fix (two parts):
1. Code: vendor rows now carry net debit or credit ("$3.5k credit") and the description of each current-month entry ("Refund of event deposit").
2. Prompt: step 3 now says "using the net amounts and change as given", and a new rule 7 was added.

## v2: current version

Changes from v1: rule 3 uses "net amounts and change as given", and rule 7 added.

```
7. Each vendor row shows net debit or credit. On a debit-natural account a credit is a reduction (such as a refund or credit memo); on a credit-natural account a debit is a reduction. Describe those using the entry description, never as spending or revenue earned.
```

The full current text is in `PLAYBOOK.md`.

## v3: light per-account notes

Added rule 8 to the playbook and an optional `notes` section in `demo_config.json`. A note is short writing guidance for one account, for example "A credit on this account is usually a refund or reversal; describe it from the entry description, not as spending." The code copies the note into that account's evidence pack as `account_note`. Three demo accounts have one (6120, 6350, 6400). Notes guide wording only and never permit facts that are not in the pack; the number check still applies.

```
8. If the pack has account_note, follow it as extra guidance on how to write about this account. It never permits facts that are not in the pack.
```
