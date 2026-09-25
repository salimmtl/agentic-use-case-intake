"""Create the SAMS security roles in the AgenticUseCaseIntake solution (idempotent).

Roles only grant access to the accelerator tables. Assign them together with the
out-of-the-box Basic User role.

Depth: Basic = User, Local = Business Unit, Deep = Parent:Child BU, Global = Organization
"""

import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from create_schema import call, ok  # noqa: E402

USER, ORG = "Basic", "Global"
TABLES = ("sams_usecase", "sams_usecasesystem")

ROLES = {
    "Agentic Use Case Submitter": {
        "Create": USER, "Read": USER, "Append": USER, "AppendTo": USER,
    },
    "Agentic Use Case Reviewer": {
        "Create": ORG, "Read": ORG, "Write": ORG, "Append": ORG, "AppendTo": ORG,
    },
    "Agentic Use Case Admin": {
        "Create": ORG, "Read": ORG, "Write": ORG, "Delete": ORG, "Append": ORG,
        "AppendTo": ORG, "Assign": ORG, "Share": ORG,
    },
}


def get(path):
    status, payload, _ = call("GET", path, solution=False)
    ok(status, payload, f"GET {path.split('?')[0]}")
    return payload["value"]


def main():
    root_bu = get("businessunits?$select=businessunitid&$filter=" + urllib.parse.quote("_parentbusinessunitid_value eq null"))[0]["businessunitid"]

    names = [f"prv{a}{t}" for t in TABLES for a in ("Create", "Read", "Write", "Delete", "Append", "AppendTo", "Assign", "Share")]
    flt = " or ".join(f"name eq '{n}'" for n in names)
    privileges = {p["name"].lower(): p["privilegeid"] for p in get("privileges?$select=name,privilegeid&$filter=" + urllib.parse.quote(flt))}

    for role_name, grants in ROLES.items():
        existing = get("roles?$select=roleid&$filter=" + urllib.parse.quote(
            f"name eq '{role_name}' and _businessunitid_value eq {root_bu}"))
        if existing:
            role_id = existing[0]["roleid"]
            print(f"[SKIP] role {role_name} exists")
        else:
            status, payload, headers = call("POST", "roles", {
                "name": role_name,
                "businessunitid@odata.bind": f"/businessunits({root_bu})",
            })
            ok(status, payload, f"role {role_name}")
            role_id = headers["OData-EntityId"].split("(")[-1].rstrip(")")

        body = {"Privileges": [
            {"PrivilegeId": privileges[f"prv{action}{t}".lower()], "Depth": depth, "BusinessUnitId": root_bu}
            for t in TABLES for action, depth in grants.items()
        ]}
        ok(*call("POST", f"roles({role_id})/Microsoft.Dynamics.CRM.AddPrivilegesRole", body)[:2],
           f"  privileges for {role_name}")


if __name__ == "__main__":
    main()
