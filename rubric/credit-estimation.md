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
