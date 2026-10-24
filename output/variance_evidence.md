# Variance analysis evidence

Target September 2026, prior August 2026, threshold $25.0k.

## 4010 Service revenue
- Tier 1: change exceeds threshold of $25.0k
- Beginning balance (August 2026): -520,000.00
- Ending balance (September 2026): -548,000.00
- Tie-out (variance): tie
```json
{
  "account": "4010",
  "name": "Service revenue",
  "statement": "Income Statement",
  "currency": "USD",
  "target_month": "September 2026",
  "prior_month": "August 2026",
  "tier": 1,
  "tier_reason": "change exceeds threshold of $25.0k",
  "natural_balance": "credit",
  "prior_month_amount": "$520.0k",
  "current_month_amount": "$548.0k",
  "tie_out": {
    "cm": {
      "status": "tie"
    },
    "pm": {
      "status": "tie"
    },
    "variance": {
      "status": "tie"
    }
  },
  "no_gl": false,
  "vendors": [
    {
      "counterparty": "Customer R",
      "August 2026 net": "$0",
      "September 2026 net": "$15.0k credit",
      "change": "increase of $15.0k",
      "current_month_entries": [
        {
          "description": "New customer onboarding fee",
          "amount": "$15.0k",
          "side": "credit"
        }
      ]
    },
    {
      "counterparty": "Customer Q",
      "August 2026 net": "$220.0k credit",
      "September 2026 net": "$233.0k credit",
      "change": "increase of $13.0k",
      "current_month_entries": [
        {
          "description": "Monthly service fee incl. added seats",
          "amount": "$233.0k",
          "side": "credit"
        }
      ]
    },
    {
      "counterparty": "Customer P",
      "August 2026 net": "$300.0k credit",
      "September 2026 net": "$300.0k credit",
      "change": "no change",
      "current_month_entries": [
        {
          "description": "Monthly service fee",
          "amount": "$300.0k",
          "side": "credit"
        }
      ]
    }
  ],
  "variance_phrase": "Increase of $28.0k due to"
}
```

## 6120 Software subscriptions
- Tier 1: change exceeds threshold of $25.0k
- Beginning balance (August 2026): 42,000.00
- Ending balance (September 2026): 71,500.00
- Tie-out (variance): tie
```json
{
  "account": "6120",
  "name": "Software subscriptions",
  "statement": "Income Statement",
  "currency": "USD",
  "target_month": "September 2026",
  "prior_month": "August 2026",
  "tier": 1,
  "tier_reason": "change exceeds threshold of $25.0k",
  "natural_balance": "debit",
  "prior_month_amount": "$42.0k",
  "current_month_amount": "$71.5k",
  "tie_out": {
    "cm": {
      "status": "tie"
    },
    "pm": {
      "status": "tie"
    },
    "variance": {
      "status": "tie"
    }
  },
  "no_gl": false,
  "vendors": [
    {
      "counterparty": "Vendor A",
      "August 2026 net": "$0",
      "September 2026 net": "$24.0k debit",
      "change": "increase of $24.0k",
      "current_month_entries": [
        {
          "description": "Annual license",
          "amount": "$24.0k",
          "side": "debit"
        }
      ]
    },
    {
      "counterparty": "Vendor B",
      "August 2026 net": "$12.0k debit",
      "September 2026 net": "$17.5k debit",
      "change": "increase of $5.5k",
      "current_month_entries": [
        {
          "description": "Usage charges",
          "amount": "$17.5k",
          "side": "debit"
        }
      ]
    },
    {
      "counterparty": "Vendor C",
      "August 2026 net": "$30.0k debit",
      "September 2026 net": "$30.0k debit",
      "change": "no change",
      "current_month_entries": [
        {
          "description": "Core platform subscription",
          "amount": "$30.0k",
          "side": "debit"
        }
      ]
    }
  ],
  "account_note": "Name each counterparty behind the change and say whether the movement is a new charge or a change in an existing counterparty's amount.",
  "variance_phrase": "Increase of $29.5k due to"
}
```

## 6200 Professional fees
- Tier 1: change exceeds threshold of $25.0k
- Beginning balance (August 2026): 18,000.00
- Ending balance (September 2026): 61,000.00
- Tie-out (variance): mismatch
```json
{
  "account": "6200",
  "name": "Professional fees",
  "statement": "Income Statement",
  "currency": "USD",
  "target_month": "September 2026",
  "prior_month": "August 2026",
  "tier": 1,
  "tier_reason": "change exceeds threshold of $25.0k",
  "natural_balance": "debit",
  "prior_month_amount": "$18.0k",
  "current_month_amount": "$61.0k",
  "tie_out": {
    "cm": {
      "status": "mismatch",
      "difference": "$3.0k",
      "difference_full": "$3,000"
    },
    "pm": {
      "status": "tie"
    },
    "variance": {
      "status": "mismatch",
      "difference": "$3.0k",
      "difference_full": "$3,000"
    }
  },
  "no_gl": false,
  "vendors": [
    {
      "counterparty": "Firm M",
      "August 2026 net": "$0",
      "September 2026 net": "$40.0k debit",
      "change": "increase of $40.0k",
      "current_month_entries": [
        {
          "description": "Project services",
          "amount": "$40.0k",
          "side": "debit"
        }
      ]
    },
    {
      "counterparty": "Firm L",
      "August 2026 net": "$18.0k debit",
      "September 2026 net": "$18.0k debit",
      "change": "no change",
      "current_month_entries": [
        {
          "description": "Advisory services",
          "amount": "$18.0k",
          "side": "debit"
        }
      ]
    }
  ],
  "variance_phrase": "Increase of $43.0k due to"
}
```

## 6350 Meals
- Tier 2: current month balance runs against natural debit balance
- Beginning balance (August 2026): 4,000.00
- Ending balance (September 2026): -1,200.00
- Tie-out (variance): tie
```json
{
  "account": "6350",
  "name": "Meals",
  "statement": "Income Statement",
  "currency": "USD",
  "target_month": "September 2026",
  "prior_month": "August 2026",
  "tier": 2,
  "tier_reason": "current month balance runs against natural debit balance",
  "natural_balance": "debit",
  "prior_month_amount": "$4.0k",
  "current_month_amount": "$1.2k",
  "tie_out": {
    "cm": {
      "status": "tie"
    },
    "pm": {
      "status": "tie"
    },
    "variance": {
      "status": "tie"
    }
  },
  "no_gl": false,
  "vendors": [
    {
      "counterparty": "Caterer",
      "August 2026 net": "$0",
      "September 2026 net": "$3.5k credit",
      "change": "decrease of $3.5k",
      "current_month_entries": [
        {
          "description": "Refund of event deposit",
          "amount": "$3.5k",
          "side": "credit"
        }
      ]
    },
    {
      "counterparty": "Employee expenses",
      "August 2026 net": "$4.0k debit",
      "September 2026 net": "$2.3k debit",
      "change": "decrease of $1.7k",
      "current_month_entries": [
        {
          "description": "Team meals",
          "amount": "$2.3k",
          "side": "debit"
        }
      ]
    }
  ],
  "account_note": "A credit on this account is usually a refund or reversal; describe it from the entry description, not as spending.",
  "unnatural_phrase": "Current month balance of $1.2k is a credit on a debit-natural account in September 2026"
}
```

## 6400 Contract labor
- Tier 1: change exceeds threshold of $25.0k
- Beginning balance (August 2026): 12,000.00
- Ending balance (September 2026): 40,000.00
- Tie-out (variance): no_gl
```json
{
  "account": "6400",
  "name": "Contract labor",
  "statement": "Income Statement",
  "currency": "USD",
  "target_month": "September 2026",
  "prior_month": "August 2026",
  "tier": 1,
  "tier_reason": "change exceeds threshold of $25.0k",
  "natural_balance": "debit",
  "prior_month_amount": "$12.0k",
  "current_month_amount": "$40.0k",
  "tie_out": {
    "cm": {
      "status": "no_gl"
    },
    "pm": {
      "status": "no_gl"
    },
    "variance": {
      "status": "no_gl"
    }
  },
  "no_gl": true,
  "vendors": [],
  "account_note": "If no transaction detail exists, say so plainly; do not guess at contractors or reasons.",
  "variance_phrase": "Increase of $28.0k"
}
```
