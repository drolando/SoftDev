from fife import fife
from fife.extensions import *

from dialog import Dialog

STATE_START, STATE_PLAY, STATE_PAUSE, STATE_END = xrange(4)


class Game():
    def __init__(self, world):
        self.applicationListener = None #run.py
        self.instance_to_agent = {}
        self.world = world
        self.agentManager = self.world.agentManager
        self.dialog = Dialog(self)
        self.reset()

    def reset(self):
        self._state = STATE_START
        self._lives = 3
        self._quest = 0

    def setApplicationListener(self, applicationListener):
        self.applicationListener = applicationListener

    def event(self, ev):
        #handle events
        if ev == 'start':
            self.dialog.show("Start", "misc/game/start.txt", self.start)
        else:
            print "Event not recognized: {}".format(ev)

    def start(self):
        self.dialog.gameStatusWindow.hide()
        self.dialog.show("Play", "misc/game/quest1.txt", self.quest1)

    def quest1(self):
        self.dialog.gameStatusWindow.hide()
        self._quest = 1
        self._state = STATE_PLAY

    def leftClick(self, clickpoint):
        if self._state == STATE_PLAY:
            self.dialog.hide_instancemenu()
            self.agentManager.getActiveAgent().run(clickpoint)

    def rightClick(self, instances, clickpoint):
        if self._state == STATE_PLAY:
            print "selected instances on agent layer: ", [i.getObject().getId() for i in instances]
            if instances:
                self.agentManager.rightButtonClicked(instances, clickpoint)

    # Callbacks from the popupmenu
    def onMoveButtonPress(self):
        if self._state == STATE_PLAY:
            self.dialog.hide_instancemenu()
            self.agentManager.run(self.dialog.instancemenu.instance.getLocationRef())

    def onTalkButtonPress(self):
        if self._state == STATE_PLAY:
            self.dialog.hide_instancemenu()
            instance = self.dialog.instancemenu.instance
            self.agentManager.talk(instance)

    def onKickButtonPress(self):
        if self._state == STATE_PLAY:
            self.dialog.hide_instancemenu()
            self.agentManager.kick(self.dialog.instancemenu.instance.getLocationRef())
            target = self.agentManager.getAgentFromId(self.dialog.instancemenu.instance.getFifeId())
            if target != None:
                target.onKick()

    def onInspectButtonPress(self):
        if self._state == STATE_PLAY:
            self.dialog.hide_instancemenu()
            inst = self.dialog.instancemenu.instance
            saytext = []
            saytext.append('%s' % inst.getObject().getId())
            self.agentManager.getHero().agent.say('\n'.join(saytext), 3500)

    def onFacePressed(self, face_button):
        if self._state == STATE_PLAY:
            self.agentManager.toggleAgent(face_button)

    def show_instancemenu(self, clickpoint, instance):
        if instance.getFifeId() == self.agentManager.getHero().agent.getFifeId():
            return
        # Add the buttons according to circumstances.
        buttons = ['inspectButton']

        target_distance = self.agentManager.getHero().agent.getLocationRef().getLayerDistanceTo(instance.getLocationRef())
        if target_distance > 3.0:
            buttons.append('moveButton')
        else:
            if self.instance_to_agent.has_key(instance.getFifeId()):
                buttons.append('talkButton')
                buttons.append('kickButton')
        self.dialog.show_instancemenu(clickpoint, instance, buttons)