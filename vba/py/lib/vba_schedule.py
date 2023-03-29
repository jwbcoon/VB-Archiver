from json import dumps
from copy import deepcopy
from lib.deepdict import deepdict

'''
vba_schedule objects are tuple pairs of configurations as dicts:
    the download config
        and
    the schedule config

vba_schedule objects have one additionaly member variable:
    url -> target url to download from
'''
class vba_schedule(tuple):
    def __init__(self, url=None) -> None:
        self.url = url

    def __new__(cls, ydl_opts=None, sched_opts=None):
        if (ydl_opts == None):
            ydl_opts = deepdict()
        elif not isinstance(ydl_opts, dict): # reject passing non-dict to __new__
            raise Exception('vba_schedule __new__ method received arguments which were not dictionaries')
        if (sched_opts == None):
            sched_opts = deepdict()
        elif not isinstance(sched_opts, dict): # reject passing non-dict to __new__
            raise Exception('vba_schedule __new__ method received arguments which were not dictionaries')

        self = super(vba_schedule, cls).__new__(cls, [ydl_opts, sched_opts])

        return self
    
    def __str__(self): # use json.dumps to format string output
        return '\tvba_schedule object --\n\ttarget URL: {}\n\n{}\n\n{}'.format(
            self.url,
            dumps(self[0], indent=4),
            dumps(self[1], indent=4) )
    
    def ydl_profile(self) -> dict:
        return self[0]
    
    def sched_profile(self) -> dict:
        return self[1]
    
    def update_ydl(self, kvpair):
        try:
            self[0].update(kvpair)
        except:
            raise

    def update_sched(self, kvpair):
        try:
            self[1].update(kvpair)
        except:
            raise
    '''
    Deep copy the ydl of src_vbas into self
    '''
    def copy_ydl(self, src_dict=None, src_vbas=None):
        if (src_dict and isinstance(src_dict, dict)):
            self[0] = deepcopy(src_dict)
        elif(src_vbas and isinstance(src_vbas, vba_schedule)):
            self[0] = deepcopy(src_vbas[0])

    '''
    Deep copy the schedule of src_vbas into self
    '''
    def copy_sched(self, src_dict=None, src_vbas=None):
        if (src_dict and isinstance(src_dict, dict)):
            self[1].clear()
            self[1].update(deepcopy(src_dict))
        elif(src_vbas and isinstance(src_vbas, vba_schedule)):
            self[1].clear()
            self[1].update(deepcopy(src_vbas[1]))
