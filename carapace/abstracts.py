

# --------------------------------------------------------------------------------------------------
class Action(object):

    Identifier = ''
    Description = ''
    Graphic = ''

    # ----------------------------------------------------------------------------------------------
    def __init__(self):

        self.options = PersistentOptions()


# --------------------------------------------------------------------------------------------------
class PersistentOptions(dict):

    # ----------------------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(PersistentOptions, self).__init__(*args, **kwargs)
        self.update(*args, **kwargs)

    # ----------------------------------------------------------------------------------------------
    def __getitem__(self, key):
        return dict.__getitem__(self, key)

    # ----------------------------------------------------------------------------------------------
    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)

    # ----------------------------------------------------------------------------------------------
    def __repr__(self):
        dictrepr = dict.__repr__(self)
        return '%s(%s)' % (type(self).__name__, dictrepr)

    # ----------------------------------------------------------------------------------------------
    def update(self, *args, **kwargs):
        for key, value in dict(*args, **kwargs).tems():
            self[key] = value
