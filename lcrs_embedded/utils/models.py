class JSONModel(dict):
    """
    Used to map classes to models. It's nice because we can then use
    Django-like models to model the whole protocol.
    """
    pass

    def __init__(self, **kwargs):
        super(JSONModel, self).__init__(**kwargs)
        # Use constructor for defining initial data
        for k, v in kwargs.items():
            self[k] = v
        parent_dict = dir(dict)
        for x in self.__dir__():
            if not x.startswith("__") and x not in parent_dict:
                self[x] = getattr(self, x)

    def __setitem__(self, key, value):
        if not hasattr(self, key):
            raise KeyError("Not a defined model attribute")
        setattr(self, key, value)
        super(JSONModel, self).__setitem__(key, value)

    def __delitem__(self, key):
        delattr(self, key)
        super(JSONModel, self).__delitem__(key)

    def __getitem__(self, key):
        if not hasattr(self, key):
            raise KeyError("Not a defined model attribute")
        if hasattr(self, key):
            return getattr(self, key)
        return super(JSONModel, self).__getitem__(key)


def decoder(Klass):
    return lambda dct: Klass(**dct)
