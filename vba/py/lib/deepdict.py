
class deepdict(dict):
    '''
    Generate a dictionary.items() deepcopy with keys and values modified via parameter methods.
    If no parameter methods are passed, return an unmodified dictionary.items() deepcopy.

        - dictionary: dictionary to deepcopy from

        - modify_key: method to modify keys with

        - modify_value: method to modify values with
    '''
    def modified_items(self, modify_key=lambda a: a, modify_value=lambda a: a):
        for key, value in self.items():
            modkey = modify_key(key)
            if type(value) is dict or isinstance(value, deepdict):
                modval = deepdict(value)
                nestval = ({k: v for k, v in modval.modified_items(modify_key, modify_value)})
                yield (modkey, nestval)
            elif (type(value) is list or type(value) is tuple) and type(value) is not str:
                for ele in value:
                    if type(ele) is dict or isinstance(value, deepdict):
                        modval = deepdict(ele)
                        elenestval = ({k: v for k, v in modval.modified_items(modify_key, modify_value)})
                        yield (modkey, elenestval)
            else:
                modval = modify_value(value)
                yield (modkey, modval)

    '''
    Generate a dictionary deepcopy with keys and values modified via parameter methods.
    If no parameter methods are passed, return an unmodified deepcopy of the dictionary parameter.

        - dictionary: dictionary to deepcopy from

        - modify_key: method to modify keys with

        - modify_value: method to modify values with
    '''
    def modified_dict(self, modify_key=lambda a: a, modify_value=lambda a: a):
        return deepdict({key: value for key, value in self.modified_items(modify_key, modify_value)})
