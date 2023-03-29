import subprocess
from vba.py.archive_schedule import contents, current, deepcopy
from vba.py.lib.vba_schedule import vba_schedule as vbas
import os

# runs the youtube-dl shell commands and redirects output to dldest/filenames.txt
def main(vb: vbas):
    sched_contents = contents(vb)
    #print(vb)
    #print(sched_contents)
    subprocess.run(sched_contents['args'])
    #with open(sched_contents['output_path'], 'w') as outfile:
    #    subprocess.run(sched_contents['args'], stdout=outfile)

if (__name__ == '__main__'):
    vb = deepcopy(current)
    vb.update_ydl('config-location',
                    os.path.abspath(os.path.join(
                    os.path.split(os.path.dirname(__file__))[0], '../settings/ytdl.conf')) )
    main(vb)
