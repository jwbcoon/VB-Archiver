import subprocess
import archiver
import os

# Make a video archive schedule
def make_schedule(frequency, modifier, day):
    interp_path = '\''.join(['', os.path.abspath(os.environ['_']),''])
    dir_path = os.path.abspath(archiver.__file__)
    task_with_args = ' '.join([interp_path, dir_path])
    task_with_args = '\"'.join(['', task_with_args, '']) # maybe unnecessary?
    task_name = 'vb_archiver'
    task_command = ['schtasks.exe',
                    '/Create',
                    '/RU', 'SYSTEM',
                    '/SC', frequency,
                    '/MO', modifier,
                    #'/D', day,
                    '/TN', task_name,
                    '/TR', task_with_args]
    subprocess.run(task_command)

# Export data to be used in another file

def get():
    output_path = './dldest/filenames.txt'
    url = 'https://www.twitch.tv/northbaysmash/videos?filter=highlights&sort=time'
    args = [
        'youtube-dl',
        url,
        '--config-location', os.path.abspath('./py/config.txt'),
        '--yes-playlist']
    return {'args': args, 'output_path': output_path}


if (__name__ == '__main__'):
    make_schedule('MINUTE', '5', '*')
