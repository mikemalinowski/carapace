import functools

from . import resources
from ...vendors import qute


# --------------------------------------------------------------------------------------------------
class Switcher(qute.QPushButton):
    panelSwitch = qute.Signal(str)

    # ----------------------------------------------------------------------------------------------
    def __init__(self, group_names, parent=None):
        super(Switcher, self).__init__('', parent=parent)

        self.toolbar = parent
        self.group_names = group_names

        pixmap = qute.QPixmap(resources.get('switch.png')).scaled(
            50,
            50,
            mode=qute.Qt.SmoothTransformation,
        )
        self.setIcon(qute.QIcon(pixmap))
        self.setSizePolicy(qute.QSizePolicy.Fixed, qute.QSizePolicy.Fixed)
        self.setFixedHeight(50)
        self.setFixedWidth(50)

    # ----------------------------------------------------------------------------------------------
    def mousePressEvent(self, event):

        if event.button() == qute.Qt.LeftButton:

            menu_data = dict()

            for group_name in self.group_names:
                menu_data[group_name] = functools.partial(
                    self.panelSwitch.emit,
                    group_name,
                )

            menu = qute.utilities.menus.menuFromDictionary(menu_data, parent=self)
            menu.popup(qute.QCursor().pos())