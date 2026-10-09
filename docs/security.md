# Atlas: security and what it can do

## Signing in

- **Over HTTPS only**, at `https://atlasmcp.finmanagerai.com/mcp`.
- **Sign-in in your browser (OAuth 2.0).** An assistant that supports it is
  given only the address. The first time, it opens Atlas's sign-in page; you
  sign in there and approve the connection. The assistant receives a token for
  your account and never sees your password.
- **Or your access key.** For an assistant that cannot open a sign-in page:
  `Authorization: Bearer <key>`. The key is on your dashboard under
  **Profile → API / CLI / MCP Key**. Replacing it there stops the old one at
  once.
- An assistant can also start a sign-in for you and hand you a link to open,
  where no browser can be opened for it. It never sees a password that way
  either.

## What Atlas can and cannot do

- **Read**: market data, and your own things: your plan and usage, your
  connected broker accounts with their balances, holdings and history, your
  workflows, alerts, plays, strategies and saved memory.
- **Change**: only through tools that say so. [tools.md](tools.md) marks every
  tool as reads, adds, changes or acts, and your assistant uses that to ask
  you first.
- **Send orders**: only to a broker account you connected on the Atlas
  dashboard, and only when you ask, or when a workflow you switched on calls
  for it.
- **Not on your computer.** Atlas runs on its own servers. It does not read
  your files and does not run commands on your machine.
- **Only your own account.** A tool answers for the person who is signed in.
  Other people's public workflows and plays come without their personal
  details or anything about their broker.

## Orders

- **Preview first.** `Preview-Order` stages an order and shows it to you;
  nothing is sent until you accept it or `Place-Order` is called with it.
- **A workflow can wait for you.** With "review before it places" on, each run
  is held until you approve it.
- **Which account is always your choice.** With more than one connected, an
  assistant is told to ask, not to pick.
- `Broker-Connections` shows, for each of your accounts, whether trading is
  switched on.

## Your plan

Looking something up (market data, a broker read, a web search) and placing an
order use one request of your plan. Working on your own setups (workflows,
alerts, plays, previews) does not. `Subscription-Status` shows how many
requests you have used and how many are left.

When the month's requests are used up, the tool says so. An assistant should
tell you, and not keep trying.

## What is kept

- What an answer contains is what was asked for. Answers do not carry
  passwords, access tokens, email addresses or internal details.
- Your broker sign-in is held by the brokerage connection service you used on
  the dashboard. Atlas and your assistant never see it.
- The full account of what Atlas collects and why:
  https://www.mind-vest.io/privacy

## Reporting a problem

- A security problem: open a private security advisory on this repository, or
  write to accesspoint@finmanagerai.com.
- Something not working: open an issue here with the steps. Never include your
  access key.
