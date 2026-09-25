import json
import os
import sys
import urllib.parse

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from create_schema import call  # noqa: E402

SCHEMA_NAMES = [
    'sams_IntakeAgentUrl',
    'sams_ToolGuideUrl',
    'sams_CreditsGuideUrl',
]


def _first_value(payload):
    values = payload.get('value') if isinstance(payload, dict) else None
    return values[0] if values else None


def read_env_var(schema_name):
    query = urllib.parse.quote(f"schemaname eq '{schema_name}'")
    path = (
        'environmentvariabledefinitions?'
        '$select=environmentvariabledefinitionid,schemaname,defaultvalue'
        f'&$filter={query}'
    )
    status, payload, _ = call('GET', path, solution=False)
    if status >= 300:
        raise RuntimeError(f'Failed to read definition {schema_name}: HTTP {status} {payload}')

    definition = _first_value(payload)
    if not definition:
        return ''

    definition_id = definition['environmentvariabledefinitionid']
    value_filter = urllib.parse.quote(f'_environmentvariabledefinitionid_value eq {definition_id}')
    value_path = f'environmentvariablevalues?$select=value&$filter={value_filter}&$top=1'
    status, value_payload, _ = call('GET', value_path, solution=False)
    if status >= 300:
        raise RuntimeError(f'Failed to read value {schema_name}: HTTP {status} {value_payload}')

    value_row = _first_value(value_payload)
    if value_row and value_row.get('value'):
        return value_row['value']
    return definition.get('defaultvalue') or ''


def main():
    result = {schema_name: read_env_var(schema_name) for schema_name in SCHEMA_NAMES}
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
