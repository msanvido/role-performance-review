---
name: role-performance-review
description: >
  Self-assessment tool: evaluates the user's own performance in a specific role by pulling evidence
  from their data sources (Granola, Airtable, Gmail, Slack, Notion, GitHub, Google Drive, LinkedIn,
  Substack, Twitter, and more), then synthesizing it into a structured report covering what worked,
  what didn't, how their guidance evolved, behavioral patterns, and concrete lessons learned.

  For SELF-ASSESSMENT ONLY — do not use to evaluate or grade other people.

  Trigger when the user asks to evaluate, assess, or reflect on their own performance or decisions:
  "evaluate me as a Y", "how have I been doing as a Z", "review my decisions", "what can I learn
  from my past interactions", "give me a performance review of myself", "assess my track record",
  "what am I doing well and where am I falling short", or any request for a structured retrospective
  on their own work. Also trigger when the user asks to repeat a previous self-evaluation.
---

# Performance Review Skill (Self-Assessment)

This skill helps the user reflect on their own performance in a specific role by gathering evidence
from the sources they specify, then synthesizing it into a structured, cited self-assessment report.
It is designed for personal use only — not for evaluating or judging other people.

---

## Step 1 — Clarify the Request

Before doing any data gathering, use the `AskUserQuestion` tool to collect what you need in one shot.
The subject is always the user themselves. Ask for:

1. **Role** — the role to evaluate themselves in (e.g. investor, engineer, sales rep, founder, manager)
2. **Time window** — how far back to look (e.g. "last 6 months", "all time", "since January 2025")
3. **Sources** — which of their own data sources to pull from. Present the full list and let them pick:

   - **Granola** — their meeting notes and transcripts (full access since it's their account)
   - **Airtable** — structured records they own or contribute to (CRM, portfolio, pipeline, etc.)
   - **Gmail** — emails they sent or received
   - **Google Calendar** — their meeting attendance and patterns
   - **Slack** — their messages and threads
   - **Notion** — docs and databases they've authored or contributed to
   - **Google Drive** — documents they've written or co-authored
   - **GitHub** — their commits, PRs, code reviews (via web search for public repos)
   - **LinkedIn** — their posts and articles (via web search)
   - **Substack** — their published articles (via web fetch)
   - **Twitter/X** — their posts and threads (via web search)
   - **Other** — any other source they name

4. **Evaluation dimensions** — use the default 5-part framework below, or ask if they want custom ones.

If the conversation already answers some of these (e.g. the user says "evaluate me as an investor
using Granola and Airtable"), pre-fill what's already clear and only ask for the rest.

---

## Step 2 — Detect Available Sources

Since this is always a self-assessment, all connected sources are authenticated as the user —
meaning full access. Check which MCPs are loaded and match each requested source:

| Source | MCP / Method |
|---|---|
| Granola | `query_granola_meetings`, `list_meetings`, `get_meetings` |
| Airtable | `list_bases`, `list_tables_for_base`, `list_records_for_table` |
| Gmail | `gmail_search_messages`, `gmail_read_thread` |
| Google Calendar | `gcal_list_events`, `gcal_get_event` |
| Slack | `slack_search_public_and_private`, `slack_read_channel`, `slack_read_thread` |
| Notion | `notion-search`, `notion-query-data-sources`, `notion-query-meeting-notes` |
| Google Drive | `google_drive_search`, `google_drive_fetch` |
| GitHub | Use `WebSearch` for public repos; no direct MCP |
| LinkedIn | Use `WebSearch` for their public posts and profile |
| Substack | Use `WebFetch` to retrieve article URLs directly |
| Twitter/X | Use `WebSearch` with site:x.com or site:twitter.com |

If a requested source has no available MCP or web access, tell the user before proceeding.
Don't silently skip sources.

---

## Step 3 — Gather Evidence in Parallel

Fire all source queries at once — don't wait for one to finish before starting another. For each source:

### Granola
Search broadly using multiple queries in parallel, focused on the user's own activity:
- `"decisions interactions outcomes {role}"`
- `"assessment feedback coaching mistakes"`
- `"advice reversed evolved updated position"`
- For **investor and advisor roles**, also run: `"interview scorecard candidate intake evaluation mentoring"`
  to surface candidate and mentee assessment decisions alongside portfolio or advisory work
Run at least 3–4 distinct queries to get broad coverage. Use `list_meetings` with a custom date
range if you need to enumerate all meetings and then fetch specific ones.

### Airtable
1. Use `list_bases` to find the relevant base (look for CRM, portfolio, or team bases)
2. Use `list_tables_for_base` to understand the schema — save the table IDs, you'll need them
3. **For investor/advisor/DRI roles — do this lookup first:**
   - Find the DRI/team members table (often called "DRIs", "Team", or "People")
   - Use `list_records_for_table` on that table to get all DRI records and their IDs
   - Identify the person's record ID (looks like `recXXXXXXXXXXXXXXX`)
   - Then query the Companies table with `list_records_for_table`, passing a `filters` object to
     match the Primary DRI field against the person's record ID. The filter format is:
     `{"operands": [{"operator": "=", "operands": ["<dri_field_id>", "<person_record_id>"]}]}`
     Note: if the DRI field is a linked record (multipleRecordLinks), use `contains` instead of `=`
   - This gives you their exact portfolio companies with stage and valuation data
4. Also query: activity logs, opportunity/deal tables, and any interview/evaluation records
5. Filter by the person's name or record ID where possible — don't just browse all records

### Gmail
Search for emails sent by or to the person:
- `from:{email} OR to:{email}` over the time window
- Look for decision emails, feedback, threads with key stakeholders
- Read threads that contain substantive decisions or turning points

### Slack
Search for messages from or about the person:
- `from:{name}` in key channels
- Mentions of their name in decision threads
- Use `slack_read_channel` on channels most relevant to their role

### Notion
- Search for pages authored by or about the person
- Query meeting notes databases for their name
- Look for strategy docs, decision logs, retrospectives they contributed to

### Google Drive
- Search for documents they authored or co-authored
- Look for presentations, memos, proposals

### Web sources (LinkedIn, Substack, Twitter/X, GitHub)
- Use `WebSearch` with targeted queries: `"{name}" site:linkedin.com/posts`, `site:substack.com`,
  `site:x.com`, `site:github.com`
- Fetch the top results for substance

---

## Step 4 — Synthesize the Evidence

Once data is gathered, produce a structured self-assessment using the 6-part framework below.
If the user specified custom dimensions, use those instead — but always include citations.

Write in second person ("you decided…", "your pattern here is…") so it reads as direct personal
feedback, not a report about someone. The goal is for the person to immediately recognize
themselves in it.

**Adapt each section to the role** using the role-specific guidance table at the bottom of this
skill. Not every role has "decisions" — an engineer has architectural choices, a manager has
people calls, a researcher has methodological bets. Use language that fits.

**How to structure evidence (for sections 1 and 2 especially):** For each item you surface, frame
it as a brief narrative — what was the context and what were the stakes, what the person was trying
to achieve, what they actually did, and what resulted. This makes the evidence feel grounded and
specific rather than like a list of events. Keep each item concise; depth comes from the synthesis
across items, not from retelling every detail of a single meeting.

---

### 6-Part Evaluation Framework

#### 1. What Worked
Surface the bets, choices, actions, or contributions that held up well — adapted to the role
(investments, architecture calls, deals won, hires made, findings that held, etc.).

For each: briefly set the context and what was at stake, what you were trying to achieve, what you
actually did, and what the outcome was. Then draw a short inference: what does this reveal about
your judgment or approach that's worth keeping? Avoid recapping every win — focus on the ones that
reveal something meaningful about *why* you were effective.

#### 2. What Didn't Work
Surface the misses, failures, or choices that went wrong or are trending poorly — same role-adapted
framing as section 1.

Same structure: context and stakes, the intent, the action taken, the result. Then be honest about
what early signals were present but not weighted correctly. Don't jump to lessons yet — account for
the actual cost of the miss before reframing it. A wound-down investment, a churned account, a
technical decision that created six months of rework: name it plainly before explaining it.

#### 3. What Evolved or Changed
Identify positions, approaches, or guidance that shifted meaningfully over the review period:
- What was the original stance or approach, and what did it become?
- What drove the change — new evidence, pressure from others, lived experience, a specific event?
- Was it healthy updating (the evidence changed, so you changed) or reactive inconsistency
  (you reversed because things got uncomfortable)?
- What does the pattern of change — or notable absence of change — say about how you process
  feedback and update your models?

#### 4. Patterns in Style and Approach
Zoom out from individual events and characterize how you show up across contexts. Two lenses are
useful here, used together:

**Recurring strengths and blind spots** — Where do you consistently add value? What's your actual
edge? What do you systematically miss or underweight? How do you behave under pressure, ambiguity,
or pushback? What mental models do you reach for, and where do those fail you?

**Depth of operation relative to the role** — Are you operating at the right level for your
experience and seniority? Some areas to probe: Do you tend to execute within defined constraints,
or do you initiate and shape direction? Do you advise and enable others, or primarily do the work
yourself? Where are you punching above your expected level — taking on complexity and influence
that creates outsized impact? Where are you operating *below* it — defaulting to execution when
the situation calls for strategy, or deferring when you should be initiating? This isn't about
whether you're "senior enough" — it's about whether your actual operating level matches what the
role and context demand.

#### 5. Key Lessons
The 3–5 most important takeaways from the evidence — framed as direct, personal insights for the
person themselves. Each one should be grounded in a specific pattern from the data, not generic
career advice ("you tend to over-index on technical quality at the expense of founder psychology"
rather than "be more holistic"). Write in second person so they land as genuine feedback.

Focus on the lessons that are most transferable — the ones that will keep showing up if left
unaddressed. Don't list every observation; pick the ones with the highest signal.

#### 6. Suggested Improvements
Concrete, bounded changes the person could make — things to do differently starting in the next
week, month, or quarter. These should be more specific than key lessons and answerable: not "improve
your sourcing" but "over the next three intake cycles, run the portfolio DRI lookup as a mandatory
step before each interview, and log whether it changed your initial read."

For each improvement: name the specific change, connect it to the pattern it addresses, describe
what success looks like (how will you know it's working?), and suggest a realistic timeframe or
context for trying it. Aim for 3–5 improvements. The best ones are small enough to actually
attempt and specific enough to actually evaluate.

---

## Output Format

Write the evaluation in **flowing prose**, not bullet points. Use section headers for each of the
5 parts. End with a **Sources** section.

**Citations are non-negotiable.** Every substantive claim — a specific decision, an outcome, a
quote, a behavioral observation — must be immediately followed by an inline link to its source.
Use markdown link format: `[[meeting title or short description]](url)` for Granola notes,
or `[Airtable: Company Name]` for Airtable records. If a claim has no citable source, either
drop the claim or explicitly flag it as inference (`[inference from pattern across multiple sources]`).
Never make a specific factual claim without a citation attached to it in the same sentence.

The tone should be honest, direct, and constructive — like a trusted advisor writing an assessment
for someone they respect and want to see succeed. Don't soften findings to be nice; don't be harsh
for the sake of it. The goal is clarity and usefulness.

Aim for depth over breadth. Five well-evidenced, specific observations are worth more than fifteen
vague ones. If the evidence is thin on a dimension, say so rather than padding.

**Length**: typically 1,000–2,500 words for the main body, depending on evidence volume.

---

## Role-Specific Guidance

Use this table to translate each framework section into language that fits the role naturally.
The section numbers (1–6) are fixed; the framing and focus areas shift by role.

For all roles, sections 1 and 2 should follow the same narrative structure: context and stakes →
intent → action → result → inference. The Patterns section should always include both the
recurring strengths/blind-spots lens and the depth-of-operation lens. Suggested Improvements
should always be specific, bounded, and include a "how will you know it worked?" check.

### Investor
| Section | What to surface |
|---|---|
| **What Worked** | Investments that marked up, exited, or are tracking well. Candidate or intake picks that proved correct. Founder advice that changed outcomes. For each: what was the thesis at the time, what did you do, what resulted? |
| **What Didn't Work** | Bets that wound down or pivoted away from the original thesis. Candidates admitted who underperformed. Passes on companies that later succeeded. Advice that had to be reversed. What were the early signals you underweighted? |
| **What Evolved** | Thesis updates; changes to your evaluation criteria or scorecard; fundraising advice that shifted; how your mentoring and coaching style changed with experience |
| **Patterns** | Assessment framework strengths/gaps; how you source vs. evaluate; depth and consistency of support to founders; where you operate as a strategic advisor vs. where you're still in execution mode |
| **Key Lessons** | Grounded in specific investment patterns — not "be more disciplined" but "your read on founder psychology is weaker than your technical assessment, and it's cost you in these cases" |
| **Suggested Improvements** | E.g. "Run the portfolio DRI lookup as a required step before every candidate interview for the next two intake cycles, and check whether it changed your initial view." |

### Software Engineer
| Section | What to surface |
|---|---|
| **What Worked** | Architecture choices that scaled or aged well. Technical calls that unblocked the team or accelerated delivery. PRs or designs that are still in production and holding up. |
| **What Didn't Work** | Tech debt created by shortcuts. Over-engineering that slowed delivery. Calls that led to incidents, rewrites, or significant rework. What was the context and what did it cost? |
| **What Evolved** | Changes in how you approach code review, testing strategy, system design, or cross-team coordination — and what drove those changes |
| **Patterns** | Collaboration style; how you handle technical ambiguity; thoroughness vs. speed tradeoffs; whether you're shaping design decisions or primarily executing others' specs |
| **Key Lessons** | Grounded in specific technical patterns — not "write better tests" but "you tend to optimize for elegance over operability, and it's shown up in these incidents" |
| **Suggested Improvements** | E.g. "For the next three system design proposals, add an explicit 'failure modes and operability' section before sign-off — check whether it surfaces concerns that weren't raised in review." |

### Sales / BD
| Section | What to surface |
|---|---|
| **What Worked** | Deals won and why — what was the context, the strategy, the action, the result? Relationships built that opened future pipeline. Pricing or proposal calls that held under negotiation. |
| **What Didn't Work** | Deals lost at late stage. Accounts that churned shortly after close. Forecasting misses. What signals were present that you explained away? |
| **What Evolved** | Shifts in how you qualify prospects, structure proposals, or handle objections — and whether those shifts came from evidence or habit |
| **Patterns** | Prospecting consistency; how you manage a pipeline under pressure; where you close independently vs. where you need support |
| **Key Lessons** | Grounded in deal-level patterns — not "qualify harder" but "you repeatedly advance deals where the economic buyer wasn't engaged, and it costs you at the final stage" |
| **Suggested Improvements** | E.g. "In the next five discovery calls, explicitly ask to meet the budget owner within the first two meetings and track whether it changes win rate." |

### Founder / Operator
| Section | What to surface |
|---|---|
| **What Worked** | Pivots, hires, or product bets that paid off. Capital allocation decisions that proved right. Strategic calls that the team rallied around and executed well. |
| **What Didn't Work** | Hires that didn't work out and why. Product directions abandoned after significant investment. Capital or time misallocated. What was the cost and what was knowable earlier? |
| **What Evolved** | How your strategy or market thesis changed. Team composition philosophy shifts. Changes in how you communicate direction or handle uncertainty with the team. |
| **Patterns** | Decision-making speed and reversibility; communication under pressure; where you're setting direction vs. where you're still doing the work yourself |
| **Key Lessons** | Grounded in operator patterns — not "delegate more" but "you hold onto hiring decisions too long when a role is ambiguous, and it's created gaps in these cases" |
| **Suggested Improvements** | E.g. "Set a 4-week decision deadline for any open role that's been in process more than 8 weeks — either close it or formally redefine the need." |

### Manager / People Lead
| Section | What to surface |
|---|---|
| **What Worked** | Team members who grew meaningfully under your tenure. Culture or process changes that stuck. Cross-functional wins you enabled. Difficult conversations that improved performance. |
| **What Didn't Work** | Underperformance situations that dragged on too long. Retention misses you didn't see coming. Promotion or leveling decisions that backfired. What would you do differently? |
| **What Evolved** | How your management style adapted to team growth, reorgs, or a specific stretch period. Changes to how you give feedback or run 1:1s. |
| **Patterns** | Feedback quality and frequency; how you handle conflict or underperformance; where you coach vs. where you fix things yourself; whether your team operates autonomously or depends on you for decisions |
| **Key Lessons** | Grounded in people patterns — not "give feedback earlier" but "you consistently address performance issues at the 3-month mark instead of the 6-week mark, and it's made the conversations harder" |
| **Suggested Improvements** | E.g. "For every new report, schedule a 6-week explicit check-in on role fit and blockers — not a status update — and track whether early issues surface sooner." |

### Researcher / Analyst
| Section | What to surface |
|---|---|
| **What Worked** | Findings that held up under scrutiny or were acted on. Methods that proved robust across contexts. Analyses that changed decisions. Communication of uncertainty that was well-calibrated. |
| **What Didn't Work** | Analyses that had to be revised after publication or delivery. Conclusions that didn't generalize. Recommendations that weren't acted on and why. |
| **What Evolved** | Methodology updates; changes in how you scope work or communicate confidence; how you've adapted to stakeholder feedback over time |
| **Patterns** | Rigor vs. speed tradeoffs; how you handle ambiguous or incomplete data; whether you're shaping the research agenda or primarily responding to requests |
| **Key Lessons** | Grounded in research patterns — not "communicate better" but "you consistently underestimate how much context stakeholders need to act on a finding, and it's shown up in these cases" |
| **Suggested Improvements** | E.g. "For the next three deliverables, include a one-paragraph 'what this means for your decision' section written for the primary stakeholder — check whether uptake improves." |

### Advisor / Mentor
This role covers anyone who advises, coaches, or mentors others — founders, executives, individual
contributors, students, or teams — without holding formal authority over them. The value comes
from the quality of the guidance, the trust built, and the outcomes for the people being advised.

| Section | What to surface |
|---|---|
| **What Worked** | Advice that the advisee acted on and that led to a better outcome. Introductions or referrals that opened real doors. Moments where you reframed a problem in a way that unblocked someone. Candidate or intake assessments that aged well. |
| **What Didn't Work** | Guidance that was ignored and in hindsight was right — did you land it effectively? Advice that was followed but led somewhere bad — what were you missing? Relationships where trust eroded or engagement dropped off. Candidates or mentees you backed who didn't work out. |
| **What Evolved** | How your coaching or mentoring style has changed — more directive vs. more Socratic, more hands-on vs. more light-touch. Changes to who you agree to advise and why. Shifts in how you give hard feedback. |
| **Patterns** | How quickly you build trust with new advisees; whether you adapt your style to the person or apply a consistent approach; where you tend to over-advise (doing the thinking for them) vs. under-advise (too hands-off); how you handle it when someone ignores your guidance; whether you're operating as a sounding board, a coach, a connector, or a domain expert — and whether that matches what each relationship actually needs |
| **Key Lessons** | Grounded in specific advisory patterns — not "be more available" but "you give your best advice in early-stage conversations and disengage as people hit execution challenges, which is exactly when your pattern-matching would be most useful" |
| **Suggested Improvements** | E.g. "For the next three active advisory relationships, schedule a 90-day check-in specifically focused on whether your guidance has been useful and what they wish you'd said differently — track whether it surfaces gaps you weren't aware of." |

For any role not listed here: use the same structure, and ask yourself what the key choices and
contributions look like in this role to fill in sections 1 and 2.
