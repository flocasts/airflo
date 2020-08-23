# coding=utf-8
from copy import deepcopy
from re import match, sub


def merge_dict(base, other):
    """Merge dict objects."""
    base.update(other or {})
    return base


def parse_ddl_from_dict(input_dictionary):
    """Create a table using an input dictionary.

    dict format:
    {
        <schema>: {
                <table>: {
                    <pk>: <list of field_names that make up primary key>,
                    <fields>: <list of {'name': <field_name>, 'type': <field_type>}
                               where field_type is a valid SQL type>,
                }
            }
    }

    :param input_dictionary: dict of appropriate format
    :return: ddl str value based on provided dict
    """
    unparsed_schema = list(input_dictionary.keys())[0]
    unparsed_table = list(input_dictionary[unparsed_schema].keys())[0]
    table_dict = input_dictionary[unparsed_schema][unparsed_table]
    schema = unparsed_schema.upper()
    table = unparsed_table.upper()
    unparsed_fields = deepcopy(table_dict['fields'])
    fields = [merge_dict(f, parse_field_name_and_type(f['name'], f['type'], escape=f.get('escape', False)))
              for f in unparsed_fields]
    pkey = table_dict.get('pk', [])
    column_creation_statement = ','.join(
        '{0} {1}'.format(field['name'], field['type'])
        for field in fields
    )
    pkey_statement = ', PRIMARY KEY ({0})'.format(','.join(pk for pk in pkey)) if pkey else ''
    return "CREATE TABLE IF NOT EXISTS {0}.{1} ({2})".format(
        schema,
        table,
        column_creation_statement + pkey_statement
    )


def parse_field_name_and_type(fname, ftype, escape=False):
    """Parse field metadata and return sanitized format."""
    unescaped_field = sub(r'^(?:\d+)_(?:.*)', r'\2_\1', fname) if match(r'^(?:\d+)_(?:.*)', fname) else fname
    corrected_field = '"{0}"'.format(unescaped_field) if escape else unescaped_field
    corrected_field_type = ftype.upper()
    type_mapper = {
        'INT': 'NUMBER(38,0)',
        'TIMESTAMP': 'TIMESTAMP_NTZ(9)',
        'VARCHAR': 'VARCHAR(16777216)',
        'TEXT': 'VARCHAR(16777216)'
    }

    for k, v in type_mapper.items():
        if corrected_field_type.startswith(k):
            corrected_field_type = v
            break
    return {'name': corrected_field, 'type': corrected_field_type, 'unescaped_name': unescaped_field}
