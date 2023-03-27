import subprocess
from vba_schedule import vba_schedule as vbas
import os

# Make a video archive schedule
def make_schedule(task_name, xml_path):
    task_command = ['schtasks.exe',
                    '/Create',
                    '/RU', 'SYSTEM',
                    '/TN', task_name,
                    '/XML', xml_path]
    subprocess.run(task_command)

# Export data to be used in another file
def contents(vbas: vbas): # receive vbas object to dissect contents and export ydl command?
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
    make_schedule('vb-archiver', os.path.abspath( os.path.join(os.path.split(os.path.dirname(__file__))[0], './settings/xml/vb_archiver.xml') ))
