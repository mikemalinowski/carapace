import os

from . import infopanel
from . import resources
from ...vendors import qute


# --------------------------------------------------------------------------------------------------
def show_tooltip(title=None, descriptive=None, graphic=None, pos=None):
    """
    For the sake of optimisation we only ever instance a single tooltip if
    we can. Therefore this function handles the concept of a singleton.

    :param title: Title to show in the tooltip
    :type title: str

    :param descriptive: A descriptive breakdown for the user
    :type descriptive: str

    :param graphic: An absolute path to a gif demonstrating the behaviour
    :type graphic: str

    :return: carapace.ui.widgets.Tooltip instance
    """
    # -- TODO: This should be removed, its here only whilst
    # -- debugging
    title = title or 'Test'
    descriptive = descriptive or 'this is a demonstration of a tooltip'
    graphic = graphic or resources.get('test.gif')

    # -- Ensure we have a parent - we use the maya window
    parent = qute.utilities.windows.mainWindow()

    # -- If we have an active instance, we strive to re-utilise it
    if TooltipWindow.ACTIVE_INSTANCE:
        try:
            TooltipWindow.ACTIVE_INSTANCE.setData(
                title,
                descriptive,
                graphic,
            )

            TooltipWindow.ACTIVE_INSTANCE.setGeometry(
                pos.x(),
                pos.y(),
                TooltipWindow.ACTIVE_INSTANCE.size().width(),
                TooltipWindow.ACTIVE_INSTANCE.size().height(),
            )

            TooltipWindow.ACTIVE_INSTANCE.show()
            return TooltipWindow.ACTIVE_INSTANCE
        except:
            pass

    # -- In this scenario we could not re-use an existing
    # -- instance, so we shall create a new one
    TooltipWindow.ACTIVE_INSTANCE = TooltipWindow(
        title,
        descriptive,
        graphic,
        parent=parent
    )

    TooltipWindow.ACTIVE_INSTANCE.setGeometry(
        pos.x(),
        pos.y(),
        TooltipWindow.ACTIVE_INSTANCE.size().width(),
        TooltipWindow.ACTIVE_INSTANCE.size().height(),
    )

    TooltipWindow.ACTIVE_INSTANCE.show()
    
    return TooltipWindow.ACTIVE_INSTANCE


# --------------------------------------------------------------------------------------------------
class ToolTip(qute.QWidget):
    """
    This is the central area  of a tool tip, and the area responsible for showing the
    information to the user
    """
    
    # ----------------------------------------------------------------------------------------------
    def __init__(self, title, descriptive, graphic, parent=None):
        super(ToolTip, self).__init__(parent=parent)

        # -- We store the movie as a variable to allow us to stop it
        # -- whenever the widget is not visible
        self._movie = None

        # --- Set the default layout
        self.setLayout(
            qute.utilities.layouts.slimify(
                qute.QVBoxLayout(),
            ),
        )

        # -- Define the styling based on the css data
        qute.utilities.styling.apply(
            [
                resources.get('tooltip.css')
            ],
            apply_to=self,
        )

        # -- Load in the ui file
        self.ui = qute.utilities.designer.load(
            resources.get('tooltip.ui'),
        )
        self.layout().addWidget(self.ui)

        # -- Finally apply the data to show in the tooltip
        self.setData(
            title,
            descriptive,
            graphic,
        )

    # ----------------------------------------------------------------------------------------------
    def optimize(self):
        if self._movie:
            self._movie.stop()

    # ----------------------------------------------------------------------------------------------
    def hideEvent(self, *args, **kwargs):
        """
        Whenever this widget is hidden we explicitly stop the movie to ensure
        we're being as optimal as possible.

        :return:
        """
        self.optimize()

    # ----------------------------------------------------------------------------------------------
    def leaveEvent(self, event):
        """
        Whenever we leave this widgets area we want to hide the window

        :param event:
        :return:
        """
        self.window().hide()

    # ----------------------------------------------------------------------------------------------
    def setData(self, title, descriptive, graphic):
        """
        Allows the setting of data within the tooltip

        :param title: Title to show in the tooltip
        :type title: str

        :param descriptive: A descriptive breakdown for the user
        :type descriptive: str

        :param graphic: An absolute path to a gif demonstrating the behaviour
        :type graphic: str

        :return:
        """
        # -- Apply the data textural data
        self.ui.title.setText(title)
        self.ui.descriptive.setText(descriptive)

        # -- Now we assign the movie and play it
        self._movie = qute.QMovie(graphic)
        self._movie.setScaledSize(qute.QSize(400, 400))
        self.ui.graphic.setMovie(self._movie)
        self._movie.start()


# --------------------------------------------------------------------------------------------------
class TooltipWindow(infopanel.PanelWindow):
    """
    This is the main window panel which holds the tooltip widget. This window
    is responsible for the transparency and rounding.
    """
    # -- We used this to track the active instance to allow us
    # -- to re-use it where possible
    ACTIVE_INSTANCE = None

    ROUNDING = 8

    # ----------------------------------------------------------------------------------------------
    def __init__(self, title, descriptive, graphic, parent=None):
        super(TooltipWindow, self).__init__(parent=parent)

        # -- Assign the central widget
        self.setCentralWidget(
            ToolTip(
                title,
                descriptive,
                graphic,
                parent=self,
            ),
        )

    # ----------------------------------------------------------------------------------------------
    def setData(self, title, descriptive, graphic):
        """
        Allows the setting of data within the tooltip

        :param title: Title to show in the tooltip
        :type title: str

        :param descriptive: A descriptive breakdown for the user
        :type descriptive: str

        :param graphic: An absolute path to a gif demonstrating the behaviour
        :type graphic: str
        :return:
        """
        self.centralWidget().setData(title, descriptive, graphic)
