"""Generate the intake agent's authored YAML from the repo's rubric files (single source of truth).

Writes into agent/intake-agent (a `pac copilot init --authoring-mode cli-copilot` workspace):
  - settings.mcs.yml             -> global instructions (StaticSegment)
  - behaviors/*.mcs.yml          -> InlineAgentSkill: intake interview, assessment (tool selection + credits)
  - capabilities/knowledge/files -> plain-language glossary (uploaded file + sidecar)
  - capabilities/tools           -> Dataverse MCP Server (McpTool), Office 365 Users "Get my profile (V2)"

Usage: python scripts/build_agent.py   (then push with the Copilot Studio manage-agent skill or `pac copilot push`)
"""

import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENT = os.path.join(ROOT, "agent", "intake-agent")
RUBRIC = os.path.join(ROOT, "rubric")

DV_CONNECTION_REF = "sams_agenticusecaseintake.cr.shared_commondataserviceforapps.dvmcp"
O365_CONNECTION_REF = "sams_agenticusecaseintake.cr.shared_office365users.profile"


def q(value):
    return json.dumps(value, ensure_ascii=False)


def block(text, indent):
    pad = " " * indent
    return "\n".join((pad + line) if line.strip() else "" for line in text.strip("\n").splitlines())


def read(name):
    with open(os.path.join(RUBRIC, name), encoding="utf-8") as f:
        return f.read()


def write(rel, content):
    path = os.path.join(AGENT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content.rstrip("\n") + "\n")
    print(f"[OK]   {rel}")


INSTRUCTIONS = """
You are the **Agentic Use Case Intake assistant**. You help people, most of them non-technical, describe an idea for an AI agent. You recommend the Microsoft tool best suited to build it, give an indicative Copilot Credit consumption band, and save the idea to Dataverse so the Center of Excellence (CoE) can review it.

## Scope
- In scope: capturing new agentic use case ideas, explaining Microsoft agentic tools in plain language, and looking up the status of the user's own submissions.
- Out of scope: building the agent, quoting prices, legal or licensing commitments, and other people's submissions. Politely decline and redirect.

## How every intake works
1. Follow the **intake-interview** skill. Get the submitter's email, ask one open question, then only the missing profile questions, one at a time, in plain language with short options. "Not sure" is always fine. Aim for 6–8 questions and under 5 minutes.
2. Play back a short summary and let the user correct it.
3. Follow the **assess-agentic-use-case** skill to choose the recommended tool, an alternative, the rationale, the credit band and estimate, complexity, confidence, scores and assumptions.
4. Show the recommendation in business language: tool, why (3–5 bullets), credit band with the main drivers, and what would change the recommendation. Then ask: "Shall I submit this idea to the CoE team?"
5. Only after the user says yes, save it. Use the **Dataverse MCP Server** tool to open the business skill **"Submit agentic use case"** (call `describe` on `skills/Submit agentic use case`, and read its resource `choice-values.md`), then follow it exactly. Confirm with the use case ID (AUC-xxxxx).

For status questions ("show my ideas", "what's the status of AUC-00042?"), open and follow the business skill **"Look up my agentic use cases"** through the Dataverse MCP Server tool.

## Dataverse rules (strict)
- Only read and write the tables `sams_usecase` and `sams_usecasesystem`, using `create_record` and `read_query`, as the business skills describe.
- Never create a use case without the user's explicit confirmation. Never create duplicates.
- Only show a user their own submissions (filtered by their email).

## Credits and recommendations
- Estimates are **indicative planning bands, not quotes**. Always say so, and suggest a pilot and a per-agent credit cap for Medium or High bands.
- Point to the guides when helpful: tool guide https://blue-hill-0cabcc90f.5.azurestaticapps.net/which-agentic-tool.html and credits guide https://blue-hill-0cabcc90f.5.azurestaticapps.net/copilot-studio-credits-explainer-extended.html
- The CoE team makes the final decision; you only recommend.

## Style
- Warm, concise and encouraging. One question per message. Avoid jargon, and explain any technical term in brackets.
- Use short bullets and options. Keep replies under about 120 words except for the recommendation summary.
- If you're unsure, say so and record it as an assumption rather than guessing.
"""


def settings():
    path = os.path.join(AGENT, "settings.mcs.yml")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    marker = "      segments:\n"
    start = text.index(marker) + len(marker)
    # the segments list ends at the next non-empty line indented less than its items
    end = re.search(r"^ {0,7}\S", text[start:], flags=re.M).start() + start
    new_segment = "        - kind: StaticSegment\n          value: |\n" + block(INSTRUCTIONS, 12) + "\n"
    write("settings.mcs.yml", text[:start] + new_segment + text[end:])


def skill(file_stem, name, description, body):
    # Server layout: behaviors/<stem>/skill.mcs.yml (metadata) + behaviors/<stem>/SKILL.md (content)
    content = f"---\nname: {name}\ndescription: {description}\n---\n<!-- bic:source=blank -->\n{body.strip()}\n"
    meta = (f"mcs.metadata:\n  componentName: {name}\n  description: {q(description)}\n"
            f"  schemaName: sams_AgenticUseCaseIntake.skill.{file_stem}\nkind: InlineAgentSkill\n")
    write(os.path.join("behaviors", file_stem, "skill.mcs.yml"), meta)
    write(os.path.join("behaviors", file_stem, "SKILL.md"), content)


ASSESS_PROCEDURE = """
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
"""


def main():
    settings()

    skill("intake-interview_Kq4w9Z", "intake-interview",
          "Runs the plain-language intake interview for a new agentic use case idea: gets the submitter's email, "
          "asks an open question, then only the missing profile questions (6-8 max), and plays back a summary.",
          read("intake-interview.md"))

    skill("assess-agentic-use-case_Tm7b2X", "assess-agentic-use-case",
          "Recommends the best Microsoft agentic tool and an alternative, estimates the Copilot Credit band, and "
          "scores complexity, confidence, value and feasibility for a confirmed agentic use case idea.",
          ASSESS_PROCEDURE + "\n\n" + read("tool-selection.md") + "\n\n" + read("credit-estimation.md"))

    kdir = os.path.join(AGENT, "capabilities", "knowledge", "files")
    os.makedirs(kdir, exist_ok=True)
    shutil.copyfile(os.path.join(RUBRIC, "agentic-tools-glossary.md"), os.path.join(kdir, "agentic-tools-glossary.md"))
    print("[OK]   capabilities/knowledge/files/agentic-tools-glossary.md")
    # File-knowledge descriptions are fixed when the file is first attached; only write the sidecar once.
    sidecar = os.path.join("capabilities", "knowledge", "files", "agentictoolsglossarymd_Gl0s5a.mcs.yml")
    if not os.path.exists(os.path.join(AGENT, sidecar)):
        write(sidecar, "mcs.metadata:\n  componentName: \"agentic-tools-glossary.md\"\n"
              "  description: \"Plain-language explanations of Microsoft agentic tools and Copilot Credits.\"\n")

    write(os.path.join("capabilities", "tools", "dataverse-mcp-server_Dv8m3P.mcs.yml"),
          "mcs.metadata:\n  componentName: \"Dataverse MCP Server\"\n"
          "  description: \"Reads and saves agentic use cases in Dataverse and retrieves the business skills 'Submit agentic "
          "use case' and 'Look up my agentic use cases'. Use describe on skills/<name> first, then create_record and "
          "read_query on sams_usecase and sams_usecasesystem only.\"\n"
          "kind: McpTool\nauthMode: \"Invoker\"\n"
          f"connectionReference: {q(DV_CONNECTION_REF)}\n"
          "connectorId: \"/providers/Microsoft.PowerApps/apis/shared_commondataserviceforapps\"\n"
          "operationId: \"InvokeMCP\"\n")

    write(os.path.join("capabilities", "tools", "office365-users-get-my-profile_Pr0f1L.mcs.yml"),
          "mcs.metadata:\n  componentName: \"Get my profile (V2)\"\n"
          "  description: \"Returns the signed-in user's Microsoft 365 profile. Use it once at the start of an intake to get "
          "the submitter's work email (userPrincipalName, or mail if userPrincipalName is empty).\"\n"
          "kind: ConnectorTool\nauthMode: \"Invoker\"\n"
          f"connectionReference: {q(O365_CONNECTION_REF)}\n"
          "connectorId: \"/providers/Microsoft.PowerApps/apis/shared_office365users\"\n"
          "operationId: \"MyProfile_V2\"\n")


if __name__ == "__main__":
    main()
