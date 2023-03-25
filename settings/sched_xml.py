import dicttoxml as dtx
from init import archive_schedule as sched

# TODO: Template for generating xml files according to the task scheduler schema
xml_schema = {
    'task': {
        'principal-key': {
            'selector': None, # selector field
            'field': None # user(?) id field
        },
        'context-key-ref': {
            'selector': None, # selector field
            'field': None, # context field
        },
        'unique-id': {
            'selector': None, # selector field related to triggers
            'field': None # unique event id
        }
    }
}

def generate(value):
    # TODO: code that confirms the XML is valid to the task scheduler schema
    return dtx.dicttoxml(value)

# Generate XML files for schtasks.exe to run
if (__name__ == '__main__'):
    xml = generate(sched.schedule_config().sched_opts)
