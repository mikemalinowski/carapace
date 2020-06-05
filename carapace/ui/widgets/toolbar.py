import json

from . import toolbutton
from . import resources
from . import switcher

from ...vendors import qute
from ...import core


# --------------------------------------------------------------------------------------------------
class Toolbar(qute.QWidget):

    # ----------------------------------------------------------------------------------------------
    def __init__(self, additional_paths=None, parent=None):
        super(Toolbar, self).__init__(parent=parent)

        with open(resources.get('struct.json'), 'r') as f:
            self.layout_data = json.load(f)

        # -- Set the main layout
        self.setLayout(
            qute.utilities.layouts.slimify(
                qute.QVBoxLayout(),
            ),
        )

        # -- Get a toolkit instance
        self.toolkit = core.toolkit(additional_paths=additional_paths)

        # -- Create the switcher
        self.switcher = switcher.Switcher(
            group_names=[
                v['panel_name']
                for v in self.layout_data
            ],
            parent=self,
        )
        self.switcher.panelSwitch.connect(self.setToolGroup)

        self.layout().addWidget(self.switcher)

        # -- Create the tool layout
        self.tool_layout = qute.utilities.layouts.slimify(
            qute.QVBoxLayout(),
        )
        self.layout().addLayout(self.tool_layout)

        self.setToolGroup('Test')

    # ----------------------------------------------------------------------------------------------
    def setToolGroup(self, group_name):

        tools_in_panel = list()

        for panel in self.layout_data:
            if group_name == panel['panel_name']:
                tools_in_panel = panel['tools']

        # -- Now clear the tool layout
        qute.utilities.layouts.empty(self.tool_layout)

        # -- Now add in a tool item
        for tool_name in tools_in_panel:

            # -- If this is an invalid tool we cannot show it
            if tool_name not in self.toolkit.identifiers():
                continue

            # -- Instance the tool, passing the tool plugin
            tool_button = toolbutton.ToolButton(
                tool=self.toolkit.request(tool_name),
                parent=self
            )

            self.tool_layout.addWidget(tool_button)

        # -- Finally add a spacer to push all the poses up
        self.tool_layout.addSpacerItem(
            qute.QSpacerItem(5, 5, qute.QSizePolicy.Expanding, qute.QSizePolicy.Expanding)
        )


# ------------------------------------------------------------------------------
# noinspection PyPep8Naming
class ToolKitWindow(qute.QMainWindow):

    # --------------------------------------------------------------------------
    def __init__(self, additional_paths=None, parent=None):
        super(ToolKitWindow, self).__init__(parent=parent)

        self.setCentralWidget(
            Toolbar(
                additional_paths=additional_paths,
                parent=self,
            ),
        )


# --------------------------------------------------------------------------------------------------
def launch(additional_paths=None):

    q_app = qute.qApp([])

    w = ToolKitWindow(
        additional_paths=additional_paths,
        parent=qute.utilities.windows.mainWindow(),
    )
    w.show()

    q_app.exec_()
