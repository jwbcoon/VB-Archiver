from lib.models import BASE_SCHED_OPTS, SYSTEM_ID, XML_SCHEMA
from lib.vba_schedule import vba_schedule as vbas
from copy import deepcopy
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
    schedule = deepcopy(BASE_SCHED_OPTS)
    init_date = dt.datetime.now()
    for outer_key in schedule.keys(): # "task" key always points to a set of dict values
        if outer_key == 'registration-info':
            for config_key in schedule[outer_key].keys():
                try:
                    if config_key == 'date':
                        schedule[outer_key][config_key] = init_date.isoformat()
                    if config_key == 'author':
                        schedule[outer_key][config_key] = os.getenv('username')
                    if config_key == 'URI':
                        schedule[outer_key][config_key] = 'vb_archiver'
                except:
                    raise
        if outer_key == 'triggers':
            schedule[outer_key] = {
                'calendar-trigger': {
                        'start-boundary': init_date.isoformat(),
                        'end-boundary': (init_date + dt.timedelta(minutes=1)).isoformat(),
                        'repetition': {
                            'interval': 'PT1M' # maybe use regex to generate time in this format?
                        }
                    }
            }
        if outer_key == 'principals':
            schedule[outer_key][0]['principal']['user-id'] = SYSTEM_ID # Windows Task Scheduler SYSTEM user-id
        if outer_key == 'actions':
            schedule[outer_key]['exec']['command'] = os.path.abspath(
                os.path.join(os.path.dirname(__file__), './scripts/archive.bat')) # this file is in the same dir as archive.bat
        
    return schedule


def generatexml(sched_dict: dict, pretty=False):
    camelcase = lambda hyphen_str: (''.join([s.capitalize() for s in hyphen_str.replace('-',' ').split()])).replace('Uri', 'URI')
    xml_dict = XML_SCHEMA.validate(sched_dict).modified_dict(modify_key=camelcase)
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

# Make a video archive schedule
def start_schedule(task_name, xml_file):
    task_command = ['schtasks.exe',
                    '/Create',
                    '/RU', 'SYSTEM',
                    '/TN', task_name,
                    '/XML', xml_file]
    subprocess.run(task_command)

# Export data to be used in another file
def contents(vbas: vbas) -> dict: # receive vbas object to dissect contents and export ydl command?
    output_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../dldest/filenames.txt') )
    vbas.url = 'https://www.twitch.tv/northbaysmash/videos?filter=highlights&sort=time'
    args = [
        'youtube-dl',
        vbas.url,
        '--config-location', os.path.abspath(
            os.path.join(os.path.split(os.path.dirname(__file__))[0],
                    './settings/ytdl.conf')),
        '--yes-playlist']
    return {'args': args, 'output_path': output_path}


current = init_vbas()

if (__name__ == '__main__'):
    print(generatexml(current.sched_profile(), pretty=True))
    #start_schedule('vb-archiver', os.path.abspath( os.path.join(os.path.split(os.path.dirname(__file__))[0], './settings/xml/vb_archiver.xml') ))
