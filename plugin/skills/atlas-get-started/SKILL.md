---
name: atlas-get-started
description: Check that Atlas is connected and show the person what it can do for them. Use right after the Atlas plugin is installed, or when the person asks what Atlas can do, whether their broker account is connected, or how much of their plan is left.
---

# Getting started with Atlas

Atlas gives you tools to scan options flow, analyze real-time stock market
data, and build investing and trading workflows that carry out a person's
plan in their own broker account. This skill is the first look around.

## What to do

1. Call `Subscription-Status`. It answers with the person's plan, how many
   requests they have used this month and how many are left, and a link to
   their dashboard. Give them that link when they ask about billing, their
   plan, or connecting a broker.
2. Call `Broker-Connections`. It lists the broker accounts they have
   connected and whether trading is switched on for each.
   - No account connected: say so, and that it is connected from the
     dashboard. Everything that only reads the market works without one.
   - More than one: never pick for them. Ask which account, every time
     something would place an order.
3. Tell them, in a few lines, what they can ask for next. Offer, do not push:
   - **Look at the market**: options flow, quotes, charts, options chains,
     dealer exposure, earnings and filings. See the `atlas-market-data` skill.
   - **Build a workflow**: a plan Atlas runs for them on a schedule or when
     an alert goes off. See `atlas-workflows`.
   - **Set an alert**: be told when something happens in the market. See
     `atlas-alerts`.
   - **Post or take a play**: one trade idea, written down in full, shared
     with a group or taken from one. See `atlas-signals`.
   - **Place and manage a trade**: preview an order, place it, and move its
     exits. See `atlas-triggers-and-trades`.

## What to keep in mind

- Looking something up uses one request of the person's plan. Working on
  their own setups (workflows, alerts, plays, previews) does not.
- Nothing is bought or sold unless the person says so. A tool that can send
  or change an order is marked for it, and your client will ask first.
- Atlas does not give investment advice. Say what the data shows and what
  the person's own plan says; the decision is theirs.
