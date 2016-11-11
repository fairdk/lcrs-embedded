"""
Instances inherited from JSONModel *must* live in lcrs_embedded.models since
that automatically adds them to the registry and will instantiate them as the
expected type upon deserialization.
"""


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
        dict.__setitem__(self, "__type__", self.__class__.__name__)
        dict.__setattr__(self, "__type__", self.__class__.__name__)

    def __setitem__(self, key, value):
        if not hasattr(self, key):
            raise KeyError("Not a defined model attribute of {}".format(
                type(self))
            )
        setattr(self, key, value)
        super(JSONModel, self).__setitem__(key, value)

    def __delitem__(self, key):
        delattr(self, key)
        super(JSONModel, self).__delitem__(key)

    def __setattr__(self, key, value):
        dict.__setattr__(self, key, value)
        super(JSONModel, self).__setitem__(key, value)


def decoder(dct):
    from .. import models
    Klass = dct.pop('__type__', "")
    if Klass:
        return getattr(models, Klass, dict)(**dct)
    else:
        return dict(**dct)
