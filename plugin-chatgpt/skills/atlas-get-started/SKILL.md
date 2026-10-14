---
name: atlas-get-started
description: Check that Atlas is connected and show the person what it can do for them. Use right after the Atlas plugin is installed, or when the person asks what Atlas can do, whether their broker account is connected, or how much of their plan is left.
---

# Getting started with Atlas

Atlas gives you tools to scan options flow, analyze real-time stock market
data, and build investing and trading workflows and alerts. This skill is the
first look around.

## What to do

1. Call `Subscription-Status`. It answers with the person's plan, how many
   requests they have used this month and how many are left, and a link to
   their dashboard. Give them that link when they ask about their plan or
   about connecting a broker.
2. Call `Broker-Connections`. It lists the broker accounts they have
   connected.
   - No account connected: say so, and that it is connected from the
     dashboard. Everything that only reads the market works without one.
3. Tell them, in a few lines, what they can ask for next. Offer, do not push:
   - **Look at the market**: options flow, quotes, charts, options chains,
     dealer exposure, earnings and filings. See the `atlas-market-data` skill.
   - **Build a workflow**: a plan Atlas runs for them on a schedule or when
     an alert goes off. See `atlas-workflows`.
   - **Set an alert**: be told when something happens in the market. See
     `atlas-alerts`.
   - **Run a workflow yourself**: you do the thinking for a workflow and hand
     in each run; Atlas checks it and carries it out on the person's own
     terms. See `atlas-agent-run-workflows`, and `atlas-agent-run-loop` for
     running it on a schedule.
   - **Read plays**: the trade ideas posted on the community board and in the
     groups they follow. See `atlas-signals`.
   - **See their account**: holdings, orders, open trades and results.

## What to keep in mind

- Looking something up uses one request of the person's plan. Working on
  their own setups (workflows, alerts) does not.
- **Nothing is bought, sold or changed at a broker from here.** Placing an
  order, setting up a trade that waits for a price, closing a trade, and
  posting or taking a play are done in Atlas itself, on the dashboard. When
  the person asks for one of those, say so and give them the dashboard link.
  Do not look for another way to do it.
- A workflow is a plan the person writes and switches on. Atlas runs it later
  by its own schedule or alert, on the terms the person set.
- Atlas does not give investment advice. Say what the data shows and what
  the person's own plan says; the decision is theirs.
