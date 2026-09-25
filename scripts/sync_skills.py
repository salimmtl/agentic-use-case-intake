"""Sync Dataverse business skills from skills/<folder>/SKILL.md (repo = source of truth).

- Front matter `name` and `description` map to the skill name and description; the markdown after it is the body.
- Creates the skill if missing (in the solution), otherwise updates it. Skills are shared org-wide (ispersonal = false).
- Resource files (*.md other than SKILL.md) are uploaded to skillresource.filecontent.

Usage: python scripts/sync_skills.py
"""

import glob
import os
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from create_schema import BASE, SOLUTION, TOKEN, call, ok  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = {
    "submit-agentic-use-case": "sams_submitagenticusecase",
    "look-up-my-agentic-use-cases": "sams_lookupmyagenticusecases",
}
SKILL_TYPE, RESOURCE_TYPE = 10429, 10430


def parse(path):
    text = open(path, encoding="utf-8").read()
    _, front, body = text.split("---", 2)
    meta = {}
    for line in front.strip().splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    return meta["name"], meta["description"], body.strip()


def query(entity_set, flt, select):
    status, payload, _ = call("GET", f"{entity_set}?$select={select}&$filter={urllib.parse.quote(flt)}", solution=False)
    ok(status, payload, f"query {entity_set}")
    return payload["value"]


def add_to_solution(component_id, ctype):
    call("POST", "AddSolutionComponent", {"ComponentId": component_id, "ComponentType": ctype,
                                          "SolutionUniqueName": SOLUTION, "AddRequiredComponents": False,
                                          "DoNotIncludeSubcomponents": False}, solution=False)


def upload_file(resource_id, path):
    name = os.path.basename(path)
    data = open(path, "rb").read()
    url = f"{BASE}skillresources({resource_id})/filecontent?x-ms-file-name={urllib.parse.quote(name)}"
    req = urllib.request.Request(url, data=data, method="PATCH", headers={
        "Authorization": f"Bearer {TOKEN}", "Content-Type": "application/octet-stream",
        "OData-MaxVersion": "4.0", "OData-Version": "4.0"})
    with urllib.request.urlopen(req) as resp:
        print(f"[OK]     resource {name} uploaded ({len(data)} bytes, HTTP {resp.status})")


def sync(folder, uniquename):
    skill_dir = os.path.join(ROOT, "skills", folder)
    name, description, body = parse(os.path.join(skill_dir, "SKILL.md"))
    existing = query("skills", f"uniquename eq '{uniquename}'", "skillid")
    record = {"name": name, "description": description, "body": body, "ispersonal": False}
    if existing:
        skill_id = existing[0]["skillid"]
        ok(*call("PATCH", f"skills({skill_id})", record)[:2], f"update skill {uniquename}")
    else:
        status, payload, headers = call("POST", "skills", {**record, "uniquename": uniquename})
        ok(status, payload, f"create skill {uniquename}")
        skill_id = headers["OData-EntityId"].split("(")[-1].rstrip(")")
    add_to_solution(skill_id, SKILL_TYPE)

    for path in sorted(glob.glob(os.path.join(skill_dir, "*.md"))):
        fname = os.path.basename(path)
        if fname == "SKILL.md":
            continue
        res = query("skillresources", f"_skillid_value eq {skill_id} and filename eq '{fname}'", "skillresourceid")
        if res:
            res_id = res[0]["skillresourceid"]
        else:
            status, payload, headers = call("POST", "skillresources", {
                "filename": fname, "skillid@odata.bind": f"/skills({skill_id})"})
            ok(status, payload, f"  create resource {fname}")
            res_id = headers["OData-EntityId"].split("(")[-1].rstrip(")")
        add_to_solution(res_id, RESOURCE_TYPE)
        upload_file(res_id, path)


if __name__ == "__main__":
    for folder, uniquename in SKILLS.items():
        sync(folder, uniquename)
    print("Done.")
