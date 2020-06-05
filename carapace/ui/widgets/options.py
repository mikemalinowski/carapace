import functools

from . import infopanel
from ...vendors import qute
from ...vendors import scribble


_SCRIBBLE_PREFIX = 'carapace_'


# --------------------------------------------------------------------------------------------------
def show_options(scribble_key, defaults=None, pos=None):
    """
    This function will show the options panel for the given scribble key.

    :param scribble_key: They key to access any user stored options
        which need to be shown.
    :type scribble_key: str

    :param defaults: Any default values which need to be shown if there are
        no saved settings for values
    :type defaults: dict

    :return: OptionsWindow instance
    """
    # -- We prefix all our option strings with 'carapace'
    if not scribble_key.startswith(_SCRIBBLE_PREFIX):
        scribble_key = _SCRIBBLE_PREFIX + scribble_key

    # -- TODO: This should be removed, its here only whilst
    # -- debugging
    # -- Ensure we have a parent - we use the maya window
    parent = qute.utilities.windows.mainWindow()

    # -- If we have an active instance, we strive to re-utilise it
    if OptionsWindow.ACTIVE_INSTANCE:
        try:
            OptionsWindow.ACTIVE_INSTANCE.setKey(scribble_key, defaults=defaults)

            if pos:
                OptionsWindow.ACTIVE_INSTANCE.setGeometry(
                    pos.x(),
                    pos.y(),
                    OptionsWindow.ACTIVE_INSTANCE.size().width(),
                    OptionsWindow.ACTIVE_INSTANCE.size().height(),
                )

            OptionsWindow.ACTIVE_INSTANCE.show()
            return OptionsWindow.ACTIVE_INSTANCE

        except:
            print('something went wrong, so making a new one')
            import sys
            print(sys.exc_info())
            pass

    # -- In this scenario we could not re-use an existing
    # -- instance, so we shall create a new one
    OptionsWindow.ACTIVE_INSTANCE = OptionsWindow(
        scribble_key,
        defaults=defaults,
        parent=parent
    )

    if pos:
        OptionsWindow.ACTIVE_INSTANCE.setGeometry(
            pos.x(),
            pos.y(),
            OptionsWindow.ACTIVE_INSTANCE.size().width(),
            OptionsWindow.ACTIVE_INSTANCE.size().height(),
        )

    OptionsWindow.ACTIVE_INSTANCE.show()

    return OptionsWindow.ACTIVE_INSTANCE


# --------------------------------------------------------------------------------------------------
class OptionsWidget(qute.QWidget):
    """
    This shows all options stored in a scribble data block.
    
    :param scribble_key: They key to access any user stored options
        which need to be shown.
    :type scribble_key: str

    :param defaults: Any default values which need to be shown if there are
        no saved settings for values
    :type defaults: dict

    """

    # ----------------------------------------------------------------------------------------------
    def __init__(self, scribble_key, defaults=None, parent=True):
        super(OptionsWidget, self).__init__(parent=parent)

        self._scribble_key = scribble_key
        self._widgets = dict()

        # -- Create our base layout
        self.setLayout(
            qute.QVBoxLayout(),
        )

        # -- Add our title and separator - so we can distinguish between
        # -- the title and the options
        self.main_label = qute.QLabel('Tool Options')
        self.layout().addWidget(self.main_label)

        self.line = qute.QFrame()
        self.line.setFrameShape(qute.QFrame.HLine)
        self.line.setFrameShadow(qute.QFrame.Sunken)
        self.layout().addWidget(self.line)

        # -- Now create the options layout
        self.options_layout = qute.QVBoxLayout()
        self.layout().addLayout(self.options_layout)

        # -- Set the key, which triggers a rebuild of the dynamic properties
        self.setKey(
            scribble_key=scribble_key,
            defaults=defaults,
        )

    # ----------------------------------------------------------------------------------------------
    def setKey(self, scribble_key, defaults=None):
        """
        This triggers a rebuild of all the options, based on the given scribble
        key.
        
        :param scribble_key: They key to access any user stored options
            which need to be shown.
        :type scribble_key: str
    
        :param defaults: Any default values which need to be shown if there are
            no saved settings for values
        :type defaults: dict

        :return: 
        """
        # -- Update the scribble key
        self._scribble_key = scribble_key

        # -- Clear out our cache
        self._widgets = dict()

        # -- Clear out the layout so we can start rebuilding it
        qute.utilities.layouts.empty(self.options_layout)

        # -- Merge the data, starting with the defaults as a base, then
        # -- overlaying with any stored preferences
        settings = defaults or dict()
        settings.update(scribble.get(self._scribble_key))

        # -- We can now start building our widgets to represent
        # -- the scribble data
        for key in sorted(settings.keys()):

            # -- If any setting starts with an underscore we assume
            # -- it is a visual hint
            if key.startswith('_'):
                continue
            
            # -- Get the current value
            value = settings[key]

            # -- Check if this key has a visual hint, if it does then we assign
            # -- a visual override. This allows for strings to be displayed as 
            # -- lists etc.
            visual_override = None
            if '_' + key in settings:
                visual_override = settings['_' + key]

            # -- Generate a widget to represent this value
            _widget = qute.utilities.derive.deriveWidget(
                visual_override or value,
                active_value=value,
            )
            
            # -- Add a label against each option so the user understands
            # -- what each setting does
            label_layout = qute.utilities.widgets.addLabel(
                _widget,
                key,
                min_width=60,
            )

            # -- Add the widget to our layout
            self.options_layout.addLayout(label_layout)

            # -- Hook up the change event
            _widget.setObjectName(key)

            # -- Store the widget in our scribble map
            self._widgets[key] = _widget

            qute.utilities.derive.connectBlind(
                _widget,
                functools.partial(
                    self._storeChange,
                    key,
                    _widget,
                )
            )

    # ----------------------------------------------------------------------------------------------
    def _storeChange(self, key, widget, *args, **kwargs):
        """
        This is used to trigger a save of settings values.

        :param key: The name of the setting to store the change for
        :type key: str

        :param widget: The widget that has been changed by the user
        :type widget: qute.QWidget

        :return:
        """
        # -- Access the stored settings
        options = scribble.get(self._scribble_key)

        # -- Update the changed key with the value from the ui
        options[key] = qute.utilities.derive.deriveValue(widget)

        # -- Save the changes
        options.save()

    # ----------------------------------------------------------------------------------------------
    def leaveEvent(self, event):
        """
        Whenever we leave this widgets area we want to hide the window

        :param event:
        :return:
        """
        # -- Map the geometry of the window to worldspace. We do this because
        # -- some widgets trigger a leaveEvent call (such as combo boxes) and we
        # -- do not want to hide the window when the user clicks one of these.
        rect = self.geometry()
        global_rect = qute.QRect(self.mapToGlobal(rect.topLeft()), rect.size())

        if not global_rect.contains(qute.QCursor().pos()):
            self.window().hide()


# --------------------------------------------------------------------------------------------------
class OptionsWindow(infopanel.PanelWindow):
    """
    Main window which shows the options information
    """
    # -- We used this to track the active instance to allow us
    # -- to re-use it where possible
    ACTIVE_INSTANCE = None

    ROUNDING = 8

    # ----------------------------------------------------------------------------------------------
    def __init__(self, scribble_key, defaults=None, parent=None):
        super(OptionsWindow, self).__init__(parent=parent)

        # -- Assign the central widget
        self.setCentralWidget(
            OptionsWidget(
                scribble_key=scribble_key,
                defaults=defaults,
                parent=self,
            ),
        )

    # ----------------------------------------------------------------------------------------------
    def setKey(self, scribble_key, defaults=None):
        self.centralWidget().setKey(scribble_key, defaults=defaults)
