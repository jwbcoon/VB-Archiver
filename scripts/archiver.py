import subprocess
import archive_schedule as schedule
#from inspect import currentframe
#import os

# runs the youtube-dl shell commands and redirects output to dldest/filenames.txt
def main():
    sched_contents = schedule.current.contents()
    with open(sched_contents['output_path'], 'w') as outfile:
        subprocess.run(sched_contents['args'], stdout=outfile)

if (__name__ == '__main__'):
    main()
