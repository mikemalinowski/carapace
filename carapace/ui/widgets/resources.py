import os


# --------------------------------------------------------------------------------------------------
def get(name):
    return os.path.join(
        os.path.dirname(__file__),
        '_res',
        name,
    )