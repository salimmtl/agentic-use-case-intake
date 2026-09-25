"""Build the Agentic Use Case Hub model-driven app assets (idempotent).

Creates or updates, inside the solution from .env:
  - main forms for sams_usecase and sams_usecasesystem
  - public views, quick find and associated views
  - system charts
  - the "Agentic Use Case Overview" dashboard
  - the model-driven app "Agentic Use Case Hub" with its site map

Fixed GUIDs (uuid5) make every component re-runnable: an existing record is PATCHed, a missing one is created.

Usage: python scripts/create_mda.py
"""

import os
import subprocess
import sys
import uuid
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from create_schema import SOLUTION, call, ok  # noqa: E402
import schema_def as S  # noqa: E402

NS = uuid.UUID("5a3e1b1c-2f7d-4a3a-9c1e-5a3e1b1c0001")
UC, SYS = "sams_usecase", "sams_usecasesystem"
REL = S.RELATIONSHIP["schema"]
V = S.V
ST = {name: V + i for i, name in enumerate(
    ["Draft", "Submitted", "InReview", "NeedsInfo", "Approved", "InBuild", "Live", "Declined"])}

CLASSID = {
    "string": "{4273EDBD-AC1D-40d3-9FB2-095C621B552D}",
    "autonumber": "{4273EDBD-AC1D-40d3-9FB2-095C621B552D}",
    "email": "{ADA2203E-B4CD-49be-9DDF-234642B43B52}",
    "memo": "{E0DECE4B-6FC8-4a8f-A065-082708572369}",
    "int": "{C6D124CA-7EDA-4a60-AEA9-7FB8D318B68F}",
    "bool": "{67FAC785-CD58-4f9f-ABB3-4B7DDC6ED5ED}",
    "date": "{5B773807-9FB2-42db-97C3-7A91EFF8ADFF}",
    "choice": "{3EF39988-22BB-4f0b-BBBE-64B5A3748AEE}",
    "multichoice": "{4AA28AB7-9C13-4F57-A73D-AD894D048B5F}",
    "lookup": "{270BD3DB-D9AF-4782-9025-509E298DEC0A}",
    "subgrid": "{E7A81278-8635-4d9e-8D4D-59480B391C5B}",
}


def gid(name):
    return str(uuid.uuid5(NS, name))


def brace(g):
    return "{" + g.upper() + "}"


def g():
    return brace(str(uuid.uuid4()))


def col_types(table):
    types = {f"{S.PREFIX}_{table['primary'][0].lower()}": ("string", table["primary"][1])}
    for suffix, display, kind, _ in table["columns"]:
        types[f"{S.PREFIX}_{suffix.lower()}"] = (kind, display)
    return types


TYPES = {UC: col_types(S.USECASE), SYS: col_types(S.USECASESYSTEM)}
TYPES[SYS]["sams_usecaseid"] = ("lookup", "Use Case")


def label_xml(text):
    return f'<labels><label description="{escape(text)}" languagecode="1033" /></labels>'


# ---------------------------------------------------------------- generic upsert
def upsert(entity_set, key, record_id, body, what):
    status, _, _ = call("GET", f"{entity_set}({record_id})?$select={key}", solution=False)
    if status == 200:
        ok(*call("PATCH", f"{entity_set}({record_id})", body)[:2], f"update {what}")
    else:
        ok(*call("POST", entity_set, {**body, key: record_id})[:2], f"create {what}")
    return record_id


def otc(table):
    status, payload, _ = call("GET", f"EntityDefinitions(LogicalName='{table}')?$select=ObjectTypeCode,MetadataId", solution=False)
    ok(status, payload, f"metadata {table}")
    return payload["ObjectTypeCode"], payload["MetadataId"]


# ---------------------------------------------------------------- forms
def field_cell(table, attr, disabled=False):
    kind, display = TYPES[table][attr]
    return (f'<cell id="{g()}" showlabel="true">{label_xml(display)}'
            f'<control id="{attr}" classid="{CLASSID[kind]}" datafieldname="{attr}" disabled="{str(disabled).lower()}" /></cell>')


def section(title, table, fields, columns=2, show_label=True):
    rows = []
    for i in range(0, len(fields), columns):
        chunk = fields[i:i + columns]
        cells = "".join(field_cell(table, f) for f in chunk)
        cells += "".join(f'<cell id="{g()}" showlabel="false">{label_xml("")}</cell>' for _ in range(columns - len(chunk)))
        rows.append(f"<row>{cells}</row>")
    return (f'<section name="{escape(title)}" id="{g()}" showlabel="{str(show_label).lower()}" showbar="false" '
            f'columns="{"1" * columns}">{label_xml(title)}<rows>{"".join(rows)}</rows></section>')


def raw_section(title, inner_cell):
    return (f'<section name="{escape(title)}" id="{g()}" showlabel="false" showbar="false" columns="1">'
            f'{label_xml(title)}<rows><row>{inner_cell}</row></rows></section>')


def tab(title, sections, expanded=True):
    return (f'<tab name="{escape(title)}" id="{g()}" expanded="{str(expanded).lower()}" showlabel="true">{label_xml(title)}'
            f'<columns><column width="100%"><sections>{"".join(sections)}</sections></column></columns></tab>')


def subgrid_cell(control_id, target, view_id, relationship, rows=6, title=""):
    return (f'<cell id="{g()}" showlabel="{str(bool(title)).lower()}" rowspan="{rows}" colspan="1" auto="false">{label_xml(title)}'
            f'<control id="{control_id}" classid="{CLASSID["subgrid"]}" indicationOfSubgrid="true"><parameters>'
            f'<ViewId>{brace(view_id)}</ViewId><IsUserView>false</IsUserView>'
            f'<RelationshipName>{relationship}</RelationshipName><TargetEntityType>{target}</TargetEntityType>'
            f'<AutoExpand>Fixed</AutoExpand><EnableQuickFind>false</EnableQuickFind><EnableViewPicker>false</EnableViewPicker>'
            f'<EnableJumpBar>false</EnableJumpBar><ChartGridMode>Grid</ChartGridMode><VisualizationId />'
            f'<IsUserChart>false</IsUserChart><EnableChartPicker>false</EnableChartPicker><RecordsPerPage>10</RecordsPerPage>'
            f'</parameters></control></cell>')


def header(table, fields):
    cells = "".join(
        f'<cell id="{g()}" showlabel="true">{label_xml(TYPES[table][f][1])}'
        f'<control id="header_{f}" classid="{CLASSID[TYPES[table][f][0]]}" datafieldname="{f}" disabled="false" /></cell>'
        for f in fields)
    return f'<header id="{g()}" celllabelposition="Top" columns="{"1" * len(fields)}" labelwidth="115" celllabelalignment="Left"><rows><row>{cells}</row></rows></header>'


def form_xml(tabs, hdr=""):
    return f'<form><tabs>{"".join(tabs)}</tabs>{hdr}<footer id="{g()}" celllabelposition="Top" columns="111" labelwidth="115" celllabelalignment="Left"><rows /></footer></form>'


def main_form_id(table):
    status, payload, _ = call("GET", f"systemforms?$select=formid,name&$filter=objecttypecode%20eq%20'{table}'%20and%20type%20eq%202", solution=False)
    ok(status, payload, f"find main form {table}")
    return payload["value"][0]["formid"]


def build_usecase_form(system_view_id):
    timeline = (f'<cell id="{g()}" showlabel="false" colspan="1" auto="false" rowspan="12">{label_xml("Timeline")}'
                f'<control id="notescontrol" classid="{{06375649-c143-495e-a496-c962e5b4488e}}"><parameters>'
                f'<DefaultTabId>ActivitiesTab</DefaultTabId></parameters></control></cell>')
    tabs = [
        tab("Idea", [
            section("Summary", UC, ["sams_name", "sams_usecasenumber", "sams_submitteremail", "sams_urgency"]),
            section("The idea", UC, ["sams_problemstatement", "sams_desiredoutcome", "sams_currentprocess",
                                     "sams_examplerequest", "sams_hourssavedpermonth"], columns=1),
        ]),
        tab("Profile", [
            section("Who and how often", UC, ["sams_audience", "sams_usersband", "sams_usagefrequency",
                                              "sams_usagechannel", "sams_copilotlicence", "sams_sensitivity"]),
            section("What it must do", UC, ["sams_capabilities", "sams_datasources", "sams_predictability",
                                            "sams_documentheavy"]),
        ]),
        tab("Recommendation", [
            section("Recommended tool", UC, ["sams_recommendedtool", "sams_alternativetool", "sams_complexity",
                                             "sams_confidence"]),
            section("Rationale", UC, ["sams_rationale", "sams_assumptions"], columns=1),
            section("Credit estimate", UC, ["sams_creditband", "sams_estimatedmonthlycredits"]),
            section("Credit drivers", UC, ["sams_creditdrivers"], columns=1, show_label=False),
            section("Scores", UC, ["sams_valuescore", "sams_feasibilityscore", "sams_priorityscore",
                                   "sams_rubricversion"]),
        ]),
        tab("Review", [
            section("Decision", UC, ["sams_status", "sams_finaltool", "sams_reviewedby", "sams_decisiondate"]),
            section("Notes", UC, ["sams_infoneeded", "sams_reviewernotes"], columns=1),
        ]),
        tab("Target systems", [
            raw_section("Target systems", subgrid_cell("TargetSystems", SYS, system_view_id, REL, rows=8)),
        ]),
        tab("Conversation", [
            section("Intake conversation", UC, ["sams_conversationsummary", "sams_conversationid"], columns=1),
            raw_section("Timeline", timeline),
        ], expanded=False),
    ]
    hdr = header(UC, ["sams_status", "sams_recommendedtool", "sams_creditband", "sams_submitteremail"])
    form_id = main_form_id(UC)
    ok(*call("PATCH", f"systemforms({form_id})", {"name": "Agentic Use Case", "formxml": form_xml(tabs, hdr)})[:2], "main form sams_usecase")
    return form_id


def build_system_form():
    tabs = [tab("General", [section("Target system", SYS, ["sams_name", "sams_usecaseid", "sams_systemtype",
                                                            "sams_access", "sams_connectoravailable"])])]
    form_id = main_form_id(SYS)
    ok(*call("PATCH", f"systemforms({form_id})", {"name": "Target System", "formxml": form_xml(tabs)})[:2], "main form sams_usecasesystem")
    return form_id


# ---------------------------------------------------------------- views
UC_COLS = [("sams_usecasenumber", 110), ("sams_name", 260), ("sams_status", 110), ("sams_recommendedtool", 220),
           ("sams_creditband", 110), ("sams_audience", 140), ("sams_usersband", 120), ("sams_priorityscore", 90),
           ("sams_submitteremail", 200), ("createdon", 130)]
SYS_COLS = [("sams_name", 220), ("sams_systemtype", 160), ("sams_access", 120), ("sams_connectoravailable", 120),
            ("sams_usecaseid", 240)]


def fetch(table, cols, conditions="", order=("createdon", True), quickfind=None):
    attrs = "".join(f'<attribute name="{c}" />' for c, _ in cols) + f'<attribute name="{table}id" />'
    filt = f'<filter type="and"><condition attribute="statecode" operator="eq" value="0" />{conditions}</filter>'
    if quickfind:
        filt += ('<filter type="or" isquickfindfields="1">' +
                 "".join(f'<condition attribute="{c}" operator="like" value="{{0}}" />' for c in quickfind) + "</filter>")
    return (f'<fetch version="1.0" output-format="xml-platform" mapping="logical" distinct="false">'
            f'<entity name="{table}">{attrs}<order attribute="{order[0]}" descending="{str(order[1]).lower()}" />'
            f'{filt}</entity></fetch>')


def layout(table, code, cols):
    cells = "".join(f'<cell name="{c}" width="{w}" />' for c, w in cols)
    return (f'<grid name="resultset" object="{code}" jump="sams_name" select="1" icon="1" preview="1">'
            f'<row name="result" id="{table}id">{cells}</row></grid>')


def status_in(*names):
    vals = "".join(f"<value>{ST[n]}</value>" for n in names)
    return f'<condition attribute="sams_status" operator="in">{vals}</condition>'


def existing_view(table, querytype, default_only=False):
    flt = f"returnedtypecode%20eq%20'{table}'%20and%20querytype%20eq%20{querytype}"
    if default_only:
        flt += "%20and%20isdefault%20eq%20true"
    status, payload, _ = call("GET", f"savedqueries?$select=savedqueryid,name&$filter={flt}", solution=False)
    ok(status, payload, f"find views {table}/{querytype}")
    return payload["value"]


def build_views(uc_code, sys_code):
    views = {}
    # Default public + quick find + associated: update the system-generated ones
    for table, code, cols, qf, name in [
        (UC, uc_code, UC_COLS, ["sams_name", "sams_usecasenumber", "sams_submitteremail"], "Active Agentic Use Cases"),
        (SYS, sys_code, SYS_COLS, ["sams_name"], "Active Target Systems"),
    ]:
        default = existing_view(table, 0, default_only=True)[0]
        ok(*call("PATCH", f"savedqueries({default['savedqueryid']})",
                 {"fetchxml": fetch(table, cols), "layoutxml": layout(table, code, cols)})[:2], f"view {name}")
        views[f"{table}:default"] = default["savedqueryid"]
        for v in existing_view(table, 4):
            # The platform rejects fetchxml updates on quick find views via Web API (0x80040216); layout only.
            status, payload, _ = call("PATCH", f"savedqueries({v['savedqueryid']})",
                                      {"layoutxml": layout(table, code, cols[:5])}, retries=0)
            print(f"[{'OK' if status < 300 else 'WARN'}]   quick find layout {table}")
    assoc = existing_view(SYS, 2)[0]
    assoc_cols = SYS_COLS[:4]
    ok(*call("PATCH", f"savedqueries({assoc['savedqueryid']})",
             {"fetchxml": fetch(SYS, assoc_cols, order=("sams_name", False)), "layoutxml": layout(SYS, sys_code, assoc_cols)})[:2],
       "associated view target systems")
    views["sys:assoc"] = assoc["savedqueryid"]

    custom = [
        ("New Submissions", status_in("Submitted"), ("createdon", True)),
        ("Awaiting Review", status_in("Submitted", "InReview"), ("createdon", False)),
        ("Needs Info", status_in("NeedsInfo"), ("modifiedon", True)),
        ("Approved Portfolio", status_in("Approved", "InBuild", "Live"), ("sams_priorityscore", True)),
        ("Declined", status_in("Declined"), ("modifiedon", True)),
        ("High Credit Band", f'<condition attribute="sams_creditband" operator="eq" value="{V + 3}" />', ("sams_estimatedmonthlycredits", True)),
        ("External Facing", f'<condition attribute="sams_audience" operator="in"><value>{V + 1}</value><value>{V + 2}</value></condition>', ("createdon", True)),
        ("By Priority", "", ("sams_priorityscore", True)),
    ]
    for name, cond, order in custom:
        vid = gid(f"view:{name}")
        upsert("savedqueries", "savedqueryid", vid, {
            "name": name, "returnedtypecode": UC, "querytype": 0, "isdefault": False, "isquickfindquery": False,
            "fetchxml": fetch(UC, UC_COLS, cond, order), "layoutxml": layout(UC, uc_code, UC_COLS),
        }, f"view {name}")
        views[name] = vid
    return views


# ---------------------------------------------------------------- charts
PALETTE = "0,120,212; 0,153,188; 135,100,184; 227,0,140; 255,140,0; 16,124,16; 164,38,44; 105,121,126"


def chart_data(table, group_attr, date_grouping=None):
    dg = f' dategrouping="{date_grouping}"' if date_grouping else ""
    return (f'<datadefinition><fetchcollection><fetch mapping="logical" aggregate="true"><entity name="{table}">'
            f'<attribute groupby="true" alias="groupby_column" name="{group_attr}"{dg} />'
            f'<attribute alias="aggregate_column" name="{table}id" aggregate="count" />'
            f'</entity></fetch></fetchcollection><categorycollection><category alias="groupby_column">'
            f'<measurecollection><measure alias="aggregate_column" /></measurecollection></category>'
            f'</categorycollection></datadefinition>')


def chart_presentation(kind):
    axis = ('<AxisY LabelAutoFitMinFontSize="8" TitleForeColor="59, 59, 59" TitleFont="{0}, 10.5px" LineColor="165, 172, 181" IntervalAutoMode="VariableCount">'
            '<MajorGrid LineColor="239, 242, 246" /><MajorTickMark LineColor="165, 172, 181" /><LabelStyle Font="{0}, 10.5px" ForeColor="59, 59, 59" /></AxisY>'
            '<AxisX LabelAutoFitMinFontSize="8" TitleForeColor="59, 59, 59" TitleFont="{0}, 10.5px" LineColor="165, 172, 181" IntervalAutoMode="VariableCount">'
            '<MajorTickMark LineColor="165, 172, 181" /><MajorGrid LineColor="Transparent" /><LabelStyle Font="{0}, 10.5px" ForeColor="59, 59, 59" /></AxisX>')
    if kind == "Pie":
        series = ('<Series ChartType="Doughnut" IsValueShownAsLabel="True" Font="{0}, 9.5px" LabelForeColor="59, 59, 59" '
                  'CustomProperties="PieLabelStyle=Inside, PieDrawingStyle=Default, DoughnutRadius=60"><SmartLabelStyle Enabled="True" /></Series>')
        legend = '<Legends><Legend Alignment="Center" LegendStyle="Table" Docking="right" IsEquallySpacedItems="True" Font="{0}, 11px" ShadowColor="0, 0, 0, 0" ForeColor="59, 59, 59" /></Legends>'
        area = '<ChartArea BorderColor="White" BorderDashStyle="Solid" />'
    else:
        series = (f'<Series ChartType="{kind}" IsValueShownAsLabel="True" Font="{{0}}, 9.5px" LabelForeColor="59, 59, 59" '
                  f'Color="0, 120, 212" BorderWidth="3" CustomProperties="PointWidth=0.75, MaxPixelPointWidth=40"><SmartLabelStyle Enabled="True" /></Series>')
        legend = ""
        area = f'<ChartArea BorderColor="White" BorderDashStyle="Solid">{axis}</ChartArea>'
    return (f'<Chart Palette="None" PaletteCustomColors="{PALETTE}"><Series>{series}</Series><ChartAreas>{area}</ChartAreas>'
            f'<Titles><Title Alignment="TopLeft" DockingOffset="-3" Font="{{0}}, 13px" ForeColor="59, 59, 59"></Title></Titles>{legend}</Chart>')


CHARTS = [
    ("Use Cases by Status", UC, "sams_status", "Column", None),
    ("Use Cases by Recommended Tool", UC, "sams_recommendedtool", "Bar", None),
    ("Use Cases by Credit Band", UC, "sams_creditband", "Pie", None),
    ("Use Cases by Audience", UC, "sams_audience", "Pie", None),
    ("Submissions per Week", UC, "createdon", "Line", "week"),
    ("Target Systems by Type", SYS, "sams_systemtype", "Bar", None),
]


def build_charts():
    ids = {}
    for name, table, attr, kind, dg in CHARTS:
        cid = gid(f"chart:{name}")
        upsert("savedqueryvisualizations", "savedqueryvisualizationid", cid, {
            "name": name, "primaryentitytypecode": table, "isdefault": False,
            "datadescription": chart_data(table, attr, dg), "presentationdescription": chart_presentation(kind),
        }, f"chart {name}")
        ids[name] = cid
    return ids


# ---------------------------------------------------------------- dashboard
def dash_cell(title, target, view_id, chart_id=None, colspan=1, rowspan=12):
    mode = "Chart" if chart_id else "Grid"
    vis = f"<VisualizationId>{brace(chart_id)}</VisualizationId>" if chart_id else "<VisualizationId />"
    return (f'<cell id="{g()}" showlabel="false" rowspan="{rowspan}" colspan="{colspan}" auto="false">{label_xml(title)}'
            f'<control id="{target}_{uuid.uuid4().hex[:8]}" classid="{CLASSID["subgrid"]}"><parameters>'
            f'<ViewId>{brace(view_id)}</ViewId><IsUserView>false</IsUserView><RelationshipName /><TargetEntityType>{target}</TargetEntityType>'
            f'<AutoExpand>Fixed</AutoExpand><EnableQuickFind>false</EnableQuickFind><EnableViewPicker>false</EnableViewPicker>'
            f'<EnableJumpBar>false</EnableJumpBar><ChartGridMode>{mode}</ChartGridMode>{vis}<IsUserChart>false</IsUserChart>'
            f'<EnableChartPicker>false</EnableChartPicker><RecordsPerPage>10</RecordsPerPage></parameters></control></cell>')


def build_dashboard(views, charts):
    uc_all = views[f"{UC}:default"]
    sys_all = views[f"{SYS}:default"]
    blank = "<row />" * 11
    rows = [
        "<row>" + dash_cell("Use Cases by Status", UC, uc_all, charts["Use Cases by Status"]) +
        dash_cell("Use Cases by Recommended Tool", UC, uc_all, charts["Use Cases by Recommended Tool"]) +
        dash_cell("Use Cases by Credit Band", UC, uc_all, charts["Use Cases by Credit Band"]) + "</row>" + blank,
        "<row>" + dash_cell("Use Cases by Audience", UC, uc_all, charts["Use Cases by Audience"]) +
        dash_cell("Submissions per Week", UC, uc_all, charts["Submissions per Week"]) +
        dash_cell("Target Systems by Type", SYS, sys_all, charts["Target Systems by Type"]) + "</row>" + blank,
        "<row>" + dash_cell("New Submissions", UC, views["New Submissions"], colspan=3) + "</row>" + blank,
    ]
    xml = (f'<form><tabs><tab name="Overview" id="{g()}" verticallayout="true" showlabel="false">{label_xml("Overview")}'
           f'<columns><column width="100%"><sections><section name="Overview" showlabel="false" showbar="false" columns="111" '
           f'id="{g()}">{label_xml("Overview")}<rows>{"".join(rows)}</rows></section></sections></column>'
           f'</columns></tab></tabs></form>')
    did = gid("dashboard:overview")
    upsert("systemforms", "formid", did, {
        "name": "Agentic Use Case Overview", "description": "Pipeline of agentic use case ideas: status, tools, credit bands and systems.",
        "type": 0, "formxml": xml,
    }, "dashboard Agentic Use Case Overview")
    return did


# ---------------------------------------------------------------- app + site map
APP_NAME = "Agentic Use Case Hub"
APP_UNIQUE = "sams_AgenticUseCaseHub"


def list_url(view_id):
    return f"/main.aspx?pagetype=entitylist&amp;etn={UC}&amp;viewid=%7b{view_id}%7d&amp;viewtype=1039"


def sitemap_xml(dashboard_id, views):
    def sub(sid, title, attrs):
        return f'<SubArea Id="{sid}" {attrs}><Titles><Title LCID="1033" Title="{escape(title)}" /></Titles></SubArea>'

    def group(gid_, title, subs):
        return f'<Group Id="{gid_}" IsProfile="false"><Titles><Title LCID="1033" Title="{escape(title)}" /></Titles>{"".join(subs)}</Group>'

    return (
        '<SiteMap IntroducedVersion="7.0.0.0"><Area Id="sams_area_intake" ShowGroups="true">'
        '<Titles><Title LCID="1033" Title="Agentic Use Cases" /></Titles>'
        + group("sams_grp_overview", "Overview", [
            sub("sams_sa_dashboard", "Dashboard", f'DefaultDashboard="{brace(dashboard_id)}" Url="/workplace/home_dashboards.aspx" '
                'Client="All,Outlook,OutlookLaptopClient,OutlookWorkstationClient,Web" AvailableOffline="true"'),
        ])
        + group("sams_grp_intake", "Intake", [
            sub("sams_sa_all", "All Use Cases", f'Entity="{UC}"'),
            sub("sams_sa_new", "New Submissions", f'Url="{list_url(views["New Submissions"])}"'),
            sub("sams_sa_review", "Awaiting Review", f'Url="{list_url(views["Awaiting Review"])}"'),
            sub("sams_sa_needsinfo", "Needs Info", f'Url="{list_url(views["Needs Info"])}"'),
        ])
        + group("sams_grp_portfolio", "Portfolio", [
            sub("sams_sa_approved", "Approved Portfolio", f'Url="{list_url(views["Approved Portfolio"])}"'),
            sub("sams_sa_priority", "By Priority", f'Url="{list_url(views["By Priority"])}"'),
        ])
        + group("sams_grp_reference", "Reference", [
            sub("sams_sa_systems", "Target Systems", f'Entity="{SYS}"'),
        ])
        + "</Area></SiteMap>"
    )


def find_app():
    flt = f"$select=appmoduleid,uniquename,name&$filter=name%20eq%20'{APP_NAME.replace(' ', '%20')}'"
    for path in (f"appmodules?{flt}", f"appmodules/Microsoft.Dynamics.CRM.RetrieveUnpublishedMultiple()?{flt}"):
        status, payload, _ = call("GET", path, solution=False)
        if status == 200 and payload["value"]:
            return payload["value"][0]
    return None


def build_app(dashboard_id, views, entity_ids, form_ids, chart_ids):
    app = find_app()
    if not app:
        env = dict(os.environ, TERM="dumb")
        out = subprocess.run(["pac", "model", "create", "--name", APP_NAME, "--solution", SOLUTION,
                              "--description", "Back-office hub to triage and manage agentic use case ideas."],
                             capture_output=True, text=True, env=env, shell=True)
        print(out.stdout.strip()[-400:], out.stderr.strip()[-400:])
        app = find_app()
        if not app:
            raise SystemExit("[FAIL] app not created")
        print(f"[OK]   app {APP_NAME} created")
    app_id = app["appmoduleid"]

    # Site map: an app site map shares the app's unique name (pac model create makes one)
    sm_id = None
    status, payload, _ = call("GET", "sitemaps/Microsoft.Dynamics.CRM.RetrieveUnpublishedMultiple()?$select=sitemapid,"
                              f"sitemapnameunique&$filter=sitemapnameunique%20eq%20'{app['uniquename']}'", solution=False)
    if status == 200 and payload["value"]:
        sm_id = payload["value"][0]["sitemapid"]
        ok(*call("PATCH", f"sitemaps({sm_id})", {"sitemapxml": sitemap_xml(dashboard_id, views)})[:2], "site map")
    else:
        sm_id = gid("sitemap:hub")
        upsert("sitemaps", "sitemapid", sm_id, {
            "sitemapname": APP_NAME, "sitemapnameunique": app["uniquename"], "isappaware": True,
            "sitemapxml": sitemap_xml(dashboard_id, views),
        }, "site map")

    components = [{"@odata.type": "Microsoft.Dynamics.CRM.sitemap", "sitemapid": sm_id},
                  {"@odata.type": "Microsoft.Dynamics.CRM.systemform", "formid": dashboard_id}]
    components += [{"@odata.type": "Microsoft.Dynamics.CRM.entity", "entityid": e} for e in entity_ids]
    components += [{"@odata.type": "Microsoft.Dynamics.CRM.systemform", "formid": f} for f in form_ids]
    components += [{"@odata.type": "Microsoft.Dynamics.CRM.savedquery", "savedqueryid": v} for v in views.values()]
    components += [{"@odata.type": "Microsoft.Dynamics.CRM.savedqueryvisualization", "savedqueryvisualizationid": c}
                   for c in chart_ids]
    ok(*call("POST", "AddAppComponents", {"AppId": app_id, "Components": components}, solution=False)[:2], "app components")

    status, payload, _ = call("GET", f"ValidateApp(AppModuleId={app_id})", solution=False)
    ok(status, payload, "validate app")
    resp = payload.get("AppValidationResponse", {})
    for issue in resp.get("ValidationIssueList", []):
        print(f"       {issue.get('ErrorType')}: {issue.get('Message')}")
    return app_id


def publish(app_id, dashboard_id):
    xml = (f"<importexportxml><entities><entity>{UC}</entity><entity>{SYS}</entity></entities>"
           f"<dashboards><dashboard>{brace(dashboard_id)}</dashboard></dashboards>"
           f"<appmodules><appmodule>{app_id}</appmodule></appmodules></importexportxml>")
    ok(*call("POST", "PublishXml", {"ParameterXml": xml}, solution=False)[:2], "publish")


def add_to_solution(object_id, ctype):
    call("POST", "AddSolutionComponent", {"ComponentId": object_id, "ComponentType": ctype, "SolutionUniqueName": SOLUTION,
                                          "AddRequiredComponents": False, "DoNotIncludeSubcomponents": False}, solution=False)


if __name__ == "__main__":
    uc_code, uc_meta = otc(UC)
    sys_code, sys_meta = otc(SYS)
    views = build_views(uc_code, sys_code)
    uc_form = build_usecase_form(views["sys:assoc"])
    sys_form = build_system_form()
    charts = build_charts()
    dashboard = build_dashboard(views, charts)
    for vid in views.values():
        add_to_solution(vid, 26)
    for cid in charts.values():
        add_to_solution(cid, 59)
    for fid in (uc_form, sys_form, dashboard):
        add_to_solution(fid, 60)
    app_id = build_app(dashboard, views, [uc_meta, sys_meta], [uc_form, sys_form], list(charts.values()))
    publish(app_id, dashboard)
    print(f"Done. App id: {app_id}")
