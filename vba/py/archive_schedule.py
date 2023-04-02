from vba.py.lib.models import BASE_SCHED_OPTS, SYSTEM_ID, XML_SCHEMA
from vba.py.lib.vba_schedule import vba_schedule as vbas
from vba.py.lib.deepdict import deepdict
from xml.dom.minidom import parseString
import dicttoxml as dtx
import subprocess
import datetime as dt
import os

# initialize a base vba_schedule to manage vba download schedules
def init_vbas() -> vbas:
    ret_vb = vbas()
    ret_vb.copy_sched(init_schedule())
    return ret_vb

# initialize a base schedule config for users to interface with
def init_schedule() -> dict:
    def init_values(date=dt.datetime.now(), k=None, v=None):
        if k == 'date':
            return date.isoformat()
        if k == 'author':
            return os.getenv('username')
        if k == 'URI':
            return 'vb_archiver'
        if k == 'start-boundary':
            return date.isoformat()
        if k == 'end-boundary':
            return (date + dt.timedelta(minutes=1)).isoformat()
        if k == 'interval':
            return 'PT1M'
        if k == 'user-id':
            return SYSTEM_ID # Windows Task Scheduler SYSTEM user-id
        if k == 'command':
            return os.path.abspath(
                os.path.join(os.path.dirname(__file__), './scripts/archive.bat')) # this file is in the same dir as archive.bat
        return v

    schedule = BASE_SCHED_OPTS.conditional_copy(
        value_conditional=lambda k, v: k in BASE_SCHED_OPTS.flat_keys(),
        value_true=init_values,
        two_value_args=True)
        
    return schedule

'''
Receive dict object as a parameter and convert it to an XML string. Use keywords
write and pretty to control whether files are written with this XML and to enable
whitespace in the XML string.
'''
def generatexml(sched_dict: deepdict, write=False, pretty=False):
    camelcase = lambda hyphen_str: (''.join([s.capitalize() for s in hyphen_str.replace('-',' ').split()])).replace('Uri', 'URI')
    xml_dict = XML_SCHEMA.validate(sched_dict).modified_copy(modify_key=camelcase)
    try:
        xml_bytes = dtx.dicttoxml(xml_dict,
                                custom_root='Task',
                                attr_type=False)
    except:
        raise

    xml_string = parseString(xml_bytes)
    xml_string = xml_string.toprettyxml() if pretty else xml_string.toxml()
    xml_string = xml_string.replace(
            '<Task>',
            '<Task version=\"1.2\" xmlns=\"http://schemas.microsoft.com/windows/2004/02/mit/task\">'
            ).replace(
            '<?xml version=\"1.0\" ?>',
            '<?xml version=\"1.0\" encoding=\"UTF-16\"?>' )
        
    if write:
        try:
            with open(os.path.abspath(os.path.join(os.path.split(os.path.dirname(__file__))[0],
                    './settings/xml/{}'.format((sched_dict['registration-info']['URI']) + '.xml'))),
                    'wb') as file:
                file.write(xml_string.encode('utf-16'))
        except:
            raise

    return xml_string

# Make a video archive schedule
def start_schedule(task_name, xml_file):
    task_command = ['schtasks.exe',
                    '/Create',
                    '/RU', 'SYSTEM',
                    '/TN', task_name,
                    '/XML', xml_file]
    subprocess.run(task_command)

# Export data to be used in another file
def contents(vb: vbas) -> dict: # receive vbas object to dissect contents and export ydl command?
    output_path = os.path.abspath( os.path.join(os.path.dirname(__file__), '../../dldest/filenames.txt') )

    # when fully implemented, this line of code should not exist, the attribute should be in the param
    vb.url = 'https://www.twitch.tv/northbaysmash/videos?filter=highlights&sort=time'

    # generator gives an item from ydl_opts.modified_copy() such that {'key':'value'} -> {'--key':'value'}
    ydl_opts = vb.ydl_opts.modified_copy(modify_key=lambda key: '--' + key)

    # first two arguments of command are the ydl command and destination url
    args = ['youtube-dl', vb.url]

    # add each key:value pair in order to match options with their arguments
    args.extend(item for tup in zip(ydl_opts.keys(), ydl_opts.values()) for item in tup)

    return {'args': args, 'output_path': output_path}


current = init_vbas()

if __name__ == '__main__':
    print(generatexml(current.sched_opts, pretty=True))
    #start_schedule('vb-archiver', os.path.abspath( os.path.join(os.path.split(os.path.dirname(__file__))[0], './settings/xml/vb_archiver.xml') ))
