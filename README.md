# role-performance-review

A self-assessment skill for [Claude Cowork](https://www.anthropic.com) that evaluates your own performance in a specific role by pulling evidence from your connected data sources and synthesizing it into a structured, cited report.

## What It Does

Given a role (investor, engineer, founder, manager, etc.) and a time window, this skill:

1. Asks which of your data sources to pull from — Granola, Airtable, Gmail, Slack, Notion, Google Drive, GitHub, LinkedIn, Substack, Twitter/X, and more
2. Queries all selected sources in parallel for evidence of decisions, actions, and outcomes
3. Synthesizes everything into a 6-part self-assessment report with inline citations

## The 6-Part Framework

| # | Section | What it covers |
|---|---|---|
| 1 | **What Worked** | Bets, choices, and contributions that held up well — with context, intent, action, and outcome |
| 2 | **What Didn't Work** | Misses and failures — named plainly before being explained |
| 3 | **What Evolved or Changed** | Positions or approaches that shifted, and whether the updates were healthy or reactive |
| 4 | **Patterns in Style and Approach** | Recurring strengths, blind spots, and depth of operation relative to the role |
| 5 | **Key Lessons** | 3–5 high-signal takeaways grounded in specific patterns from the data |
| 6 | **Suggested Improvements** | Concrete, bounded changes with a "how will you know it worked?" check |

The framework draws inspiration from STAR (Situation → Task → Action → Result), SMART Goals, and SFIA (Skills Framework for the Information Age) without being rigid about any of them.

## Supported Roles

The skill includes role-specific guidance for:
- **Investor** — portfolio bets, candidate intake, founder coaching
- **Software Engineer** — architecture calls, code quality, technical leadership
- **Sales / BD** — pipeline, deal outcomes, relationship building
- **Founder / Operator** — strategy, hires, capital allocation
- **Manager / People Lead** — team growth, feedback, retention
- **Researcher / Analyst** — findings, methods, stakeholder communication
- **Advisor / Mentor** — guidance quality, trust building, coaching style

Any role not listed is also supported — the skill adapts the framework to fit.

## Important Constraints

**Self-assessment only.** This skill is designed to help you reflect on your own performance. It will not evaluate or grade other people. All data queries are scoped to the authenticated user's own records and accounts.

## Data Sources

The skill can pull from any combination of:

| Source | Access Method |
|---|---|
| Granola | Native MCP — meeting notes and transcripts |
| Airtable | Native MCP — CRM, portfolio, pipeline records |
| Gmail | Native MCP — emails sent and received |
| Google Calendar | Native MCP — meeting patterns and attendance |
| Slack | Native MCP — messages and threads |
| Notion | Native MCP — docs and databases |
| Google Drive | Native MCP — documents and presentations |
| GitHub | Web search — public repos, commits, PRs |
| LinkedIn | Web search — posts and profile |
| Substack | Web fetch — published articles |
| Twitter/X | Web search — posts and threads |

## How to Use

Install the `.skill` file in Claude Cowork, then trigger it by saying things like:

- "Evaluate me as an investor over the last 6 months"
- "Give me a performance review of myself as an engineer"
- "How have I been doing as a manager this year?"
- "Review my decisions from the past quarter"
- "What can I learn from my past interactions?"

The skill will ask for any missing details (role, time window, sources) before starting.

## Output Format

The assessment is written in flowing prose in second person ("you decided…", "your pattern here is…") so it reads as direct personal feedback. Every substantive claim is cited inline to its source. Typical length is 1,000–2,500 words depending on evidence volume.

## Installation

Download `role-performance-review.skill` and install it in Claude Cowork via **Settings → Plugins → Install from file**.

## License

MIT — see [LICENSE](LICENSE)
