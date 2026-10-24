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

| File | Purpose |
|---|---|
| `variance_tool.html` | Single-file web app. Checks run in the browser with no key; AI drafting needs an Anthropic API key pasted into the page (kept in the tab only). |
| `variance_cli.py` | Same pipeline as a command-line script (standard library only). |
| `PLAYBOOK.md` | The drafting prompt. |
| `PROMPTS.md` | Prompt versions, what failed, and how it was fixed. |
| `demo_statement.csv`, `demo_vouchers.csv`, `demo_config.json` | Scrubbed demo inputs. The config holds the threshold, each account's normal balance (debit or credit) and optional short per-account writing notes. |
| `gen_data.py` | Regenerates the demo inputs. |

## Run it

Web app: open `variance_tool.html` in a browser, or host it (below). Click "Run checks", paste an API key, then "Draft explanations with AI". "Test number check" injects an invented sentence to show it being blocked.

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
3. Rename `variance_tool.html` to `index.html` (or link to it by name). The link will be `https://<user>.github.io/<repo>/`.

The page makes no calls until a user clicks the AI button, and the key is sent only to `api.anthropic.com`.

## Using your own files

Statement CSV columns: `Account, Name, Prior Month, Current Month, Change` (debit positive). Voucher CSV columns: `Date, Account display value, Amount, Posting layer`, plus optional `Voucher, Description, Name2`. Rows whose posting layer is not `Current` are excluded.
