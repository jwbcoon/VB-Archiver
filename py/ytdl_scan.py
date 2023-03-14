import subprocess
import interface as itface
import os

# front facing GUI presents progress on download


# runs the youtube-dl shell commands and redirects output to dldest
def scan():
    with open(itface.get()['output_path'], 'w') as outfile:
        subprocess.run(itface.get()['args'], stdout=outfile)

if (__name__ == '__main__'):
    scan()
