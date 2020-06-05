from ...vendors import qute


# --------------------------------------------------------------------------------------------------
class PanelWindow(qute.QMainWindow):

    # -- Define class variables so we do not have to reinitialise them
    # -- as these are considered constants.
    BACKGROUND_COLOR = qute.QColor(46, 46, 46, a=200)
    PEN = qute.QPen(qute.Qt.black, 1)
    ROUNDING = 25

    # ----------------------------------------------------------------------------------------------
    def __init__(self, parent=None):
        super(PanelWindow, self).__init__(parent=parent)

        # -- Set the window to not have a title bar and have the background
        # -- be transparent
        self.setWindowFlags(qute.Qt.Window | qute.Qt.FramelessWindowHint)
        self.setAttribute(qute.Qt.WA_TranslucentBackground)

    # ----------------------------------------------------------------------------------------------
    def paintEvent(self, event):
        """
        We override the paint event to allow us to draw with nice rounded edges

        :param event:
        :return:
        """
        qp = qute.QPainter()
        qp.begin(self)
        qp.setRenderHint(
            qute.QPainter.Antialiasing,
            True,
        )

        qsize = self.size()

        gradient = qute.QLinearGradient(0, 0, 0, qsize.height())
        gradient.setColorAt(0, qute.QColor(150, 150, 150, a=150))
        gradient.setColorAt(1, qute.QColor(50, 50, 50, a=150))

        qp.setPen(self.PEN)
        qp.setBrush(gradient) # self.BACKGROUND_COLOR)

        qp.drawRoundedRect(
            0,
            0,
            qsize.width(),
            qsize.height(),
            self.ROUNDING,
            self.ROUNDING,
        )
        qp.end()
