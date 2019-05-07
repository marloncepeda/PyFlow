from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QWidget
from Qt.QtWidgets import QGridLayout
from Qt.QtWidgets import QHBoxLayout
from Qt.QtWidgets import QSpacerItem
from Qt.QtWidgets import QSizePolicy
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QMenu


from PyFlow.Core.Common import *


UI_INPUT_WIDGET_PINS_FACTORIES = {}


class IInputWidget(object):
    def __init__(self):
        super(IInputWidget, self).__init__()

    def getWidget(self):
        raise NotImplementedError(
            "getWidget of IInputWidget is not implemented")

    def setWidget(self, widget):
        raise NotImplementedError(
            "setWidget of IInputWidget is not implemented")

    def blockWidgetSignals(self, bLock=False):
        raise NotImplementedError(
            "blockWidgetSignals of IInputWidget is not implemented")


class InputWidgetRaw(QWidget, IInputWidget):
    """
    This type of widget can be used as a base class for complex ui generated by designer
    """

    def __init__(self, parent=None, dataSetCallback=None, defaultValue=None, **kwds):
        super(InputWidgetRaw, self).__init__(parent=parent, **kwds)
        self._defaultValue = defaultValue
        # fuction with signature void(object)
        # this will set data to pin
        self.dataSetCallback = dataSetCallback
        self._widget = None
        self._menu = QMenu()
        self.actionReset = self._menu.addAction("ResetValue")
        self.actionReset.triggered.connect(self.onResetValue)

    def setWidgetValueNoSignals(self, value):
        self.blockWidgetSignals(True)
        self.setWidgetValue(value)
        self.blockWidgetSignals(False)

    def setWidget(self, widget):
        self._widget = widget

    def getWidget(self):
        assert(self._widget is not None)
        return self._widget

    def onResetValue(self):
        self.setWidgetValue(self._defaultValue)

    def setWidgetValue(self, value):
        '''to widget'''
        pass

    def widgetValueUpdated(self, value):
        '''from widget'''
        pass

    def contextMenuEvent(self, event):
        self._menu.exec_(event.globalPos())


class InputWidgetSingle(InputWidgetRaw):
    """
    This type of widget is used for a simple widgets like buttons, checkboxes etc.
    It consists of horizontal layout widget itself and reset button.
    """

    def __init__(self, parent=None, dataSetCallback=None, defaultValue=None, **kwds):
        super(InputWidgetSingle, self).__init__(parent=parent, dataSetCallback=dataSetCallback,
                                                defaultValue=defaultValue, **kwds)
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self._index = 0
        self._widget = None
        self.senderPin = None

    def getWidget(self):
        return InputWidgetRaw.getWidget(self)

    def setWidget(self, widget):
        InputWidgetRaw.setWidget(self, widget)
        self.horizontalLayout.insertWidget(self._index, self.getWidget())


def REGISTER_UI_INPUT_WIDGET_PIN_FACTORY(packageName, factory):
    if packageName not in UI_INPUT_WIDGET_PINS_FACTORIES:
        UI_INPUT_WIDGET_PINS_FACTORIES[packageName] = factory
        print("registering", packageName, "input widgets")


def createInputWidget(dataType, dataSetter, defaultValue=None):
    pinInputWidget = None
    for packageName, factory in UI_INPUT_WIDGET_PINS_FACTORIES.items():
        pinInputWidget = factory(dataType, dataSetter, defaultValue)
        if pinInputWidget is not None:
            return pinInputWidget
    return pinInputWidget
