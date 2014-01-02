from fife import fife
from fife.extensions import *
from fife.extensions.fife_settings import Setting
from threading import Timer
import world
import agents.agent_manager
from dialog import Dialog

TDS = Setting(app_name="rio_de_hola")
STATE_START, STATE_PLAY, STATE_PAUSE, STATE_END = xrange(4)
EV_START, EV_ACTION_FINISHED, EV_HIT = xrange(3)
STATE_WARRIOR1, STATE_WARRIOR2 = xrange(2)


class Game():
    __game = None

    def __init__(self, engine):
        Game.__game = self
        self.applicationListener = None #run.py
        self.instance_to_agent = {}
        self.world= world.World(engine)
        self.agentManager = agents.agent_manager.AgentManager(self.world)
        self.dialog = Dialog(self)
        self.reset()

    @classmethod
    def getGame(cls):
        return Game.__game

    def reset(self):
        self._state = STATE_START
        self._lives = 3
        self._quest = 0
        self._secState = None

    def setApplicationListener(self, applicationListener):
        self.applicationListener = applicationListener

    def event(self, ev, *args):
        #handle events
        if ev == EV_START:
            self.state = STATE_START
            self.dialog.show("Start", "misc/game/start.txt", self.start)
        elif ev == EV_HIT:
            self._lives -= 1
            if self._lives <= 0:
                print "DEAAAAAD"
                self.reset()
                self.event('start')
        elif ev == EV_ACTION_FINISHED:
            if args[0] == "warrior":
                pass

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

            if instance.getObject().getId() == 'beekeeper':
                beekeeperTexts = TDS.get("rio", "beekeeperTexts")
                instance.say(random.choice(beekeeperTexts), 5000)
            if instance.getObject().getId() == 'girl':
                girlTexts = TDS.get("rio", "girlTexts")
                instance.say(random.choice(girlTexts), 5000)
            if instance.getObject().getId() == 'warrior':
                warriorTexts = TDS.get("rio", "warriorTexts")
                if self._quest == 1:
                    if self._secState == None:
                        self._secState = STATE_WARRIOR1
                        self.agentManager.warrior.say(warriorTexts[0])
                        t = Timer(2.5, self.warr1)
                        t.start()
                    else:
                        self.agentManager.warrior.say(warriorTexts[1])
                else:
                    self.agentManager.warrior.say(warriorTexts[2])
                #self.agentManager.warrior.follow_hero()

    def warr1(self, *args):
        warriorTexts = TDS.get("rio", "warriorTexts")
        self.agentManager.warrior.say(warriorTexts[1])
        t = Timer(2.5, self.warr2)
        t.start()

    def warr2(self, *args):
        self.agentManager.warrior.follow_hero()

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
            self.agentManager.toggleAgent(self.world, face_button)

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

    def load(self, map):
        self.world.load(map)

    def save(self, file):
        self.world.save(file)

    def pump(self):
        self.world.pump()