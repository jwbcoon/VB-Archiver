import dicttoxml as dtx
from xml.dom.minidom import parseString
from vba_schedule.models import XML_SCHEMA

# TODO: Template for generating xml files according to the task scheduler schema

# changes a hyphenated string parameter and converts it to camel case
def camelcase(hyphen_str: str):
    return ''.join([s.capitalize() for s in hyphen_str.replace('-',' ').split()])

# generate a dictionary copy with modified keys to conform to Windows Task Scheduler XML
def recursive_items(dictionary):
    for key, value in dictionary.items():
        camelkey = camelcase(key)
        if type(value) is dict:
            nestval = ({k: v for k, v in recursive_items(value)})
            yield (camelkey, nestval)
        elif (type(value) is list or type(value) is tuple) and type(value) is not str:
            for ele in value:
                if type(ele) is dict:
                    elnestval = ({k: v for k, v in recursive_items(ele)})
                    yield (camelkey, elnestval)
        else:
            yield (camelkey, value)

def generatexml(sched_dict: dict, pretty=False):
    xml_dict = {key: value for key, value in recursive_items(sched_dict)}
    if xml_dict['RegistrationInfo'].get('Uri'): # This if statment feels like a bad fix
        xml_dict['RegistrationInfo']['URI'] = xml_dict['RegistrationInfo'].pop('Uri')
    try:
        ret_xml = dtx.dicttoxml(xml_dict,
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
