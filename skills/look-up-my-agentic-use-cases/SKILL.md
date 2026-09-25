---
name: Look up my agentic use cases
description: Use when a user asks about the agentic use case ideas they submitted, e.g. "show my ideas", "what's the status of AUC-00042", "did the CoE review my use case", "what information do they need from me". Reads sams_usecase and sams_usecasesystem rows for the user's own submissions and explains status, recommendation and reviewer requests in plain language.
---

# Look up my agentic use cases

Finds and explains the user's own agentic use case submissions with the Dataverse MCP server.

**Required tool:** Dataverse MCP server `read_query` only. This skill never writes.

## Inputs
- **Submitter email** (required). Take it from the user's session. If there is none, ask for it.
- **Use case ID** (optional), e.g. `AUC-00042`.

## Steps

1. **List the user's submissions** (newest first):
   ```sql
   SELECT TOP 20 sams_usecaseid, sams_usecasenumber, sams_name, sams_status, sams_recommendedtool,
          sams_finaltool, sams_creditband, sams_infoneeded, createdon
   FROM sams_usecase
   WHERE sams_submitteremail = '<email>'
   ORDER BY createdon DESC
   ```

2. **One specific use case:**
   ```sql
   SELECT sams_usecaseid, sams_usecasenumber, sams_name, sams_status, sams_recommendedtool, sams_alternativetool,
          sams_finaltool, sams_creditband, sams_estimatedmonthlycredits, sams_rationale, sams_infoneeded,
          sams_reviewernotes, sams_decisiondate, createdon
   FROM sams_usecase
   WHERE sams_usecasenumber = '<AUC-xxxxx>' AND sams_submitteremail = '<email>'
   ```
   Its systems:
   ```sql
   SELECT sams_name, sams_systemtype, sams_access FROM sams_usecasesystem WHERE sams_usecaseid = '<guid>'
   ```
   Always keep the `sams_submitteremail` filter. Only show a user their own submissions, even if they ask about someone else's ID.

3. **Explain in plain language.** `read_query` returns both the value and a `…name` label column (e.g. `sams_statusname`). Use the labels.
   - Status meanings:

     | Status | Meaning |
     |---|---|
     | Submitted | Waiting for the CoE team |
     | In review | Being assessed |
     | Needs info | The reviewers asked a question; show `sams_infoneeded` and invite the user to reply by submitting an updated idea or contacting the CoE |
     | Approved | Accepted for build |
     | In build | Being built |
     | Live | In use |
     | Declined | Not going ahead; show the reviewer notes if present |
   - If `sams_finaltool` is set and differs from the recommended tool, say the reviewers chose a different tool.
   - Present a list as a short table: ID · title · status · tool · credit band.

## Output
A short answer in business language. If nothing is found, say so and offer to capture a new idea.

## Troubleshooting

| Error | Cause | Recovery |
|---|---|---|
| Missing prvReadsams_UseCase privilege | The user doesn't have the Submitter role | Explain that they need access from their Power Platform admin. |
| No rows but the user insists | Different email used at submission | Ask whether they used another email address, then search with it. |
