from json import dumps
from copy import deepcopy
from vba.py.lib.deepdict import deepdict

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
        self.ydl_opts = self[0]
        self.sched_opts = self[1]
        self.url = url

    def __new__(cls):
        self = super(vba_schedule, cls).__new__(cls, [deepdict(), deepdict()])
        return self
    
    def __str__(self): # use json.dumps to format string output
        return '\tvba_schedule object --\n\ttarget URL: {}\n\n{}\n\n{}'.format(
            self.url,
            dumps(self.ydl_opts, indent=4),
            dumps(self.sched_opts, indent=4) )
    
    def __deepcopy__(self, memo): # reference: https://stackoverflow.com/questions/1500718/how-to-override-the-copy-deepcopy-operations-for-a-python-object
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for key, value in self.__dict__.items():
            setattr(result, key, deepcopy(value, memo))
        return result
    
    def update_ydl(self, key, value):
        try:
            self.ydl_opts.update({key: value})
        except:
            raise

    def update_sched(self, key, value):
        try:
            self.sched_opts.update({key: value})
        except:
            raise
    '''
    Deep copy the ydl of src_vbas into self
    '''
    def copy_ydl(self, src_dict=None, src_vbas=None):
        if src_dict and isinstance(src_dict, dict):
            self.ydl_opts = deepdict(src_dict)
        elif src_vbas and isinstance(src_vbas, vba_schedule):
            self.ydl_opts = deepdict(src_vbas[0])

    '''
    Deep copy the schedule of src_vbas into self
    '''
    def copy_sched(self, src_dict=None, src_vbas=None):
        if src_dict and isinstance(src_dict, dict):
            self.sched_opts.update(deepdict(src_dict))
        elif src_vbas and isinstance(src_vbas, vba_schedule):
            self.sched_opts.update(deepdict(src_vbas.sched_opts))
