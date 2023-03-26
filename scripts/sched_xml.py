import dicttoxml as dtx
import archive_schedule as sched
from schema import Schema, And, Or, Use, Optional
import os
import re

# https://stackoverflow.com/questions/66140495/python-how-to-check-the-string-is-a-utc-timestamp
# regex pattern to confirm ISO8601 format conformity from time strings,
# validates "yyyy-(m)m-(d)dT(h)h:(m)m:(s)s.s(ssssss)"
DATETIME_ISO8601 = re.compile(
    r'^([0-9]{4})' r'-' r'([0-9]{1,2})' r'-' r'([0-9]{1,2})' # date
    r'([T\s][0-9]{1,2}:[0-9]{1,2}:?[0-9]{1,2}(\.[0-9]{1,7})?)?' # time
)

# TODO: Template for generating xml files according to the task scheduler schema
XML_SCHEMA = Schema({
                'task': {
                    'registration-info': {
                        'date': And(str, lambda date: bool(re.fullmatch(date, DATETIME_ISO8601))), # task creation date is in ISO8601 Time Format
                        'author': str, # task author
                        'URI': str, # identifier for the task
                    },
                    'triggers': {
                        str: {}
                    },
                    'principals': {
                        'principal': {
                            'user-id': str # user id under whose permissions the task will be run
                        }
                    },
                    'settings': {
                        Optional('enabled', default=True): bool, # enable the task to run when triggered
                        Optional('allow-start-on-demand', default=True): bool, # allow the user to run the program on demand
                        Optional('allow-hard-terminate', default=True): bool # allow the user to end the task while it is running
                    },
                    'actions': {
                        'exec': {
                            'command': And(str, lambda cmdPath: os.path.exists(cmdPath)) # the command to be executed by the windows task scheduler
                        }
                    }
                }
            })

def generateXML(xml_dict):
    # TODO: code that confirms the XML is valid to the task scheduler schema
    return dtx.dicttoxml(XML_SCHEMA.validate(xml_dict))

# Generate XML files for schtasks.exe to run
if (__name__ == '__main__'):
    xml_dict = sched.schedule_config().sched_profile()
    print(xml_dict)
    xml = generateXML(xml_dict)
