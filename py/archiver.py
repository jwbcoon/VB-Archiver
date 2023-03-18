import subprocess
import logging
import archive_schedule as schedule

logging.basicConfig(filename='logs/archiver.log',
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
