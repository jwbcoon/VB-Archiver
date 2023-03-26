import dicttoxml as dtx
from init import archive_schedule as sched
from schema import Schema, And, Or, Use, Optional

# TODO: Template for generating xml files according to the task scheduler schema
xml_schema = Schema({
                'task': {
                    'registration-info': {
                        'date': None, # task creation date
                        'author': None, # task author
                        'URI': None, # identifier for the task
                    },
                    'triggers': {},
                    'principals': {
                        'principal': {
                            'user-id': None # user id under whose permissions the task will be run
                        }
                    },
                    'settings': {
                        'enabled': True, # enable the task to run when triggered
                        'allow-start-on-demand': True, # allow the user to run the program on demand
                        'allow-hard-terminate': True # allow the user to end the task while it is running
                    },
                    'actions': {
                        'exec': {
                            'command': None # the command to be executed by the windows task scheduler
                        }
                    }
                }
            })

def generateXML(xmlDict):
    # TODO: code that confirms the XML is valid to the task scheduler schema
    return dtx.dicttoxml(xmlDict)

# Generate XML files for schtasks.exe to run
if (__name__ == '__main__'):
    xml = generateXML(sched.schedule_config().sched_profile())
