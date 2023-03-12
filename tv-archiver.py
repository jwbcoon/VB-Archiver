import subprocess

# runs the youtube-dl shell commands and redirects output to dldest
with open('./dldest/filenames.txt', 'w') as outfile:
    subprocess.run(['youtube-dl',
                    'BaW_jenozKc', 
                    '--config-location', './config.txt'],
                   stdout=outfile)
