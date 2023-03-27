import dicttoxml as dtx
import archive_schedule as sched
from vba_schedule.models import XML_SCHEMA

# TODO: Template for generating xml files according to the task scheduler schema


def generateXML(xml_dict):
    # TODO: code that confirms the XML is valid to the task scheduler schema
    try:
        ret_xml = dtx.dicttoxml(XML_SCHEMA.validate(xml_dict))
    except:
        raise
    return ret_xml

# Generate XML files for schtasks.exe to run
if (__name__ == '__main__'):
    xml_dict = sched.current.sched_profile()
    xml = generateXML(xml_dict)
