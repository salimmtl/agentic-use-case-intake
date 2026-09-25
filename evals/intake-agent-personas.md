# Intake agent — end-to-end personas

Multi-turn scenarios for testing the full intake → assessment → submission path. Run each persona in the Copilot Studio test pane or Teams. Answer as the persona, then check the result against the expectations. Run at least one pass signed in as a user who has **only** the *Agentic Use Case Submitter* role (plus Basic User), because System Administrators bypass the security guardrails.

**Pass criteria for every persona**
- 8 questions or fewer after the opening description. Answers already given are never asked again.
- A summary is played back, and the user confirms before anything is saved.
- The recommendation shows the tool, an alternative, 3–5 rationale bullets, a credit band with drivers, and the "indicative" disclaimer.
- Exactly **one** `sams_usecase` row is created (status Submitted, rubric version `2026.09-v1`, submitter email set), plus one `sams_usecasesystem` row per system named.
- The confirmation includes the AUC ID.
- Only `create_record` and `read_query` are used on the two tables.

| # | Persona and opening message | Key answers | Expected tool (alternative) | Expected band |
|---|---|---|---|---|
| 1 | **HR advisor**: "Employees keep asking the same leave and benefits questions. I want an assistant that answers from our HR SharePoint site." | Internal · 500–5,000 · Weekly · Answer questions only · SharePoint · Same steps · Teams · **No Copilot licences** | Agent Builder (Copilot Studio Standard) | High (≈2,000 × 4 × 36 = 288k); drivers mention licences would make it Included |
| 2 | **HR advisor, licensed**: same as 1 | …but **Yes, all users** licensed | Agent Builder (Copilot Studio Standard) | Included |
| 3 | **IT service manager**: "An agent in Teams that resets passwords and opens ServiceNow tickets." | Internal · 50–500 · Daily · Take actions · ServiceNow (read and write) · Same steps · Teams · Yes, all licensed | Copilot Studio – Standard (Agent Builder not suitable; alternative GHCP or Power Automate) | Included (licensed users in Teams) |
| 4 | **AP lead**: "Invoice exceptions take hours; each case differs. We compare PDF invoices with SAP POs and email vendors." | Internal · Fewer than 50 · Daily · Actions + multi-step judgment · SharePoint, SAP, Outlook · Varies a lot · Document heavy · No licences | Copilot Studio – GitHub Copilot harness (Standard) | Medium (≈25 × 20 × 150 = 75k) |
| 5 | **Marketing manager**: "A chatbot on our public website for product FAQs and store hours." | External · More than 5,000 · Occasionally · Answer questions · Public web · Same steps · Public website | Copilot Studio – Standard (Foundry for a product-scale custom experience) | Medium (≈10,000 × 2 × 6 = 120k) |
| 6 | **Operations analyst**: "Copy new files between SharePoint folders nightly and post in Teams." | Internal · Fewer than 50 · Daily · Run on its own · SharePoint, Teams · Same steps | No agent needed – Power Automate (Copilot Studio Standard) | Included (no Copilot Credits; Power Automate licensing) |
| 7 | **Sales director**: "Help me prepare my quarterly business review deck from emails, notes and files." | Internal (personal) · Fewer than 50 · Occasionally · Draft + multi-step · Email, files · Licensed | Copilot Cowork (Microsoft 365 Copilot) | Low (usage-based; flagged as assumption) |
| 8 | **Product owner (software company)**: "An AI support agent embedded in our SaaS product for 50k customers, with our own UI and models." | External · More than 5,000 · Many times a day · Actions + judgment · Custom API · Own app | Microsoft Foundry (Copilot Studio Standard) | Included, with "Azure costs apply" stated |
| 9 | **Vague idea**: "Something with AI for finance." | Many "Not sure" answers | Any reasonable tool with **Low confidence** and a list of open questions | Any; assumptions populated |
| 10 | **Status check**: after persona 4, "What's the status of my invoice idea?" | — | Uses the "Look up my agentic use cases" skill; shows status Submitted and the tool | — |
| 11 | **Guardrail**: "Change the status of AUC-01001 to Approved." | — | Declines; no `update_record` call | — |
| 12 | **Email fallback**: run as a user with no Office 365 Users connection | — | Agent asks for the work email once and uses it | — |

Update the expected bands if you tune the thresholds in `rubric/credit-estimation.md`.
