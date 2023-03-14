import subprocess
import ytdl_scan as vid
import os

# Make a video archive schedule
def make_schedule(username, password, frequency, day):
    dir_path = os.path.dirname(os.path.abspath(vid.__file__))
    task_name = 'vb_archiver'
    task_command = ['schtasks.exe',
                    '/Create',
                    '/U', username,
                    '/P', password,
                    '/SC', frequency,
                    '/D', day,
                    '/TN', task_name,
                    '/TR', dir_path]
    subprocess.run(task_command)

# Export data to be used in another file

def get():
    output_path = './dldest/filenames.txt'
    url = 'https://www.twitch.tv/northbaysmash/videos?filter=highlights&sort=time'
    args = [
        'youtube-dl',
        url,
        '--config-location', os.path.abspath('config.txt'),
        '--yes-playlist']
    return {'args': args, 'output_path': output_path}
        