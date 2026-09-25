"""Deploy the Agentic Use Case Intake schema to Dataverse (idempotent).

Creates global choices, tables, columns, the 1:N relationship and environment variables,
all inside the solution named in .env (SOLUTION_NAME), then publishes.

Usage:  python scripts/create_schema.py
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from auth import get_token, load_env  # noqa: E402
import schema_def as S  # noqa: E402

load_env()
BASE = os.environ["DATAVERSE_URL"].rstrip("/") + "/api/data/v9.2/"
SOLUTION = os.environ["SOLUTION_NAME"]
TOKEN = get_token()


def call(method, path, body=None, solution=True, retries=3):
    import time
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
    }
    if solution:
        headers["MSCRM.SolutionUniqueName"] = SOLUTION
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            return resp.status, (json.loads(raw) if raw else None), resp.headers
    except urllib.error.HTTPError as e:
        payload = e.read().decode("utf-8", "replace")
        # 0x80040216 = transient metadata lock right after a previous customization
        if retries and method != "GET" and (e.code >= 500 or "0x80040216" in payload):
            time.sleep(10)
            return call(method, path, body, solution, retries - 1)
        return e.code, payload, e.headers


def ok(status, payload, what):
    if status >= 300:
        raise SystemExit(f"[FAIL] {what}: HTTP {status}\n{payload}")
    print(f"[OK]   {what}")


def exists(path):
    status, _, _ = call("GET", path, solution=False)
    return status == 200


def label(text):
    return {
        "@odata.type": "Microsoft.Dynamics.CRM.Label",
        "LocalizedLabels": [{"@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel", "Label": text, "LanguageCode": 1033}],
    }


def required(flag):
    return {"Value": "ApplicationRequired" if flag else "None", "CanBeChanged": True,
            "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings"}


# ---------- Global choices ----------
def create_choices():
    for name, (display, options) in S.CHOICES.items():
        if exists(f"GlobalOptionSetDefinitions(Name='{name}')"):
            print(f"[SKIP] choice {name}")
            continue
        body = {
            "@odata.type": "Microsoft.Dynamics.CRM.OptionSetMetadata",
            "Name": name,
            "DisplayName": label(display),
            "OptionSetType": "Picklist",
            "IsGlobal": True,
            "Options": [{"Value": v, "Label": label(t)} for v, t in options],
        }
        ok(*call("POST", "GlobalOptionSetDefinitions", body)[:2], f"choice {name}")


# ---------- Columns ----------
_optionset_ids = {}


def optionset_id(name):
    if name not in _optionset_ids:
        status, payload, _ = call("GET", f"GlobalOptionSetDefinitions(Name='{name}')?$select=MetadataId", solution=False)
        ok(status, payload, f"resolve choice {name}")
        _optionset_ids[name] = payload["MetadataId"]
    return _optionset_ids[name]


def attribute_body(table_prefix_schema, col):
    suffix, display, kind, extra = col
    schema = f"{S.PREFIX}_{suffix}"
    base = {"SchemaName": schema, "DisplayName": label(display), "RequiredLevel": required(extra.get("required", False))}
    if kind in ("string", "email", "autonumber"):
        base.update({"@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
                     "MaxLength": extra.get("max", 100 if kind != "email" else 320),
                     "FormatName": {"Value": "Email" if kind == "email" else "Text"}})
        if kind == "autonumber":
            base["AutoNumberFormat"] = extra["format"]
    elif kind == "memo":
        base.update({"@odata.type": "Microsoft.Dynamics.CRM.MemoAttributeMetadata",
                     "MaxLength": extra.get("max", 4000), "Format": "TextArea"})
    elif kind == "int":
        base.update({"@odata.type": "Microsoft.Dynamics.CRM.IntegerAttributeMetadata",
                     "MinValue": extra.get("min", 0), "MaxValue": extra.get("max", 2147483647), "Format": "None"})
    elif kind == "bool":
        base.update({"@odata.type": "Microsoft.Dynamics.CRM.BooleanAttributeMetadata", "DefaultValue": False,
                     "OptionSet": {"TrueOption": {"Value": 1, "Label": label("Yes")},
                                   "FalseOption": {"Value": 0, "Label": label("No")}}})
    elif kind == "date":
        base.update({"@odata.type": "Microsoft.Dynamics.CRM.DateTimeAttributeMetadata",
                     "Format": "DateOnly", "DateTimeBehavior": {"Value": "DateOnly"}})
    elif kind in ("choice", "multichoice"):
        odt = "PicklistAttributeMetadata" if kind == "choice" else "MultiSelectPicklistAttributeMetadata"
        base.update({"@odata.type": f"Microsoft.Dynamics.CRM.{odt}",
                     "GlobalOptionSet@odata.bind": f"/GlobalOptionSetDefinitions({optionset_id(extra['set'])})"})
        if "default" in extra:
            base["DefaultFormValue"] = extra["default"]
    else:
        raise ValueError(kind)
    return schema.lower(), base


def create_table(t):
    logical = t["schema"].lower()
    p_suffix, p_display, p_max = t["primary"]
    if not exists(f"EntityDefinitions(LogicalName='{logical}')"):
        body = {
            "@odata.type": "Microsoft.Dynamics.CRM.EntityMetadata",
            "SchemaName": t["schema"],
            "DisplayName": label(t["display"]),
            "DisplayCollectionName": label(t["plural"]),
            "Description": label(t["description"]),
            "OwnershipType": "UserOwned",
            "HasActivities": False,
            "HasNotes": True,
            "IsActivity": False,
            "Attributes": [{
                "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
                "SchemaName": f"{S.PREFIX}_{p_suffix}",
                "IsPrimaryName": True,
                "MaxLength": p_max,
                "FormatName": {"Value": "Text"},
                "DisplayName": label(p_display),
                "RequiredLevel": required(True),
            }],
        }
        ok(*call("POST", "EntityDefinitions", body)[:2], f"table {logical}")
    else:
        print(f"[SKIP] table {logical}")

    for col in t["columns"]:
        a_logical, body = attribute_body(t["schema"], col)
        if exists(f"EntityDefinitions(LogicalName='{logical}')/Attributes(LogicalName='{a_logical}')"):
            print(f"[SKIP]   column {a_logical}")
            continue
        ok(*call("POST", f"EntityDefinitions(LogicalName='{logical}')/Attributes", body)[:2], f"  column {a_logical}")


def create_relationship():
    r = S.RELATIONSHIP
    if exists(f"RelationshipDefinitions(SchemaName='{r['schema']}')"):
        print(f"[SKIP] relationship {r['schema']}")
        return
    body = {
        "@odata.type": "Microsoft.Dynamics.CRM.OneToManyRelationshipMetadata",
        "SchemaName": r["schema"],
        "ReferencedEntity": r["referenced"],
        "ReferencingEntity": r["referencing"],
        "CascadeConfiguration": {"Assign": "Cascade", "Delete": "Cascade", "Merge": "NoCascade",
                                 "Reparent": "Cascade", "Share": "Cascade", "Unshare": "Cascade",
                                 "RollupView": "NoCascade"},
        "AssociatedMenuConfiguration": {"Behavior": "UseCollectionName", "Group": "Details", "Order": 10000},
        "Lookup": {
            "@odata.type": "Microsoft.Dynamics.CRM.LookupAttributeMetadata",
            "SchemaName": r["lookup_schema"],
            "DisplayName": label(r["lookup_display"]),
            "RequiredLevel": required(True),
        },
    }
    ok(*call("POST", "RelationshipDefinitions", body)[:2], f"relationship {r['schema']}")


def create_env_vars():
    for schema, display, desc, default in S.ENV_VARS:
        q = urllib.parse.quote(f"schemaname eq '{schema}'")
        status, payload, _ = call("GET", f"environmentvariabledefinitions?$select=schemaname&$filter={q}", solution=False)
        if status == 200 and payload["value"]:
            print(f"[SKIP] env var {schema}")
            continue
        body = {"schemaname": schema, "displayname": display, "description": desc, "type": 100000000}
        if default:
            body["defaultvalue"] = default
        ok(*call("POST", "environmentvariabledefinitions", body)[:2], f"env var {schema}")


def publish():
    entities = "".join(f"<entity>{t['schema'].lower()}</entity>" for t in (S.USECASE, S.USECASESYSTEM))
    sets = "".join(f"<optionset>{n}</optionset>" for n in S.CHOICES)
    xml = f"<importexportxml><entities>{entities}</entities><optionsets>{sets}</optionsets></importexportxml>"
    ok(*call("POST", "PublishXml", {"ParameterXml": xml}, solution=False)[:2], "publish")


if __name__ == "__main__":
    create_choices()
    create_table(S.USECASE)
    create_table(S.USECASESYSTEM)
    create_relationship()
    create_env_vars()
    publish()
    print("Done.")
