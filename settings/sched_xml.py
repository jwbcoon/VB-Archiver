import dicttoxml as dtx
from init import archive_schedule as sched

# Generate XML files for schtasks.exe to run

xml = dtx.dicttoxml(sched.profile())
