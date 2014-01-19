
from fife.extensions import pychan
from fife.extensions.pychan.pychanbasicapplication import PychanApplicationBase
from fife.extensions.pychan.fife_pychansettings import FifePychanSettings
from fife.extensions.pychan import widgets
from fife.extensions.pychan.widgets.buttons import Button
from fife.extensions.pychan.internal import get_manager


class Dialog():
    _gameStatusWindow = None

    def __init__(self, game):
        self.instancemenu = None
        self.dynamic_widgets = {}
        self.game = game
        self.agentManager = game.agentManager

    def getGameStatusWindow(self):
        if self._gameStatusWindow == None:
            self._gameStatusWindow = pychan.loadXML('gui/xml/game.xml')
        return self._gameStatusWindow

    def build_instancemenu(self):
        self.hide_instancemenu()
        dynamicbuttons = ('moveButton', 'talkButton', 'kickButton', 'inspectButton', 'openButton', 'attackButton', 'spellButton', 'activateButton')
        self.instancemenu = pychan.loadXML('gui/xml/instancemenu.xml')
        self.instancemenu.mapEvents({
            'moveButton' : self.game.onMoveButtonPress,
            'talkButton' : self.game.onTalkButtonPress,
            'kickButton' : self.game.onKickButtonPress,
            'inspectButton' : self.game.onInspectButtonPress,
            'openButton' : self.game.onOpenButtonPress,
            'attackButton' : self.game.onAttackButtonPress,
            'spellButton' : self.game.onSpellButtonPress,
            'activateButton' : self.game.onActivateButtonPress,
        })
        for btn in dynamicbuttons:
            self.dynamic_widgets[btn] = self.instancemenu.findChild(name=btn)
        self.instancemenu.removeAllChildren()

    def show_instancemenu(self, clickpoint, instance, buttons):
        # Create the popup.
        self.build_instancemenu()
        self.instancemenu.clickpoint = clickpoint
        self.instancemenu.instance = instance

        # Add the buttons according to circumstances.
        for el in buttons:
            self.instancemenu.addChild(self.dynamic_widgets[el])
        # And show it :)
        self.instancemenu.position = (clickpoint.x, clickpoint.y)
        self.instancemenu.show()

    def hide_instancemenu(self):
        if self.instancemenu:
            self.instancemenu.hide()

    def show(self, buttonText, text, callback, cancelText=None, callbackCancel=None):
        self.getGameStatusWindow().findChild(name='playButton').text = buttonText
        self.getGameStatusWindow().distributeData({ 'gameStatus' : open(text).read() })
        if cancelText == None or callbackCancel == None:
            self.getGameStatusWindow().mapEvents({ 'playButton' : callback })
        else:
            cancel = Button(name="cancelButton", text=cancelText)
            self.getGameStatusWindow().addChild(cancel)
            self.getGameStatusWindow().mapEvents({ 'playButton' : callback, 'cancelButton' : callbackCancel })
        self.getGameStatusWindow().show()

    def hide(self):
        self.getGameStatusWindow().hide()
