import subprocess
import logging
import archiver
import os

log_file = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'logs/archive_schedule.log') )
logging.basicConfig(filename=log_file,
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
    logging.info((' '.join(task_command)))
    taskproc = subprocess.run(task_command)
    logging.info('stdout: {0}'.format(taskproc.stdout))
    logging.error('stderr: {0}'.format(taskproc.stderr))

# Export data to be used in another file

def get():
    output_path = os.path.abspath(
        os.path.join(os.path.dirname(archiver.__file__), '../dldest/filenames.txt') )
    url = 'https://www.twitch.tv/northbaysmash/videos?filter=highlights&sort=time'
    args = [
        'youtube-dl',
        url,
        '--config-location', os.path.abspath('./config.txt'),
        '--yes-playlist']
    logging.info('Sending dldest path: {0}'.format(output_path))
    return {'args': args, 'output_path': output_path}


if (__name__ == '__main__'):
    make_schedule('MINUTE', '1', '*')
