# Monthly Variance Analysis Automation

Explaining why each income statement account moved versus the prior month is a recurring close task. This tool automates the repeatable parts and leaves approval with the accountant.

**Design rule:** code does every number; the model only writes the words.

1. Intake and validate (columns, period, prior month, duplicates, posting layer)
2. Tier accounts (Tier 1: change over threshold; Tier 2: balance against its normal direction)
3. Tie-out of the statement to the voucher detail, to the cent
4. Evidence pack per flagged account (amounts, drivers, direction words computed by code)
5. Draft explanation from the pack, following `PLAYBOOK.md` (the only model call)
6. Number check: any dollar amount or counterparty in a draft that is not in the pack blocks the draft, with one corrective retry
7. Evidence file for audit; an accountant reviews; nothing is posted

All data here is scrubbed demo data (one entity, USD, income statement, August and September 2026). No real organization data is used. The demo plants four cases: a clean tie, a tie-out mismatch (Professional fees), a backwards balance (Meals), and an account with no transaction detail (Contract labor).

## Files

| File | What it is and what it is for |
|---|---|
| `index.html` | The tool. A single-file web app that runs in the browser: loads the statement and voucher detail, flags accounts, ties them to the ledger, builds evidence packs, drafts explanations and runs the number check. AI drafting works inside Cowork with no key; elsewhere it needs a pasted Anthropic API key (kept in the tab only). |
| `variance_cli.py` | The same pipeline as a command-line script (standard library only). Easier to read line by line; writes the evidence file and results CSV to `output/`. |
| `PLAYBOOK.md` | The drafting prompt used by the command-line version. The web page has its own copy built in, so change both together. |
| `PROMPTS.md` | Prompt history: each version, what failed (the Meals refund wording), and how it was fixed. |
| `demo_statement.csv` | Scrubbed demo income statement (August and September 2026): account, prior month, current month, change. |
| `demo_vouchers.csv` | Scrubbed voucher (ledger) detail for the same months. The tool ties the statement to it. |
| `demo_config.json` | Command-line settings: each account's normal balance (debit or credit) and optional per-account writing notes. The threshold is a separate option (`--threshold`), and the web page keeps its own copies of these settings in its script. |
| `gen_data.py` | Regenerates the demo input files. |
| `output/variance_evidence.md` | Sample evidence file: why each account was flagged, its tie-out result, the evidence pack and any draft attempts. This sample was produced with AI off, so it has no drafts. |
| `output/variance_results.csv` | Sample results table: account, tier, beginning and ending balance, change, tie-out, draft, number check. |

## Run it

Web app: open `index.html` in a browser, or host it (below). Click "Run checks", then "Draft explanations with AI" (inside Cowork this needs no key; elsewhere paste an Anthropic API key first). "Test number check" injects an invented sentence to show it being blocked.

Command line:

```
python variance_cli.py --no-ai            # checks only
export ANTHROPIC_API_KEY=sk-ant-...
python variance_cli.py                    # with AI drafts
python variance_cli.py --inject-bad       # prove the number check blocks a made-up draft
```

Outputs are written to `output/`: `variance_evidence.md` and `variance_results.csv`.

## Host the web app for a shareable link (GitHub Pages)

1. Create a GitHub repository and upload these files.
2. Settings, Pages, deploy from the main branch, root folder.
3. Keep the file named `index.html`. The link will be `https://<user>.github.io/<repo>/`.

The page makes no calls until a user clicks the AI button, and the key is sent only to `api.anthropic.com`.

## Using your own files

Statement CSV columns: `Account, Name, Prior Month, Current Month, Change` (debit positive). Voucher CSV columns: `Date, Account display value, Amount, Posting layer`, plus optional `Voucher, Description, Name2`. Rows whose posting layer is not `Current` are excluded.
