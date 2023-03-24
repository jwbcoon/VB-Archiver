import dicttoxml as dtx
from init import archive_schedule as sched

# Template for generating xml files
xml_schema = {
    
}

# Generate XML files for schtasks.exe to run
xml = dtx.dicttoxml(sched.profile())
