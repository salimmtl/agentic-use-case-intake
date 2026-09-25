"""Single source of truth for the Agentic Use Case Intake Dataverse schema.

Consumed by create_schema.py (metadata deployment) and gen_docs.py (docs/data-model.md).
Choice values use the SAMS publisher option value prefix 72641.
"""

PREFIX = "sams"
V = 726410000  # first option value for every choice


def opts(*labels):
    return [(V + i, label) for i, label in enumerate(labels)]


# Global choices (name -> display name, options)
CHOICES = {
    "sams_audience": ("Audience", opts("Internal (employees)", "External (customers, partners, public)", "Both")),
    "sams_usersband": ("Number of Users", opts("Fewer than 50", "50 to 500", "500 to 5,000", "More than 5,000", "Not sure")),
    "sams_usagefrequency": ("Usage Frequency", opts("Occasionally", "Weekly", "Daily", "Many times a day", "Not sure")),
    "sams_datasources": ("Data Sources", opts(
        "Public web", "Documents and SharePoint", "Email, Teams and calendar",
        "Business systems (CRM, ERP, ticketing...)", "None or not sure")),
    "sams_capabilities": ("Agent Capabilities", opts(
        "Answer questions", "Draft or summarize content", "Take actions in systems",
        "Run on its own when something happens", "Work through multi-step tasks with judgment")),
    "sams_predictability": ("Process Predictability", opts(
        "Same steps every time", "Mostly the same, some exceptions", "Varies a lot case by case", "Not sure")),
    "sams_usagechannel": ("Usage Channel", opts(
        "Microsoft Teams", "Microsoft 365 Copilot", "Public website", "Our own app or portal", "Not sure")),
    "sams_copilotlicence": ("M365 Copilot Licence", opts("Yes, all users", "Some users", "No", "Not sure")),
    "sams_sensitivity": ("Data Sensitivity", opts(
        "No sensitive data", "Personal information", "Financial information", "Regulated or confidential", "Not sure")),
    "sams_urgency": ("Urgency", opts("Exploring the idea", "Within 6 months", "Within 3 months", "As soon as possible")),
    "sams_agentictool": ("Agentic Tool", opts(
        "Microsoft 365 Copilot", "Copilot Cowork", "Agent Builder (declarative agent)",
        "Copilot Studio - Standard harness", "Copilot Studio - GitHub Copilot harness",
        "Microsoft Foundry", "No agent needed - Power Automate / workflow")),
    "sams_creditband": ("Credit Band", opts("Included (about 0)", "Low", "Medium", "High")),
    "sams_level": ("Level", opts("Low", "Medium", "High")),
    "sams_usecasestatus": ("Use Case Status", opts(
        "Draft", "Submitted", "In review", "Needs info", "Approved", "In build", "Live", "Declined")),
    "sams_systemtype": ("System Type", opts(
        "Microsoft 365 app", "Dataverse or Dynamics 365", "SAP", "ServiceNow", "Salesforce",
        "Custom API or database", "Website or portal", "Other")),
    "sams_systemaccess": ("System Access", opts("Read", "Write", "Read and write", "Not sure")),
    "sams_yesnounknown": ("Yes No Unknown", opts("Yes", "No", "Not sure")),
}

STATUS_SUBMITTED = V + 1

# Column spec: (schema_suffix, display, type, extra)
# types: string, email, memo, int, bool, date, choice, multichoice, autonumber
USECASE = {
    "schema": "sams_UseCase",
    "display": "Agentic Use Case",
    "plural": "Agentic Use Cases",
    "description": "An agentic use case idea captured by the intake agent, with its assessment and review.",
    "primary": ("Name", "Title", 200),
    "columns": [
        # Identity
        ("UseCaseNumber", "Use Case ID", "autonumber", {"format": "AUC-{SEQNUM:5}"}),
        ("SubmitterEmail", "Submitter Email", "email", {"required": True}),
        # The idea
        ("ProblemStatement", "Problem Statement", "memo", {"max": 4000}),
        ("DesiredOutcome", "Desired Outcome", "memo", {"max": 4000}),
        ("CurrentProcess", "Current Process", "memo", {"max": 4000}),
        ("ExampleRequest", "Example Request or Trigger", "memo", {"max": 2000}),
        ("HoursSavedPerMonth", "Hours Saved per Month", "int", {"min": 0, "max": 1000000}),
        # Profile
        ("Audience", "Audience", "choice", {"set": "sams_audience"}),
        ("UsersBand", "Number of Users", "choice", {"set": "sams_usersband"}),
        ("UsageFrequency", "Usage Frequency", "choice", {"set": "sams_usagefrequency"}),
        ("DataSources", "Data Sources", "multichoice", {"set": "sams_datasources"}),
        ("Capabilities", "What It Must Do", "multichoice", {"set": "sams_capabilities"}),
        ("Predictability", "Process Predictability", "choice", {"set": "sams_predictability"}),
        ("DocumentHeavy", "Document Heavy", "bool", {}),
        ("UsageChannel", "Where Users Will Use It", "choice", {"set": "sams_usagechannel"}),
        ("CopilotLicence", "Users Have M365 Copilot", "choice", {"set": "sams_copilotlicence"}),
        ("Sensitivity", "Data Sensitivity", "choice", {"set": "sams_sensitivity"}),
        ("Urgency", "Urgency", "choice", {"set": "sams_urgency"}),
        # Assessment
        ("RecommendedTool", "Recommended Tool", "choice", {"set": "sams_agentictool"}),
        ("AlternativeTool", "Alternative Tool", "choice", {"set": "sams_agentictool"}),
        ("Rationale", "Rationale", "memo", {"max": 10000}),
        ("CreditBand", "Credit Band", "choice", {"set": "sams_creditband"}),
        ("EstimatedMonthlyCredits", "Estimated Monthly Credits", "int", {"min": 0, "max": 2000000000}),
        ("CreditDrivers", "Credit Drivers", "memo", {"max": 4000}),
        ("Complexity", "Complexity", "choice", {"set": "sams_level"}),
        ("Confidence", "Confidence", "choice", {"set": "sams_level"}),
        ("Assumptions", "Assumptions and Open Questions", "memo", {"max": 4000}),
        ("ValueScore", "Value Score", "int", {"min": 1, "max": 5}),
        ("FeasibilityScore", "Feasibility Score", "int", {"min": 1, "max": 5}),
        ("PriorityScore", "Priority Score", "int", {"min": 1, "max": 25}),
        ("RubricVersion", "Rubric Version", "string", {"max": 20}),
        # Review
        ("Status", "Status", "choice", {"set": "sams_usecasestatus", "default": STATUS_SUBMITTED}),
        ("ReviewedBy", "Reviewed By", "email", {}),
        ("FinalTool", "Final Tool", "choice", {"set": "sams_agentictool"}),
        ("ReviewerNotes", "Reviewer Notes", "memo", {"max": 4000}),
        ("InfoNeeded", "Information Needed", "memo", {"max": 2000}),
        ("DecisionDate", "Decision Date", "date", {}),
        # Trace
        ("ConversationSummary", "Conversation Summary", "memo", {"max": 10000}),
        ("ConversationId", "Conversation ID", "string", {"max": 200}),
    ],
}

USECASESYSTEM = {
    "schema": "sams_UseCaseSystem",
    "display": "Target System",
    "plural": "Target Systems",
    "description": "A system the agentic use case needs to read from or write to.",
    "primary": ("Name", "System Name", 200),
    "columns": [
        ("SystemType", "System Type", "choice", {"set": "sams_systemtype"}),
        ("Access", "Access", "choice", {"set": "sams_systemaccess"}),
        ("ConnectorAvailable", "Known Connector", "choice", {"set": "sams_yesnounknown"}),
    ],
}

RELATIONSHIP = {
    "schema": "sams_UseCase_UseCaseSystem",
    "referenced": "sams_usecase",
    "referencing": "sams_usecasesystem",
    "lookup_schema": "sams_UseCaseId",
    "lookup_display": "Use Case",
}

ENV_VARS = [
    ("sams_IntakeAgentUrl", "Intake Agent URL",
     "Link that opens the published intake agent (Teams or other channel). Set after publishing the agent.", ""),
    ("sams_ToolGuideUrl", "Agentic Tool Guide URL", "Link to the 'Which agentic tool' guide.",
     "https://blue-hill-0cabcc90f.5.azurestaticapps.net/which-agentic-tool.html"),
    ("sams_CreditsGuideUrl", "Copilot Credits Guide URL", "Link to the Copilot Studio credits explainer.",
     "https://blue-hill-0cabcc90f.5.azurestaticapps.net/copilot-studio-credits-explainer-extended.html"),
]
