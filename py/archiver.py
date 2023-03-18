import subprocess
import logging
import archive_schedule as schedule
import os

log_file = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'logs/archiver.log') )
logging.basicConfig(filename=log_file,
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

# runs the youtube-dl shell commands and redirects output to dldest/filenames.txt
def main():
    logging.info('Running ytdl ... ')
    with open(schedule.get()['output_path'], 'w') as outfile:
        dlproc = subprocess.run(schedule.get()['args'], stdout=outfile)
        logging.info('stdout: {0}'.format(dlproc.stdout))
        logging.error('stderr: {0}'.format(dlproc.stderr))

if (__name__ == '__main__'):
    main()
