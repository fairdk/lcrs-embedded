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

    def __init__(self, **kwargs):
        super(JSONModel, self).__init__(**kwargs)
        # Use constructor for defining initial data
        for k, v in kwargs.items():
            self[k] = v
        parent_dict = dir(dict)
        for x in self.__dir__():
            if not x.startswith("__") and x not in parent_dict:
                # Make sure that fresh instances are created of mutable objects
                static_attr = getattr(self, x)
                if hasattr(static_attr, 'copy'):
                    new_instance = static_attr.copy()
                    if not type(new_instance) == type(static_attr):
                        print("Not equal: {}, {}".format(
                            type(new_instance), type(static_attr))
                        )
                else:
                    new_instance = static_attr
                new_instance = static_attr
                setattr(self, x, new_instance)
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
        raise NotImplementedError()

    def __setattr__(self, key, value):
        if not hasattr(self, key):
            raise KeyError("Not a defined model attribute of {}".format(
                type(self))
            )
        dict.__setattr__(self, key, value)
        super(JSONModel, self).__setitem__(key, value)

    # def copy(self, *args, **kwargs):
    #     JSONModel(**dict.copy(self, *args, **kwargs))


def decoder(dct):
    from .. import models
    if not isinstance(dct, dict):
        return dct
    Klass = dct.pop('__type__', "")
    if Klass:
        for k, v in dct.items():
            dct[k] = decoder(v)
            print("It was: {}".format(type(dct[k])))
        return getattr(models, Klass, dict)(**dct)
    else:
        return dict(**dct)
