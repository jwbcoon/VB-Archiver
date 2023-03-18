import subprocess
import arch_schedule as schedule

# runs the youtube-dl shell commands and redirects output to dldest
def scan():
    with open(schedule.get()['output_path'], 'w') as outfile:
        subprocess.run(schedule.get()['args'], stdout=outfile)

if (__name__ == '__main__'):
    scan()
