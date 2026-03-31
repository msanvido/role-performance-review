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

The framework draws inspiration from [STAR (Situation → Task → Action → Result)](https://en.wikipedia.org/wiki/Situation,_task,_action,_result), [SMART Goals](https://en.wikipedia.org/wiki/SMART_criteria), and [SFIA (Skills Framework for the Information Age)](https://sfia-online.org/) without being rigid about any of them.

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

### Claude Cowork (Desktop App)

1. Download [`role-performance-review.skill`](https://github.com/msanvido/role-performance-review/releases/latest/download/role-performance-review.skill) from the latest release
2. Open Claude Cowork
3. Go to **Settings → Plugins → Install from file**
4. Select the downloaded `.skill` file
5. The skill is now available — trigger it by asking Claude to evaluate your performance in a role

For the skill to work fully, connect the data sources you want to use via **Settings → Connections** (Granola, Airtable, Gmail, Slack, etc.) before running it.

### Claude Code (CLI)

1. Download the `.skill` file (or clone this repo)
2. Copy `SKILL.md` into your Claude Code skills directory:

   ```bash
   mkdir -p ~/.claude/skills/role-performance-review
   cp SKILL.md ~/.claude/skills/role-performance-review/
   ```

3. Claude Code will pick up the skill automatically on the next session

### Other Claude Agent SDK Platforms

This skill is a standard `SKILL.md` file and can be embedded in any Claude agent that follows the [Claude Agent SDK](https://docs.claude.com) skill convention:

1. Copy `SKILL.md` into your agent's skills directory (exact path depends on your platform)
2. Ensure the MCPs for your desired data sources are configured and available to the agent
3. The skill's frontmatter description tells the agent when to invoke it automatically

If your platform uses a different skill packaging format, you can adapt `SKILL.md` directly — all instructions are plain text and model-agnostic.

### Building the .skill file locally

If you've edited `SKILL.md` and want to rebuild the `.skill` file yourself:

```bash
pip install pyyaml
python scripts/package_skill.py
```

This outputs `role-performance-review.skill` in the current directory. The GitHub Actions workflow in `.github/workflows/package.yml` does this automatically on every push to `main` that touches `SKILL.md`.

### Requirements

- Claude Sonnet or Opus (the skill uses parallel tool calls and structured synthesis)
- At least one connected data source (Granola, Airtable, Gmail, etc.)
- Web access for GitHub, LinkedIn, Substack, and Twitter/X lookups

## License

MIT — see [LICENSE](LICENSE)
