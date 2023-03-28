import dicttoxml as dtx
from xml.dom.minidom import parseString
from vba_schedule.models import XML_SCHEMA

# TODO: Template for generating xml files according to the task scheduler schema

def generatexml(sched_dict: dict, pretty=False):
    camelcase = lambda hyphen_str: (''.join([s.capitalize() for s in hyphen_str.replace('-',' ').split()])).replace('Uri', 'URI')
    xml_dict = {key: value for key, value in XML_SCHEMA.validate(sched_dict).modified_items(modify_key=camelcase)}
    try:
        ret_xml = dtx.dicttoxml((xml_dict),
                                custom_root='Task',
                                attr_type=False)
    except:
        raise
    if pretty:
        xml_string = parseString(ret_xml)
        xml_string = xml_string.toprettyxml().replace(
            '<Task>',
            '<Task version=\"1.2\" xmlns=\"http://schemas.microsoft.com/windows/2004/02/mit/task\">')
        xml_string = xml_string.replace(
            '<?xml version=\"1.0\" ?>',
            '<?xml version=\"1.0\" encoding=\"UTF-16\"?>'
        )
        return xml_string
    return ret_xml

# Generate XML files for schtasks.exe to run
if (__name__ == '__main__'):
    pass
