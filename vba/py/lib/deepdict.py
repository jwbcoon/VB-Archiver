
class deepdict(dict):
    '''
    Generate a dictionary.items() deepcopy with keys and values modified via parameter methods.
    If no parameter methods are passed, return an unmodified dictionary.items() deepcopy.

        - self: dictionary to deepcopy from

        - modify_key: method to modify keys with

        - modify_value: method to modify values with
    '''
    def modified_items(self, modify_key=lambda a: a, modify_value=lambda a: a):
        for key, value in self.items():
            modkey = modify_key(key)
            if isinstance(value, dict):
                modval = deepdict(value)
                nestval = ({k: v for k, v in modval.modified_items(modify_key, modify_value)})
                yield (modkey, nestval)
            elif (type(value) is list or type(value) is tuple) and type(value) is not str:
                modlist = [listitem for listitem in (({k: v for k, v in deepdict(ele).modified_items(modify_key, modify_value)})
                           for ele in value if type(ele) is dict or isinstance(ele, deepdict))]
                if type(value) is list:
                    yield (modkey, modlist)
                if type(value) is tuple:
                    yield (modkey, tuple(modlist))
            else:
                modval = modify_value(value)
                yield (modkey, modval)

    '''
    Generate a dictionary deepcopy with keys and values modified via parameter methods.
    If no parameter methods are passed, return an unmodified deepcopy of the dictionary parameter.

        - self: dictionary to deepcopy from

        - modify_key: method to modify keys with

        - modify_value: method to modify values with
    '''
    def modified_copy(self, modify_key=lambda a: a, modify_value=lambda a: a):
        return deepdict({key: value for key, value in self.modified_items(modify_key, modify_value)})

    '''
    Generate a dictionary.items() deepcopy with keys and values modified via parameter methods.
    If no parameter methods are passed, return an unmodified dictionary.items() deepcopy.
    Keys and Values may be modified conditionally based upon boolean methods key_condtional and
    value_conditional. By default, key_conditional and value_conditional return true, the number
    of arguments passed to methods key_true, key_false, value_true, and value_false are assumed
    to be one argument. Each of these methods returns their first parameter, by default.

        - self: dictionary to deepcopy from

        - presence_conditional: method to evaluate key and value operands with, returning a boolean.
                                if true is returned, the key:value pair being evaluated will be a member
                                of the generated items() set.
                                if false is returned, the key:value pair being evaluated will not be
                                a member of the generated items() set.

        - key_conditional: method to evaluate key and value operands with, returning a boolean.
                           if true is returned, method key_true will be applied to modify
                           dictionary keys from self.
                           if false is returned, method key_false will be applied to modify
                           dictionary keys from self.

        - value_conditional: method to evaluate key and value operands with, returning a boolean.
                             if true is returned, method value_true will be applied to modify
                             dictionary values from self.
                             if false is returned, method value_false will be applied to modify
                             dictionary values from self.
        
        - key_true: method to modify keys with when key_conditional evaluates to true.

        - value_true: method to modify values with when value_conditional evaluates to true.

        - key_false: method to modify keys with when key_conditional evaluates to false.

        - value_false: method to modify keys with when value_conditional evaluates to false.

        - two_key_args: if true, pass two args to key_true and key_false methods.
                        if false, pass one arg to key_true and key_false methods.
        
        - two_value_args: if true, pass two args to value_true and value_false methods.
                          if false, pass one arg to value_true and value_false methods.
    '''
    def conditional_items(self, presence_conditional=lambda k, v: True,
                          key_conditional=lambda k, v: True, value_conditional=lambda k, v: True,
                          key_true=lambda k=None, v=None: k, key_false=lambda k=None, v=None: k,
                          value_true=lambda k=None, v=None: v, value_false=lambda k=None, v=None: v,
                          two_key_args=False, two_value_args=False):
        for key, value in self.items():
            modify_key = key_true if key_conditional(key, value) else key_false
            modify_value = value_true if value_conditional(key, value) else value_false

            modkey = modify_key(k=key, v=value) if two_key_args else modify_key(k=key)
            if type(value) is dict or isinstance(value, deepdict):
                modval = deepdict(value)
                nestval = (
                { k: v
                    for k, v in modval.conditional_items(presence_conditional,
                                                         key_conditional,
                                                         value_conditional,
                                                         key_true,
                                                         key_false,
                                                         value_true,
                                                         value_false,
                                                         two_key_args,
                                                         two_value_args)
                    if presence_conditional(k, v)
                } )
                yield (modkey, nestval)
            elif (type(value) is list or type(value) is tuple) and type(value) is not str:
                modlist = [listitem for listitem in ((
                          { k: v
                          for k, v in deepdict(ele).conditional_items(presence_conditional,
                                                                      key_conditional,
                                                                      value_conditional,
                                                                      key_true,
                                                                      key_false,
                                                                      value_true,
                                                                      value_false,
                                                                      two_key_args,
                                                                      two_value_args)
                          if presence_conditional(k, v)
                          } ) for ele in value if type(ele) is dict or isinstance(value, deepdict))]
                if type(value) is list:
                    yield (modkey, modlist)
                if type(value) is tuple:
                    yield (modkey, tuple(modlist))
            else:
                modval = modify_value(k=key, v=value) if two_value_args else modify_value(v=value)
                if presence_conditional(key, value):
                    yield (modkey, modval)

    '''
    Generate a dictionary.items() deepcopy with keys and values modified via parameter methods.
    If no parameter methods are passed, return an unmodified dictionary.items() deepcopy.
    Keys and Values may be modified conditionally based upon boolean methods key_condtional and
    value_conditional. By default, key_conditional and value_conditional return true, the number
    of arguments passed to methods key_true, key_false, value_true, and value_false are assumed
    to be one argument. Each of these methods returns their first parameter, by default.

        - self: dictionary to deepcopy from

        - key_conditional: method to evaluate key and value operands with, returning a boolean.
                           if true is returned, method key_true will be applied to modify
                           dictionary keys from self.
                           if false is returned, method key_false will be applied to modify
                           dictionary keys from self.

        - value_conditional: method to evaluate key and value operands with, returning a boolean.
                             if true is returned, method value_true will be applied to modify
                             dictionary values from self.
                             if false is returned, method value_false will be applied to modify
                             dictionary values from self.
        
        - key_true: method to modify keys with when key_conditional evaluates to true.

        - value_true: method to modify values with when value_conditional evaluates to true.

        - key_false: method to modify keys with when key_conditional evaluates to false.

        - value_false: method to modify keys with when value_conditional evaluates to false.

        - two_key_args: if true, pass two args to key_true and key_false methods.
                        if false, pass one arg to key_true and key_false methods.
        
        - two_value_args: if true, pass two args to value_true and value_false methods.
                          if false, pass one arg to value_true and value_false methods.
    '''
    def conditional_copy(self, presence_conditional=lambda k, v: True,
                         key_conditional=lambda k, v: True, value_conditional=lambda k, v: True,
                         key_true=lambda k=None, v=None: k, key_false=lambda k=None, v=None: k,
                         value_true=lambda k=None, v=None: v, value_false=lambda k=None, v=None: v,
                         two_key_args=False, two_value_args=False):
        return deepdict(
            {key: value for key, value in self.conditional_items(presence_conditional,
                                                                 key_conditional,
                                                                 value_conditional,
                                                                 key_true,
                                                                 key_false,
                                                                 value_true,
                                                                 value_false,
                                                                 two_key_args,
                                                                 two_value_args)})
    
    def __flat_keys_helper(self):
        for key, value in self.items():
            if type(value) is dict or isinstance(value, deepdict):
                modval = deepdict(value)
                yield from ({k for k in modval.__flat_keys_helper()})
            elif (type(value) is list or type(value) is tuple) and type(value) is not str:
                for ele in value:
                    if type(ele) is dict or isinstance(value, deepdict):
                        modval = deepdict(ele)
                        yield from ({k for k in modval.__flat_keys_helper()})
            yield key
    
    def flat_keys(self):
        return [key for key in self.__flat_keys_helper()]
    
    
    def __flat_values_helper(self):
        for key, value in self.items():
            if type(value) is dict or isinstance(value, deepdict):
                modval = deepdict(value)
                yield from ({v for v in modval.__flat_values_helper()})
            elif (type(value) is list or type(value) is tuple) and type(value) is not str:
                for ele in value:
                    if type(ele) is dict or isinstance(value, deepdict):
                        modval = deepdict(ele)
                        yield from ({v for v in modval.__flat_values_helper()})
            yield value
    
    def flat_values(self):
        return [value for value in self.__flat_values_helper()]
