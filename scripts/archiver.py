import subprocess
import logging
import archive_schedule as schedule
from inspect import currentframe
import os

log_file = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'logs/archiver.log') )
logging.basicConfig(filename=log_file,
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

# runs the youtube-dl shell commands and redirects output to dldest/filenames.txt
def main():
    logging.info('Running ytdl ... ')
    sched_contents = schedule.contents()
    with open(sched_contents['output_path'], 'w') as outfile:
        dlproc = subprocess.run(sched_contents['args'], stdout=outfile)
        logging.error('stderr: {0}'.format(dlproc.stderr))

if (__name__ == '__main__'):
    logging.info('Starting archiver. __name__ == {0}'.format(__name__))
    try:
        main()
    except Exception as e:
        logging.error('Failed to start archiver.py; line {0}\n{1}'
                      .format(currentframe().f_lineno, e))
