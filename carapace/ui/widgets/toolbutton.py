import os

from . import options
from . import tooltip

from ...vendors import qute


# --------------------------------------------------------------------------------------------------
class ToolButton(qute.QPushButton):

    # ----------------------------------------------------------------------------------------------
    def __init__(self, tool, parent=None):
        super(ToolButton, self).__init__('', parent=parent)

        self.tool = tool
        self.toolbar = parent

        self.setIcon(
            qute.QIcon(
                qute.QPixmap(self.tool.Icon.replace('\\', '/')).scaled(
                    50,
                    50,
                    mode=qute.Qt.SmoothTransformation,
                ),
            ),
        )

        self.setSizePolicy(qute.QSizePolicy.Fixed, qute.QSizePolicy.Fixed)
        self.setFixedHeight(50)
        self.setFixedWidth(50)

        self.setToolTip(self.tool.Identifier)

    # ----------------------------------------------------------------------------------------------
    def mousePressEvent(self, event):

        if event.button() == qute.Qt.LeftButton:
            self.tool.run(
                **self.tool.options()
            )

        elif event.button() == qute.Qt.RightButton:

            # -- Show the options
            options.show_options(
                self.tool.Identifier,
                self.tool.DEFAULT_OPTIONS,
                qute.QCursor().pos(),
            )

        elif event.button() == qute.Qt.MiddleButton:

            tooltip.show_tooltip(
                title=self.tool.Identifier,
                descriptive=self.tool.Description,
                graphic=self.tool.Graphic,
                pos=qute.QCursor().pos(),
            )
