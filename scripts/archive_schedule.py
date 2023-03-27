from vba_schedule.models import BASE_SCHED_OPTS
from vba_schedule.vba_schedule import vba_schedule as vbas
from copy import deepcopy
import subprocess
import datetime
import os

# initialize a base vba_schedule to manage vba download schedules
def init_vbas() -> vbas:
    ret_vb = vbas()
    ret_vb.copy_sched(init_schedule())
    return ret_vb

# initialize a base schedule config for users to interface with
def init_schedule() -> dict:
    schedule = deepcopy(BASE_SCHED_OPTS)
    init_date = datetime.datetime.now()
    for key in schedule.keys():
        try:
            if key == 'date':
                schedule[key] = init_date.isoformat()
            if key == 'author':
                schedule[key] = os.getenv('username')
            if key == 'URI':
                schedule[key] = '\\vb_archiver'
            if key == 'triggers':
                schedule[key] = {
                    'calendar-trigger': {
                            'start-boundary': init_date.isoformat(),
                            'end-boundary': (init_date + datetime.timedelta(minutes=1)).isoformat(),
                            'repetition': {
                                'interval': 'P1M'
                            }
                        }
                }
            if key == 'user-id':
                schedule[key] = 'S-1-5-18' # Windows Task Scheduler SYSTEM user-id
            if key == 'command':
                schedule[key] = os.path.abspath(os.path.dirname(__file__)) # this file is in the same dir as archive.bat
        except:
            raise
    return schedule

# Make a video archive schedule
def start_schedule(task_name, xml_path):
    task_command = ['schtasks.exe',
                    '/Create',
                    '/RU', 'SYSTEM',
                    '/TN', task_name,
                    '/XML', xml_path]
    subprocess.run(task_command)

# Export data to be used in another file
def contents(vbas: vbas) -> dict: # receive vbas object to dissect contents and export ydl command?
    output_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../dldest/filenames.txt') )
    url = 'https://www.twitch.tv/northbaysmash/videos?filter=highlights&sort=time'
    args = [
        'youtube-dl',
        url,
        '--config-location', os.path.abspath(
            os.path.join(os.path.split(os.path.dirname(__file__))[0],
                    './settings/ytdl.conf')),
        '--yes-playlist']
    return {'args': args, 'output_path': output_path}


current = vbas()

if (__name__ == '__main__'):
    print(current)
    start_schedule('vb-archiver', os.path.abspath( os.path.join(os.path.split(os.path.dirname(__file__))[0], './settings/xml/vb_archiver.xml') ))
