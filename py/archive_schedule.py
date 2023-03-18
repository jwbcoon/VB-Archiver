import subprocess
import logging
import archiver
import os

logging.basicConfig(filename='logs/archive_schedule.log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

# Make a video archive schedule
def make_schedule(frequency, modifier, day):
    interp_path = os.path.abspath(os.environ['_'])
    dir_path = os.path.abspath(archiver.__file__)
    task_with_args = ' '.join([interp_path, dir_path])
    task_name = 'vb_archiver'
    task_command = ['schtasks.exe',
                    '/Create',
                    '/RU', 'SYSTEM',
                    '/SC', frequency,
                    '/MO', modifier,
                    #'/D', day,
                    '/TN', task_name,
                    '/TR', task_with_args,
                    '/RL', 'HIGHEST']
    
    logging.info('Creating vb_archiver task ... ')
    logging.info('\n'.join(['', ' '.join(task_command)]))
    taskproc = subprocess.run(task_command)
    logging.info('stdout: {0}'.format(taskproc.stdout))
    logging.error('stderr: {0}'.format(taskproc.stderr))

# Export data to be used in another file

def get():
    output_path = os.path.abspath('../dldest/filenames.txt')
    url = 'https://www.twitch.tv/northbaysmash/videos?filter=highlights&sort=time'
    args = [
        'youtube-dl',
        url,
        '--config-location', os.path.abspath('./config.txt'),
        '--yes-playlist']
    logging.info('Sending dldest path: %(output_path)s')
    return {'args': args, 'output_path': output_path}


if (__name__ == '__main__'):
    make_schedule('MINUTE', '1', '*')
