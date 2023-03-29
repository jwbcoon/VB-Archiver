import subprocess
import archive_schedule as schedule
from py.lib.vba_schedule import vba_schedule as vbas

# runs the youtube-dl shell commands and redirects output to dldest/filenames.txt
def main(vb: vbas):
    sched_contents = schedule.contents(vb)
    with open(sched_contents['output_path'], 'w') as outfile:
        subprocess.run(sched_contents['args'], stdout=outfile)

if (__name__ == '__main__'):
    main()
