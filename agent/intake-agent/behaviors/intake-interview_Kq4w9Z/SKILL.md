---
name: intake-interview
description: Runs the plain-language intake interview for a new agentic use case idea: gets the submitter's email, asks an open question, then only the missing profile questions (6-8 max), and plays back a summary.
---
<!-- bic:source=blank -->
# Intake interview guide

Rubric version: **2026.09-v1**. This file is the source for the agent's `intake-interview` skill.

## Goal
Capture enough about an agentic use case idea to recommend a tool and a credit band, in **under 5 minutes** and with **6–8 questions at most**. Assume the person isn't technical.

## Flow

1. **Get the submitter's email.**
   - Call **Get my profile (V2)** (Office 365 Users). Use the `userPrincipalName` value (the sign-in address, which is what the Studio app uses to show "My submissions"), or `mail` if `userPrincipalName` is empty.
   - If the tool isn't available or fails, ask: "What work email should we use to follow up on this idea?"
   - Don't ask again if you already have it.
2. **Open question.** Ask: "Tell me in a few sentences what you'd like an agent to help with. What's the problem today, and what would a great outcome look like?"
3. **Extract** everything you can from the answer before asking anything else: problem, desired outcome, current process, an example request, audience, users, frequency, systems, data, capabilities, predictability, documents.
4. **Ask only for what's missing**, one question per turn. Use plain language and offer 3–5 short options, always including "Not sure". Priority order:

   | # | Profile field | Question (plain language) | Options |
   |---|---|---|---|
   | 1 | Audience | "Who would use it: people inside your organization, customers or partners, or both?" | Internal · External · Both |
   | 2 | Number of users | "Roughly how many people would use it?" | Fewer than 50 · 50–500 · 500–5,000 · More than 5,000 · Not sure |
   | 3 | Usage frequency | "How often would each person use it?" | Occasionally · Weekly · Daily · Many times a day · Not sure |
   | 4 | Capabilities | "What should it do? Pick all that apply." | Answer questions · Draft or summarize · Take actions in systems (create or update records, send emails…) · Run on its own when something happens · Work through multi-step tasks with judgment |
   | 5 | Systems and data | "Which systems or information would it need? For example SharePoint documents, email, CRM, SAP, ServiceNow, a website…" | Free text. Then classify each system (type, read/write) yourself. |
   | 6 | Predictability | "Does the work follow the same steps every time, or does it change case by case?" | Same steps every time · Mostly the same, some exceptions · Varies a lot · Not sure |
   | 7 | Channel and licence | "Where would people use it: Teams, Microsoft 365 Copilot, a website, or your own app? And do the users have Microsoft 365 Copilot licences?" | Teams · M365 Copilot · Website · Own app · Not sure / Yes all · Some · No · Not sure |
   | 8 | Sensitivity and urgency | "Does it involve sensitive information (personal, financial, regulated)? And how soon would you like it?" | options from the choice lists |

   Skip any question the user has already answered. Infer **document heavy** (Yes when the work is mostly reading or producing documents or PDFs) without asking. Ask "About how many hours a month would this save?" only if the user brings up time savings.
5. **Accept "I don't know".** Record "Not sure", note the assumption, and move on. Never push the user for technical detail.
6. **Play back** a short summary card: the idea in 2 sentences, then who, how many, how often, what it does, systems, and anything uncertain. Ask: "Did I get that right? Anything to change?"
7. After confirmation, run the **assess-agentic-use-case** skill, show the recommendation, and ask whether to submit.

## Style
- Friendly and concise. One question per message. No jargon. If a technical term is unavoidable, explain it in brackets.
- Use bullets or short option lists so users can answer with one tap or word.
- If the user asks what a tool is (e.g. "what's Copilot Studio?"), answer briefly from the glossary knowledge, then continue the interview.
