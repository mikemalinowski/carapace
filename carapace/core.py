import os
from .vendors import scribble
from .vendors import factories
from . import constants


# --------------------------------------------------------------------------------------------------
def _get_resource(name):
    return os.path.join(
        os.path.dirname(__file__),
        '_res',
        name,
    )


# --------------------------------------------------------------------------------------------------
def toolkit(additional_paths=None):
    """
    Returns a factory containing all the carapace tools available for use.

    :param additional_paths: Any additional locations you want to specify. Each location
        will be added to the factories search locations.
    :type additional_paths: list

    :return: factories.Factory instance
    """
    # -- Allow the user to give additional paths to find carapace tools
    paths = additional_paths or list()
    paths.append(
        os.path.join(
            os.path.dirname(__file__),
            'tools',
        ),
    )

    return factories.Factory(
        abstract=Tool,
        plugin_identifier='Identifier',
        envvar=constants.CARAPACE_TOOL_PATHS_ENVVAR,
        paths=paths,
    )


# --------------------------------------------------------------------------------------------------
class Tool(object):

    Identifier = ''
    Description = ''
    Graphic = ''
    Icon = _get_resource('tool.png')

    DEFAULT_OPTIONS = dict()

    # ----------------------------------------------------------------------------------------------
    @classmethod
    def run(cls, *args, **kwargs):
        pass

    @classmethod
    def options(cls):

        settings = dict()

        for k, v in cls.DEFAULT_OPTIONS.items():
            settings[k] = v

        for k, v in scribble.get('carapace_' + cls.Identifier).items():
            settings[k] = v

        return settings
