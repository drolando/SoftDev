
from fife.extensions import pychan
from fife.extensions.pychan.pychanbasicapplication import PychanApplicationBase
from fife.extensions.pychan.fife_pychansettings import FifePychanSettings
from fife.extensions.pychan import widgets
from fife.extensions.pychan.internal import get_manager


class Dialog():
    def __init__(self, game):
        self.instancemenu = None
        self.dynamic_widgets = {}
        self.instance_to_agent = {}
        self.gameStatusWindow = pychan.loadXML('gui/xml/game.xml')
        self.game = game
        self.agentManager = game.agentManager

    def build_instancemenu(self):
        """
        Just loads the menu from an XML file
        and hooks the events up.
        The buttons are removed and later re-added if appropiate.
        """
        self.hide_instancemenu()
        dynamicbuttons = ('moveButton', 'talkButton', 'kickButton', 'inspectButton')
        self.instancemenu = pychan.loadXML('gui/xml/instancemenu.xml')
        self.instancemenu.mapEvents({
            'moveButton' : self.game.onMoveButtonPress,
            'talkButton' : self.game.onTalkButtonPress,
            'kickButton' : self.game.onKickButtonPress,
            'inspectButton' : self.game.onInspectButtonPress,
        })
        for btn in dynamicbuttons:
            self.dynamic_widgets[btn] = self.instancemenu.findChild(name=btn)
        self.instancemenu.removeAllChildren()

    def show_instancemenu(self, clickpoint, instance):
        """
        Build and show a popupmenu for an instance that the player
        clicked on. The available actions are dynamically added to
        the menu (and mapped to the onXYZ functions).
        """
        if instance.getFifeId() == self.agentManager.getHero().agent.getFifeId():
            return

        # Create the popup.
        self.build_instancemenu()
        self.instancemenu.clickpoint = clickpoint
        self.instancemenu.instance = instance

        # Add the buttons according to circumstances.
        self.instancemenu.addChild(self.dynamic_widgets['inspectButton'])
        target_distance = self.agentManager.getHero().agent.getLocationRef().getLayerDistanceTo(instance.getLocationRef())
        if target_distance > 3.0:
            self.instancemenu.addChild(self.dynamic_widgets['moveButton'])
        else:
            if self.instance_to_agent.has_key(instance.getFifeId()):
                self.instancemenu.addChild(self.dynamic_widgets['talkButton'])
                self.instancemenu.addChild(self.dynamic_widgets['kickButton'])
        # And show it :)
        self.instancemenu.position = (clickpoint.x, clickpoint.y)
        self.instancemenu.show()

    def hide_instancemenu(self):
        if self.instancemenu:
            self.instancemenu.hide()

    def show(self, buttonText, text, callback):
        self.gameStatusWindow.mapEvents({ 'playButton' : callback })
        self.gameStatusWindow.findChild(name='playButton').text = buttonText
        self.gameStatusWindow.distributeData({ 'gameStatus' : open(text).read() })
        self.gameStatusWindow.show()
