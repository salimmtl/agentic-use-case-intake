---
name: assess-agentic-use-case
description: Recommends the best Microsoft agentic tool and an alternative, estimates the Copilot Credit band, and scores complexity, confidence, value and feasibility for a confirmed agentic use case idea.
---
<!-- bic:source=blank -->
# Assess an agentic use case

Use after the intake summary is confirmed and before submitting. Produce every field needed by the "Submit agentic use case" business skill.

## Steps
1. Apply the **tool selection rubric** below in order. Pick one recommended tool and one alternative, stating whether the alternative is simpler or more capable.
2. Apply the **credit estimation rubric** below to the recommended tool. Compute users × conversations × credits per conversation, apply the licence adjustment, and choose the band.
3. Set complexity, confidence, value score (1–5), feasibility score (1–5) and priority score (value × feasibility).
4. Write the rationale as 3–5 bullets in business language that echo the user's own words. The last bullet says what would change the recommendation.
5. Write credit drivers (2–4 bullets with the arithmetic), always ending with "Indicative only. Set a per-agent credit cap and validate with a pilot."
6. List assumptions and open questions (every "Not sure" answer becomes an assumption).
7. Present the result to the user:
   - **Recommended:** the tool, plus one line on why.
   - **Alternative:** the tool, and why it's simpler or more capable.
   - **Credit band:** the band and ≈ monthly credits, plus the top drivers.
   - **Complexity and confidence.**
   - **Open questions**, if any.
   Then ask whether to submit.

Use rubric version `2026.09-v1` when saving.


# Tool selection rubric

Rubric version: **2026.09-v1**. Source: the "Which agentic tool should I use?" guide (Microsoft Learn guidance, July–August 2026). Microsoft Scout is intentionally out of scope.

Use this rubric to recommend **one primary tool** and **one alternative** for an agentic use case. Always explain the choice in plain business language.

## The seven options

| Value | Tool | Pick it when… | Typical examples |
|---|---|---|---|
| 726410000 | **Microsoft 365 Copilot** | A person wants help in the flow of their own work: Q&A, drafting, summarizing or analysis inside Word, Excel, PowerPoint, Outlook or Teams. Nothing needs to be built. | Meeting recap with owners; explaining a variance in a workbook; drafting a reply |
| 726410001 | **Copilot Cowork** | One person wants to delegate a long, multi-step outcome across Microsoft 365 and get back a finished artifact or completed action. | Quarterly business review deck from email, notes and files; overnight competitive brief; clearing an inbox backlog with drafted replies |
| 726410002 | **Agent Builder (declarative agent)** | A focused, reusable **answers-only** helper for employees with a stable, narrow scope. Its knowledge comes from instructions, the public web, or SharePoint, OneDrive and connectors. It takes no actions. | New-hire onboarding buddy; expense and travel policy Q&A; brand voice checker |
| 726410003 | **Copilot Studio – Standard harness** | The agent must **take actions** (connectors, flows, APIs, MCP) or follow a **structured, predictable** process. It needs consistent answers, governance, or channels beyond Microsoft 365, such as a website or external users. | IT help desk that resets passwords and raises tickets; leave-request bot in Teams; FAQ and guided support on a public website |
| 726410004 | **Copilot Studio – GitHub Copilot harness** | The process is **reasoning-heavy**: it varies case by case, handles exceptions, is **document-intensive**, and orchestrates several tools. The path can't be mapped out up front. | Drafting an RFP response from past proposals and pricing; invoice and contract exception handling; vendor due-diligence review that outputs a summary deck |
| 726410005 | **Microsoft Foundry** | A **custom agent product or platform**: embedded in the customer's own product at scale, multi-agent pipelines, custom models, special protocols, strict network isolation, or offline use. Needs pro-developer skills. | Customer-facing support agent inside their product; multi-agent claims intake → adjudication → payout; offline field assistant |
| 726410006 | **No agent needed – Power Automate / workflow** | The steps are fully deterministic, triggered by an event or schedule, and need no language understanding or judgment. | Copy attachments to SharePoint and notify a channel; nightly data sync; approval routing with fixed rules |

## Decision flow (apply in order; stop at the first clear match)

1. **Is an agent needed at all?** If there is no conversation, no language understanding and no judgment, and the steps are always the same, recommend **Power Automate / workflow**.
2. **Personal productivity, nothing to build?** If an individual wants assistance inside Office apps with their own work, recommend **Microsoft 365 Copilot**.
3. **Personal delegation of a long outcome?** If one person hands off a multi-step task across Microsoft 365 and expects a finished deliverable, recommend **Copilot Cowork**.
4. **Answers only, internal, narrow scope?** If the agent only answers questions for employees from documents, SharePoint or the web and takes no actions, recommend **Agent Builder**.
5. **Building a product or platform?** If the agent is embedded in the customer's own product at scale, is a multi-agent pipeline, needs custom models or protocols, or needs VNet or offline operation, recommend **Microsoft Foundry**. This applies even if it takes actions or serves external users.
6. **Reasoning-heavy with exceptions?** If the process varies a lot case by case, is document-heavy, involves several tools with detours and retries, or needs multi-step judgment, recommend **Copilot Studio – GitHub Copilot harness**. This applies even if it takes actions in systems.
7. **Takes actions or follows a predictable process?** If the agent calls systems, runs workflows, needs consistent guided steps, or is published to a website or external users, and none of steps 5–6 matched, recommend **Copilot Studio – Standard harness**. This is also the default when the agent needs more than Agent Builder offers but nothing points to GHCP or Foundry.

### Mapping intake answers to the flow

| Intake answer | Pushes towards |
|---|---|
| What it must do = *Answer questions* only | Agent Builder (internal) · Standard (external) |
| What it must do includes *Take actions in systems* | Standard · GHCP if the process varies a lot |
| What it must do includes *Run on its own when something happens* | Standard (autonomous trigger) · Power Automate if no judgment is needed |
| What it must do includes *Work through multi-step tasks with judgment* | GHCP · Cowork if it's personal |
| Predictability = *Same steps every time* | Standard · Power Automate |
| Predictability = *Varies a lot case by case* | GHCP |
| Document heavy = Yes | GHCP (sandbox, native Office and PDF work) |
| Audience = External or Both | Standard (website channel) · Foundry if product-scale or custom UX |
| Usage channel = Our own app or portal, and users are more than 5,000 | Foundry (or Standard with a web channel if the logic is simple) |
| Data sources = Public web only, internal | Agent Builder (free) |
| Sensitivity = Regulated | Flag governance. Foundry if VNet or isolation is required. |

### Choosing the alternative
The alternative is the **next-best fit** on the flow. It is usually one step simpler (cheaper, faster to build) or one step more capable (handles more variation). Say which direction it goes and why, for example: "Alternative: Standard harness. Cheaper and more predictable if you can map the main paths up front."

## Complexity (sams_complexity)
- **Low**: answers only, 0–1 systems, internal, predictable.
- **Medium**: 1–2 systems with actions, or some exceptions, or external audience.
- **High**: 3+ systems, write access to business systems, varies a lot, regulated data, or product-scale.

## Scores
- **Value score (1–5)** comes from reach and frequency, adjusted by hours saved: 1 = few users occasionally · 3 = hundreds of users weekly, or clear time savings · 5 = thousands of users daily, or major time savings.
- **Feasibility score (1–5)** is the inverse of complexity, adjusted for data readiness and known connectors: 5 = low complexity and known connectors · 1 = high complexity and unknown systems.
- **Priority score** = value × feasibility (1–25).

## Confidence (sams_confidence)
- **High**: all profile questions answered, and exactly one tool clearly matches.
- **Medium**: 1–2 answers were "Not sure", or two tools are close.
- **Low**: several unknowns, or a vague idea. Always list the open questions in *Assumptions and Open Questions*.

## Rationale style
Give 3–5 short bullets in business language. Refer to the user's own words. Avoid jargon; if a technical term is unavoidable, explain it in brackets. End with one bullet on what would change the recommendation.


# Credit estimation rubric

Rubric version: **2026.09-v1**. Source: the "Copilot Studio & Agent Builder – What consumes Copilot Credits?" explainer (Microsoft Learn and Microsoft Licensing news, August 2026).

Estimates are **indicative planning bands, not quotes**. Always say so, and point to the Microsoft Copilot Studio Licensing Guide for current terms.

## Formula

```
monthly credits ≈ users × conversations per user per month × credits per conversation
```

### Users (from *Number of Users*)
| Answer | Planning value |
|---|---|
| Fewer than 50 | 25 |
| 50 to 500 | 200 |
| 500 to 5,000 | 2,000 |
| More than 5,000 | 10,000 |
| Not sure | 200 (flag as an assumption) |

### Conversations per user per month (from *Usage Frequency*)
| Answer | Planning value |
|---|---|
| Occasionally | 2 |
| Weekly | 4 |
| Daily | 20 |
| Many times a day | 60 |
| Not sure | 4 (flag as an assumption) |

For **autonomous agents** (runs on its own when something happens), estimate **runs per month** instead of conversations and state the assumption.

### Credits per conversation, by recommended tool

Reference rates (Standard harness):
- Classic answer: 1
- Generative answer: 2
- Tenant graph grounding: +10 per message
- Agent action or connector call: 5
- Agent flow: 13 per 100 actions
- Prompt tools: basic 0.1, standard 1.5 or premium 10 per 1K tokens
- Content processing: 8 per page

| Tool | Planning credits per conversation | Notes |
|---|---|---|
| Microsoft 365 Copilot | **0** | Covered by the per-user Microsoft 365 Copilot licence. Band = Included. |
| Copilot Cowork | **Usage-based** | Requires Microsoft 365 Copilot plus usage-based Cowork billing. Use 20 per task as a planning value and flag it. |
| Agent Builder – web or instructions only | **0** | Free for every Copilot Chat user. |
| Agent Builder – Microsoft 365 data | **0 if licensed**, otherwise **≈12 per message × 3 messages = 36** | Included with a Microsoft 365 Copilot licence; unlicensed users are metered. |
| Copilot Studio – Standard (answers) | **6** (3 generative answers) · **36** with tenant graph grounding | |
| Copilot Studio – Standard (actions) | **20** (3 generative answers + 2 actions + one flow of about 10 actions) | |
| Copilot Studio – Standard (autonomous run) | **25 per run** (about 4 agent actions + flow) | Autonomous triggers are always billed. |
| Copilot Studio – GitHub Copilot harness | **50** typical · **150** if document-heavy | Usage-based from the first build turn, for **every** user, licensed or not. Build, test and evaluation also consume credits. Planning assumption: tune from real telemetry. |
| Microsoft Foundry | **0 Copilot Credits** | Azure consumption (models, tools, hosting) instead. Band = Included, and **state that Azure costs apply**. |
| Power Automate / workflow | **0 Copilot Credits** | Power Automate licensing instead. Band = Included, and state it. |

### Licence adjustment (Standard harness only)
If **Users have M365 Copilot = Yes, all users**, AND **Audience = Internal**, AND **Usage channel = Microsoft Teams or Microsoft 365 Copilot**, then most Standard-harness operations are **included (0 credits)** for those users. The exceptions are autonomous triggers other than "When an agent calls the flow", computer use, and bring-your-own model. These are still billed.
- **Some users** licensed: apply the formula to the unlicensed share only. Assume 50% unless the user says otherwise.
- The GitHub Copilot harness is **never** licence-included.

## Bands

| Band | Value | Monthly credits | Plain-language meaning |
|---|---|---|---|
| Included (about 0) | 726410000 | ≈ 0 | Covered by licences, or no Copilot Credits used (other costs may apply) |
| Low | 726410001 | < 25,000 | About one Copilot Credit pack per month or less |
| Medium | 726410002 | 25,000 – 250,000 | Needs budget planning and a per-agent cap |
| High | 726410003 | > 250,000 | Significant spend: validate with a pilot and a capacity plan |

Customers can tune these thresholds to their own capacity and prepaid packs.

## What to write
- **Estimated Monthly Credits**: the rounded number from the formula (0 when included).
- **Credit Drivers**: 2–4 bullets naming the assumptions (users, frequency, credits per conversation, licence effect). Example: "200 users × 20 conversations × 20 credits ≈ 80,000/month (Medium). Users aren't Copilot-licensed, so standard rates apply. Mostly generative answers plus 2 ticket actions per conversation."
- Always add: "Indicative only. Set a per-agent credit cap and validate with a pilot."

## Worked examples
1. HR policy Q&A, internal, 2,000 users, weekly, SharePoint, no licences → Agent Builder with M365 data: 2,000 × 4 × 36 = 288,000 → **High**. The alternative is to license users (→ Included) or ground on curated files in Copilot Studio Standard (2,000 × 4 × 6 = 48,000 → Medium).
2. IT help desk, internal, 500 users, daily, Teams, all licensed → Standard: **Included** (licensed users in an M365 channel).
3. Invoice exception handling, 30 users, daily, document-heavy → GHCP: 25 × 20 × 150 = 75,000 → **Medium**.
4. Public website FAQ, external, more than 5,000 users, occasionally → Standard: 10,000 × 2 × 6 = 120,000 → **Medium**.
