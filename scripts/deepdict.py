from copy import deepcopy

class deepdict(dict):
    '''
    Generate a dictionary deepcopy with keys and values modified via parameter methods.
    If no parameter methods are passed, return an unmodified deepcopy of the dictionary parameter.

        - dictionary: dictionary to deepcopy from

        - modify_key: method to modify keys with

        - modify_value: method to modify values with
    '''
    def modified_items(self, modify_key=lambda a: a, modify_value=lambda a: a):
        for key, value in self.items():
            modkey = modify_key(key)
            if type(value) is dict or isinstance(value, deepdict):
                modval = deepdict(deepcopy(value))
                nestval = ({k: v for k, v in modval.modified_items(modify_key, modify_value)})
                yield (modkey, nestval)
            elif (type(value) is list or type(value) is tuple) and type(value) is not str:
                for ele in value:
                    if type(ele) is dict or isinstance(value, deepdict):
                        modval = deepdict(deepcopy(ele))
                        elnestval = ({k: v for k, v in modval.modified_items(modify_key, modify_value)})
                        yield (modkey, elnestval)
            else:
                modval = modify_value(value)
                yield (modkey, modval)
