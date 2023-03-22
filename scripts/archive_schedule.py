import subprocess
import archiver
import os

'''
download_schedules objects are pairs of configurations as dicts:
    the download config
        and
    the schedule config
'''
class download_schedule(tuple(ytdl_conf=dict, sched_conf=dict)):
    def __init__(self) -> None:
        pass

    # Return a schedule dict object to be converted to XML for schtasks.exe
    def profile():
        return 0

    # Make a video archive schedule
    def make_schedule(username, password):
        xml_path = os.path.abspath(
            os.path.join(os.path.split(os.path.dirname(archiver.__file__))[0],
                        './settings/xml/vb_archiver.xml'))
        task_name = 'vb_archiver'
        task_command = ['schtasks.exe',
                        '/Create',
                        '/RU', username,
                        '/RP', password,
                        '/TN', task_name,
                        '/XML', xml_path]
        subprocess.run(task_command)

    # Export data to be used in another file
    def contents():
        output_path = os.path.abspath(
            os.path.join(os.path.dirname(archiver.__file__), '../dldest/filenames.txt') )
        url = 'https://www.twitch.tv/northbaysmash/videos?filter=highlights&sort=time'
        args = [
            'youtube-dl',
            url,
            '--config-location', os.path.abspath(
                os.path.join(os.path.split(os.path.dirname(archiver.__file__))[0],
                        './settings/ytdl.conf')),
            '--yes-playlist']
        return {'args': args, 'output_path': output_path}

current = download_schedule()

if (__name__ == '__main__'):
    current.make_schedule(os.getenv('username'), 'mynameisjoe1')
