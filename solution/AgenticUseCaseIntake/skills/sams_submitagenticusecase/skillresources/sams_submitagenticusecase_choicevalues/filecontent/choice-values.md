# Agentic Use Case Intake — column and choice reference

Generated from `scripts/schema_def.py`. Do not edit by hand.

## sams_usecase (Agentic Use Case)

| Logical name | Display name | Type | Notes |
|---|---|---|---|
| `sams_name` | Title | text (max 200) | **required** |
| `sams_usecasenumber` | Use Case ID | auto-number (read-only, do not set) |  |
| `sams_submitteremail` | Submitter Email | email (max 320) | **required** |
| `sams_problemstatement` | Problem Statement | text (max 4000) |  |
| `sams_desiredoutcome` | Desired Outcome | text (max 4000) |  |
| `sams_currentprocess` | Current Process | text (max 4000) |  |
| `sams_examplerequest` | Example Request or Trigger | text (max 2000) |  |
| `sams_hourssavedpermonth` | Hours Saved per Month | whole number 0–1000000 |  |
| `sams_audience` | Audience | choice `sams_audience` |  |
| `sams_usersband` | Number of Users | choice `sams_usersband` |  |
| `sams_usagefrequency` | Usage Frequency | choice `sams_usagefrequency` |  |
| `sams_datasources` | Data Sources | multi-select choice `sams_datasources` |  |
| `sams_capabilities` | What It Must Do | multi-select choice `sams_capabilities` |  |
| `sams_predictability` | Process Predictability | choice `sams_predictability` |  |
| `sams_documentheavy` | Document Heavy | yes/no (true/false) |  |
| `sams_usagechannel` | Where Users Will Use It | choice `sams_usagechannel` |  |
| `sams_copilotlicence` | Users Have M365 Copilot | choice `sams_copilotlicence` |  |
| `sams_sensitivity` | Data Sensitivity | choice `sams_sensitivity` |  |
| `sams_urgency` | Urgency | choice `sams_urgency` |  |
| `sams_recommendedtool` | Recommended Tool | choice `sams_agentictool` |  |
| `sams_alternativetool` | Alternative Tool | choice `sams_agentictool` |  |
| `sams_rationale` | Rationale | text (max 10000) |  |
| `sams_creditband` | Credit Band | choice `sams_creditband` |  |
| `sams_estimatedmonthlycredits` | Estimated Monthly Credits | whole number 0–2000000000 |  |
| `sams_creditdrivers` | Credit Drivers | text (max 4000) |  |
| `sams_complexity` | Complexity | choice `sams_level` |  |
| `sams_confidence` | Confidence | choice `sams_level` |  |
| `sams_assumptions` | Assumptions and Open Questions | text (max 4000) |  |
| `sams_valuescore` | Value Score | whole number 1–5 |  |
| `sams_feasibilityscore` | Feasibility Score | whole number 1–5 |  |
| `sams_priorityscore` | Priority Score | whole number 1–25 |  |
| `sams_rubricversion` | Rubric Version | text (max 20) |  |
| `sams_status` | Status | choice `sams_usecasestatus` |  |
| `sams_reviewedby` | Reviewed By | email (max 320) |  |
| `sams_finaltool` | Final Tool | choice `sams_agentictool` |  |
| `sams_reviewernotes` | Reviewer Notes | text (max 4000) |  |
| `sams_infoneeded` | Information Needed | text (max 2000) |  |
| `sams_decisiondate` | Decision Date | date only (YYYY-MM-DD) |  |
| `sams_conversationsummary` | Conversation Summary | text (max 10000) |  |
| `sams_conversationid` | Conversation ID | text (max 200) |  |

## sams_usecasesystem (Target System)

| Logical name | Display name | Type | Notes |
|---|---|---|---|
| `sams_name` | System Name | text (max 200) | **required** |
| `sams_systemtype` | System Type | choice `sams_systemtype` |  |
| `sams_access` | Access | choice `sams_systemaccess` |  |
| `sams_connectoravailable` | Known Connector | choice `sams_yesnounknown` |  |
| `sams_usecaseid` | Use Case | lookup to sams_usecase | **required** |

## Choice values

### sams_audience (Audience)

`726410000` = Internal (employees) · `726410001` = External (customers, partners, public) · `726410002` = Both

### sams_usersband (Number of Users)

`726410000` = Fewer than 50 · `726410001` = 50 to 500 · `726410002` = 500 to 5,000 · `726410003` = More than 5,000 · `726410004` = Not sure

### sams_usagefrequency (Usage Frequency)

`726410000` = Occasionally · `726410001` = Weekly · `726410002` = Daily · `726410003` = Many times a day · `726410004` = Not sure

### sams_datasources (Data Sources)

`726410000` = Public web · `726410001` = Documents and SharePoint · `726410002` = Email, Teams and calendar · `726410003` = Business systems (CRM, ERP, ticketing...) · `726410004` = None or not sure

### sams_capabilities (Agent Capabilities)

`726410000` = Answer questions · `726410001` = Draft or summarize content · `726410002` = Take actions in systems · `726410003` = Run on its own when something happens · `726410004` = Work through multi-step tasks with judgment

### sams_predictability (Process Predictability)

`726410000` = Same steps every time · `726410001` = Mostly the same, some exceptions · `726410002` = Varies a lot case by case · `726410003` = Not sure

### sams_usagechannel (Usage Channel)

`726410000` = Microsoft Teams · `726410001` = Microsoft 365 Copilot · `726410002` = Public website · `726410003` = Our own app or portal · `726410004` = Not sure

### sams_copilotlicence (M365 Copilot Licence)

`726410000` = Yes, all users · `726410001` = Some users · `726410002` = No · `726410003` = Not sure

### sams_sensitivity (Data Sensitivity)

`726410000` = No sensitive data · `726410001` = Personal information · `726410002` = Financial information · `726410003` = Regulated or confidential · `726410004` = Not sure

### sams_urgency (Urgency)

`726410000` = Exploring the idea · `726410001` = Within 6 months · `726410002` = Within 3 months · `726410003` = As soon as possible

### sams_agentictool (Agentic Tool)

`726410000` = Microsoft 365 Copilot · `726410001` = Copilot Cowork · `726410002` = Agent Builder (declarative agent) · `726410003` = Copilot Studio - Standard harness · `726410004` = Copilot Studio - GitHub Copilot harness · `726410005` = Microsoft Foundry · `726410006` = No agent needed - Power Automate / workflow

### sams_creditband (Credit Band)

`726410000` = Included (about 0) · `726410001` = Low · `726410002` = Medium · `726410003` = High

### sams_level (Level)

`726410000` = Low · `726410001` = Medium · `726410002` = High

### sams_usecasestatus (Use Case Status)

`726410000` = Draft · `726410001` = Submitted · `726410002` = In review · `726410003` = Needs info · `726410004` = Approved · `726410005` = In build · `726410006` = Live · `726410007` = Declined

### sams_systemtype (System Type)

`726410000` = Microsoft 365 app · `726410001` = Dataverse or Dynamics 365 · `726410002` = SAP · `726410003` = ServiceNow · `726410004` = Salesforce · `726410005` = Custom API or database · `726410006` = Website or portal · `726410007` = Other

### sams_systemaccess (System Access)

`726410000` = Read · `726410001` = Write · `726410002` = Read and write · `726410003` = Not sure

### sams_yesnounknown (Yes No Unknown)

`726410000` = Yes · `726410001` = No · `726410002` = Not sure
