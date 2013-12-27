from fife import fife
from fife.extensions import *

from dialog import Dialog

STATE_START, STATE_LV1, STATE_END = xrange(3)

class Game():
    def __init__(self, world):
        self.applicationListener = None
        self.world = world
        self.agentManager = self.world.agentManager
        self.dialog = Dialog(self)
        self.state = STATE_START
        self.lives = 3

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
        self.dialog.show("Play", "misc/game/level1.txt", self.dialog.gameStatusWindow.hide)

    def leftClick(self, clickpoint):
        self.dialog.hide_instancemenu()
        self.agentManager.getActiveAgent().run(clickpoint)

    def rightClick(self, instances, clickpoint):
        print "selected instances on agent layer: ", [i.getObject().getId() for i in instances]
        if instances:
            self.agentManager.rightButtonClicked(instances, clickpoint)

    # Callbacks from the popupmenu
    def onMoveButtonPress(self):
        self.dialog.hide_instancemenu()
        self.agentManager.run(self.dialog.instancemenu.instance.getLocationRef())

    def onTalkButtonPress(self):
        self.dialog.hide_instancemenu()
        instance = self.dialog.instancemenu.instance
        self.agentManager.talk(instance)

    def onKickButtonPress(self):
        self.dialog.hide_instancemenu()
        self.agentManager.kick(self.dialog.instancemenu.instance.getLocationRef())
        self.dialog.instancemenu.instance.say('Hey!', 1000)

    def onInspectButtonPress(self):
        self.dialog.hide_instancemenu()
        inst = self.dialog.instancemenu.instance
        saytext = []
        # if inst.getId():
            # saytext.append('This is %s,' % inst.getId())
        # saytext.append(' ID %s and' % inst.getFifeId())
        saytext.append('%s' % inst.getObject().getId())
        self.agentManager.getHero().agent.say('\n'.join(saytext), 3500)

    