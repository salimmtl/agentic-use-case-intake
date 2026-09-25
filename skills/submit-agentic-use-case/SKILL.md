---
name: Submit agentic use case
description: Use when an agentic use case idea has been captured, assessed and confirmed by the user, and must be saved to Dataverse. Trigger phrases include "submit my idea", "save this use case", "create the use case" or the user confirming the intake summary. Creates one sams_usecase row and one sams_usecasesystem row per target system, then returns the use case ID (AUC-xxxxx).
---

# Submit agentic use case

Saves a confirmed agentic use case to Dataverse with the Dataverse MCP server.

**Required tools:** Dataverse MCP server `create_record` and `read_query`. Do not use any other write tool. Never call `update_record`, `delete_record`, `create_table`, `update_table` or `delete_table` from this skill.

**Resource:** `choice-values.md` lists every column's logical name, its type, and every choice's integer value. Always take choice values from it. Never guess them.

## Inputs

| Input | Required | Notes |
|---|---|---|
| Title | yes | Short business title written by you, max 200 characters, e.g. "Invoice exception handling assistant" |
| Submitter email | yes | From the user's session or asked from the user. Must look like an email address. |
| Problem statement | yes | The user's own words, lightly cleaned up |
| Desired outcome | yes | |
| Profile answers | recommended | Audience, number of users, frequency, data sources, capabilities, predictability, document heavy, usage channel, M365 Copilot licence, sensitivity, urgency. Use the "Not sure" option when the user doesn't know. |
| Assessment | yes | Recommended tool, alternative tool, rationale, credit band, estimated monthly credits, credit drivers, complexity, confidence, assumptions, value score, feasibility score |
| Target systems | optional | A list of {name, system type, access, known connector} |
| Conversation summary | yes | 5–10 lines summarizing the interview |
| Conversation ID | optional | The conversation identifier, if available |

## Steps

1. **Validate before writing.**
   - Title, submitter email, problem statement, recommended tool and credit band are present.
   - Each choice value exists in `choice-values.md` for that column's choice set.
   - Value and feasibility scores are whole numbers from 1 to 5. Priority score = value × feasibility.
   - Estimated monthly credits is a whole number ≥ 0 (use 0 when the band is Included).
   - Text fits the max lengths. Shorten it if needed, never fail on length.
   - If anything required is missing, ask the user for it. Don't invent values.

2. **Guard against duplicates.** Run `read_query`:
   ```sql
   SELECT sams_usecaseid, sams_usecasenumber FROM sams_usecase
   WHERE sams_submitteremail = '<email>' AND sams_name = '<title>'
   ```
   If a conversation ID is available, also check `sams_conversationid = '<conversation id>'`. If a row already exists, **do not create another one**. Reuse its ID and continue at step 5 (systems) only for systems that don't exist yet.
   Escape single quotes in values by doubling them (`'` → `''`).

3. **Create the use case** with `create_record` on table `sams_usecase`. Example `item`:
   ```json
   {
     "sams_name": "Invoice exception handling assistant",
     "sams_submitteremail": "jane.doe@contoso.com",
     "sams_problemstatement": "...",
     "sams_desiredoutcome": "...",
     "sams_currentprocess": "...",
     "sams_examplerequest": "...",
     "sams_hourssavedpermonth": 40,
     "sams_audience": 726410000,
     "sams_usersband": 726410000,
     "sams_usagefrequency": 726410002,
     "sams_datasources": "726410001,726410003",
     "sams_capabilities": "726410002,726410004",
     "sams_predictability": 726410002,
     "sams_documentheavy": true,
     "sams_usagechannel": 726410000,
     "sams_copilotlicence": 726410002,
     "sams_sensitivity": 726410002,
     "sams_urgency": 726410002,
     "sams_recommendedtool": 726410004,
     "sams_alternativetool": 726410003,
     "sams_rationale": "- ...\n- ...",
     "sams_creditband": 726410002,
     "sams_estimatedmonthlycredits": 75000,
     "sams_creditdrivers": "- 25 users × 20 runs × 150 credits ≈ 75,000/month\n- ...",
     "sams_complexity": 726410002,
     "sams_confidence": 726410001,
     "sams_assumptions": "- ...",
     "sams_valuescore": 4,
     "sams_feasibilityscore": 3,
     "sams_priorityscore": 12,
     "sams_rubricversion": "2026.09-v1",
     "sams_status": 726410001,
     "sams_conversationsummary": "...",
     "sams_conversationid": "..."
   }
   ```
   Formatting rules:
   - **Single choice** is an integer.
   - **Multi-select choice** (`sams_datasources`, `sams_capabilities`) is a comma-separated string of integers with no spaces.
   - **Yes/no** is `true` or `false`.
   - **Status** is always `726410001` (Submitted).
   - Omit optional columns you have no value for. Never send `sams_usecasenumber`, because Dataverse generates it.
   - Rationale, credit drivers and assumptions are markdown bullets separated by `\n`.

   The tool returns `Created record with ID <guid>`. Keep that GUID.

4. **Read back the use case ID** with `read_query`:
   ```sql
   SELECT sams_usecasenumber, sams_status FROM sams_usecase WHERE sams_usecaseid = '<guid>'
   ```

5. **Create target systems.** For each system, call `create_record` on table `sams_usecasesystem`:
   ```json
   {
     "sams_name": "ServiceNow",
     "sams_systemtype": 726410003,
     "sams_access": 726410002,
     "sams_connectoravailable": 726410000,
     "sams_usecaseid": { "recordId": "<use case guid>", "relatedTable": "sams_usecase" }
   }
   ```
   When unsure, use `Other` (726410007) as the system type, and `Not sure` for access (726410003) and known connector (726410002).
   You can create all systems in **one** `create_record` call by passing them as an `items` array (max 25). Check the per-record results for failures.

6. **Confirm to the user.** Give the use case ID (for example **AUC-00042**), the title, the recommended tool and credit band, and say it's now **Submitted** for review by the CoE team. Mention they can ask "What's the status of AUC-00042?" at any time.

## Output
- Success: the use case ID, the GUID, and the number of systems saved.
- Failure: a plain-language message to the user, plus the technical error kept for troubleshooting.

## Troubleshooting

| Error | Cause | Recovery |
|---|---|---|
| "Principal user … is missing prvCreatesams_UseCase privilege" | The user doesn't have the **Agentic Use Case Submitter** role | Tell the user politely that they need access and should contact their Power Platform admin. Don't retry. |
| Invalid option value / "value … is not valid" | Wrong choice integer | Re-check `choice-values.md`, correct the value, retry once. |
| Use case created but a system failed | Transient error or bad system value | Retry that system once with safe defaults (Other / Not sure). Never re-create the use case. If it still fails, submit anyway and add the missing system names to the confirmation message. |
| Read-back returns nothing | Replication delay | Wait briefly and retry the `read_query` once. If still empty, confirm using the GUID and say the ID will appear shortly. |
| String too long | Text exceeds the column max | Shorten and retry. |

## Example

User confirms: "Yes, that's right, please submit."
→ Validate → duplicate check (none) → `create_record` sams_usecase → GUID `8f8a…` → `read_query` gives `AUC-00042` → `create_record` ×2 for SAP and ServiceNow → reply:
"Your idea **AUC-00042 – Invoice exception handling assistant** is submitted. Recommended: Copilot Studio (GitHub Copilot harness), credit band Medium. The CoE team will review it; ask me for its status any time."
