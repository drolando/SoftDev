from fife import fife
from fife.extensions import *
from fife.extensions.fife_settings import Setting
from fife.extensions.pychan import widgets
from fife.fife import Color
from fife.fife import Font
from threading import Timer
import world
import random
import agents.agent_manager
import agents.bee
from dialog import Dialog
from ConfigParser import SafeConfigParser
import sys, os
import datetime

TDS = Setting(app_name="rio_de_hola")
STATE_START, STATE_PLAY, STATE_PAUSE, STATE_END = xrange(4)
EV_START, EV_ACTION_FINISHED, EV_HIT, EV_BEE_ARRIVED, EV_QUEST_2, EV_BEE_DEAD, EV_QUEST_3, EV_EXPLOSION, EV_SHRINE = xrange(9)
STATE_WARRIOR1, STATE_WARRIOR2, STATE_BEE1, STATE_SWORD, STATE_BEE2, STATE_BEE3, STATE_WIZARD1, STATE_WIZARD2 = xrange(8)


class Game():
    __game__ = None

    def __init__(self, engine):
        Game.__game__ = self
        self.applicationListener = None #run.py
        self.instance_to_agent = {}
        self.engine = engine #needed for exit function
        self.world= world.World(engine)
        self.agentManager = agents.agent_manager.AgentManager(self.world)
        self.dialog = Dialog(self)
        self.reset()


    @classmethod
    def getGame(cls):
        return Game.__game__

    def reset(self):
        self._state = STATE_START
        self._quest = 0
        self._secState = None

    def setApplicationListener(self, applicationListener):
        self.applicationListener = applicationListener

    """
        This method handles all the events. It should be the only function called from
        outside the Game class except for the callback methods (like onTalkButtonPress).
        Combining the event with the current state it decides how to responde.
    """
    def event(self, ev, *args):
        if ev == EV_START:
            if self._state == STATE_START:
                self.dialog.show("Start", "misc/game/start.txt", self.start)
            else:
                self.setState(STATE_PLAY)
        elif ev == EV_HIT:
            self.agentManager.getActiveAgent().health -= 10
            self.setHealth()
            if self.agentManager.getActiveAgent().health <= 0:
                self.deleteStatus()
                self.dialog.show("Exit", "misc/game/game_over.txt", self.game_over)
        elif ev == EV_ACTION_FINISHED:
            pass
        elif ev == EV_BEE_ARRIVED:
            if self.agentManager.beesAtHome():
                self._secState = STATE_BEE1
        elif ev == EV_QUEST_2:
            self.setState(STATE_PAUSE)
            self.dialog.show("Play", "misc/game/quest2.txt", self.quest2)
        elif ev == EV_BEE_DEAD:
            if self.agentManager.beesDead():
                self._secState = STATE_BEE3
        elif ev == EV_QUEST_3:
            self.setState(STATE_PAUSE)
            self.dialog.show("Play", "misc/game/quest3.txt", self.quest3)
        elif ev == EV_SHRINE:
            self._state = STATE_END
            self._secState = STATE_END
            self.dialog.show("Exit", "misc/game/end.txt", self.end)
        else:
            print "Event not recognized: {}".format(ev)

    """
        The functions in this block are callbacks from the gameStatus popup
    """
    def start(self):
        self.dialog.hide()
        self.dialog.show("Play", "misc/game/quest1.txt", self.quest1)

    def quest1(self):
        self.dialog.hide()
        self._quest = 1
        self.setState(STATE_PLAY)

    def quest2(self):
        self.dialog.hide()
        self._quest = 2
        self.setState(STATE_PLAY)
        self._secState = STATE_BEE2

    def quest3(self):
        self.dialog.hide()
        self._quest = 3
        self.setState(STATE_PLAY)
        self._secState = STATE_WIZARD2

    def game_over(self):
        self.exit()

    def end(self):
        self.deleteStatus()
        self.exit()

    """
        The following functions allow the user to save, load and delete the game status.
    """
    def show_save_dialog(self):
        if self._state == STATE_PLAY:
            self._old_state = self._state
            self.setState(STATE_PAUSE)
            self.dialog.hide_instancemenu()
            self.dialog.show_exit_menu(self.saveStatus, self.loadButtonPress, self.exit)
        else:
            if self.dialog.exit_load_visible():
                self.dialog.hide_exit_menu()
                self.dialog.hide_load_menu()
                self.setState(STATE_PLAY)


    def exit(self):
        self.agentManager.destroy()
        cmd = fife.Command()
        cmd.setSource(None)
        cmd.setCommandType(fife.CMD_QUIT_GAME)
        self.engine.getEventManager().dispatchCommand(cmd)

    def saveStatus(self):
        name_tmp = "./saves/{:s}".format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M"))
        name = name_tmp
        i = 1
        while os.path.exists(name):
            name = "{:s}_{:d}".format(name_tmp, i)
            i += 1

        Config = SafeConfigParser()
        Config.add_section("GAME")
        Config.set("GAME", "quest", str(self._quest))
        Config.set("GAME", "state", str(self._old_state))
        Config.set("GAME", "secState", str(self._secState))
        Config.add_section("PLAYABLE_AGENTS")
        for a in self.agentManager.playableAgent:
            c = a.agent.getLocation().getMapCoordinates()
            Config.set("PLAYABLE_AGENTS", a.agentName.replace(':', '_'), 
                        "{:d};{:d};{:f};{:f};{:d}".format(int(a.health), int(a.magic), c.x*2, c.y*2, int(a._mode)))
        Config.add_section("BEES")
        for b in self.agentManager.bees:
            c = b.agent.getLocation().getMapCoordinates()
            Config.set("BEES", b.agentName.replace(':','_'), "{:f};{:f};{:d};{:d}".format(c.x*2, c.y*2, int(b.state), int(b.mode)))
        cfg = open(name, "w")
        Config.write(cfg)
        cfg.close()
        cfg = open("./conf", "w")
        Config.write(cfg)
        cfg.close()
        self.setState(STATE_PLAY)
        self.dialog.hide_exit_menu()

    def deleteStatus(self):
        Config = SafeConfigParser()
        cfg = open("./conf", "w")
        cfg.close()

    def loadButtonPress(self):
        list = []
        tmp_list = []
        for fn in os.listdir("./saves/"):
            tmp_list.append(fn)
        tmp_list.sort(reverse=True)
        i = 1
        for fn in tmp_list:
            obj = LoadObject(self, fn)
            list.append(obj)
            i += 1
            if i > 8:
                break
        self.dialog.hide_exit_menu()
        self.dialog.show_load_menu(list)

    def loadStatus(self, name="./conf"):
        config = SafeConfigParser()
        config.read(name)
        try:
            if config.sections() != []:
                if config.has_section("GAME"):
                    self._quest = config.getint("GAME", "quest")
                    self.setState(config.getint("GAME", "state"))
                    self._secState = config.get("GAME", "secState")
                    if self._secState != "None":
                        self._secState = int(self._secState)
                if config.has_section("PLAYABLE_AGENTS"):
                    self.agentManager.reset()
                    for l in config.options("PLAYABLE_AGENTS"):
                        name = "{:s}:{:s}".format(l.split('_')[0].upper(), l.split('_')[1])
                        a = self.agentManager.getAgentByName(name)
                        params = config.get("PLAYABLE_AGENTS", l).split(';')
                        if a != None:
                            a.health = int(params[0])
                            a.magic = int(params[1])
                            l = a.agent.getLocation()
                            l.setLayerCoordinates(fife.ModelCoordinate(*(int(float(params[2])), int(float(params[3])))))
                            a.agent.setLocation(l)
                            a._mode = int(params[4])
                        self.agentManager.addNewPlayableAgent(name)
                if config.has_section("BEES"):
                    for l in config.options("BEES"):
                        name = "{:s}:{:s}:{:s}".format(l.split('_')[0].upper(), l.split('_')[1], l.split('_')[2])
                        b = self.agentManager.getAgentByName(name)
                        params = config.get("BEES", l).split(';')
                        if b != None:
                            l = fife.Location(self.world.map.getLayer('TechdemoMapGroundObjectLayer'))
                            l.setLayerCoordinates(fife.ModelCoordinate(*(int(float(params[0])), int(float(params[1])))))
                            b.agent.setLocation(l)
                            b.state = int(params[2])
                            b.mode = int(params[3])
                            b.start()
                self.dialog.hide_exit_menu()
                self.dialog.hide_load_menu()
        except AttributeError as e:
            print "###################################################################################"
            print "Unexpected error:", sys.exc_info()[0]
            print e.message
            print "--- Configuration file malformed. Deleted. ---"
            print "--- Please, restart again the game ---"
            print "###################################################################################"
            self.deleteStatus()
            self.exit()

    """
        This function set the current state: if it's STATE_PAUSE it shows the PAUSE label below the
        user icon. If it's a different state it hides that label.
    """
    def setState(self, state):
        self._state = state
        if state == STATE_PLAY:
            self.statusBar.hide()
        else:
            self.statusBar.show()

    """
        These functions handle the user's clicks on the map or on one character.
        If the game is paused, they'll be ignored.
    """
    def leftClick(self, clickpoint):
        if self._state == STATE_PLAY:
            self.dialog.hide_instancemenu()
            self.agentManager.getActiveAgent().run(clickpoint)

    def rightClick(self, instances, clickpoint):
        if self._state == STATE_PLAY:
            if instances:
                self.show_instancemenu(clickpoint, instances[0])

    """
        The following functions are the callbacks for the instancemenu popup.
    """
    # Callbacks from the popupmenu
    def onMoveButtonPress(self):
        if self._state == STATE_PLAY:
            self.dialog.hide_instancemenu()
            self.agentManager.getActiveAgent().run(self.dialog.instancemenu.instance.getLocationRef())

    def onKickButtonPress(self):
        if self._state == STATE_PLAY:
            self.dialog.hide_instancemenu()
            activeAgent = self.agentManager.getActiveInstance()
            instance = self.dialog.instancemenu.instance
            target_distance = activeAgent.getLocation().getLayerDistanceTo(instance.getLocation())
            if target_distance < 3:
                self.agentManager.getActiveAgent().kick(self.dialog.instancemenu.instance.getLocationRef())
                target = self.agentManager.getAgentFromId(instance.getFifeId())
                if target != None:
                    target.onKick()
            else:
                activeAgent.say("Too far...", 2000)

    def onInspectButtonPress(self):
        if self._state == STATE_PLAY:
            self.dialog.hide_instancemenu()
            inst = self.dialog.instancemenu.instance
            saytext = []
            saytext.append('%s' % inst.getObject().getId())
            self.agentManager.getActiveAgent().say('\n'.join(saytext))

    def onOpenButtonPress(self):
        if self._state == STATE_PLAY:
            self.dialog.hide_instancemenu()
            self.agentManager.cage.open()
            self._secState = STATE_SWORD
            self.agentManager.warrior.gotSword()
            #self.event(EV_QUEST_2)

    def onAttackButtonPress(self):
        if self._state == STATE_PLAY:
            self.dialog.hide_instancemenu()
            activeAgent = self.agentManager.getActiveInstance()
            instance = self.dialog.instancemenu.instance
            target_distance = activeAgent.getLocation().getLayerDistanceTo(instance.getLocation())
            if target_distance < 3:
                self.agentManager.warrior.attack(instance.getLocationRef())
                self.agentManager.getAgentFromId(instance.getFifeId()).onAttack()
            else:
                activeAgent.say("Too far...", 2000)

    def onSpellButtonPress(self):
        if self._state == STATE_PLAY:
            self.dialog.hide_instancemenu()
            instance = self.dialog.instancemenu.instance
            self.agentManager.wizard.cast_spell(instance)

    def onActivateButtonPress(self):
        if self._state == STATE_PLAY:
            self.event(EV_SHRINE)

    """
        ----------------------------------------------------------------
    """
    def onTalkButtonPress(self):
        if self._state == STATE_PLAY:
            self.dialog.hide_instancemenu()
            instance = self.dialog.instancemenu.instance
            self.agentManager.getActiveAgent().talk(instance.getLocationRef())
            if instance.getObject().getId() == 'beekeeper':
                beekeeperTexts = TDS.get("rio", "beekeeperTexts")
                if self._secState == STATE_WARRIOR2:
                    instance.say(beekeeperTexts[0], 5000)
                elif self._secState == STATE_BEE1:
                    instance.say(beekeeperTexts[1], 5000)
                else:
                    instance.say(beekeeperTexts[2], 3000)
            if instance.getObject().getId() == 'girl':
                girlTexts = TDS.get("rio", "girlTexts")
                instance.say(random.choice(girlTexts), 5000)
            if instance.getObject().getId() == 'warrior':
                warriorTexts = TDS.get("rio", "warriorTexts")
                if self._quest == 1:
                    if self._secState == None:
                        self.setState(STATE_PAUSE)
                        self._secState = STATE_WARRIOR1
                        self.agentManager.warrior.say(warriorTexts[0])
                        t = Timer(2.5, self.warr1)
                        t.start()
                    else:
                        self.agentManager.warrior.say(warriorTexts[1])
                        self.agentManager.warrior.follow_hero()
                        self.agentManager.addNewPlayableAgent("PC:warrior")
                else:
                    self.agentManager.warrior.say(warriorTexts[2])
                    self.agentManager.addNewPlayableAgent("PC:warrior")
            if instance.getObject().getId() == 'wizard':
                wizardTexts = TDS.get("rio", "wizardTexts")
                if self._quest == 1:
                    self.agentManager.wizard.say(wizardTexts[0])
                elif self._quest == 2:
                    if self._secState == STATE_BEE2:
                        self.agentManager.wizard.say(wizardTexts[0])
                    elif self._secState == STATE_BEE3:
                        self.setState(STATE_PAUSE)
                        self._secState = STATE_WIZARD1
                        self.agentManager.wizard.say(wizardTexts[1])
                        t = Timer(2.0, self.wiz1)
                        t.start()
                elif self._quest == 3:
                    self.agentManager.wizard.say(wizardTexts[3])
            if instance.getObject().getId() == 'chemist':
                chemistTexts = TDS.get("rio", "chemistTexts")
                if self._quest == 2:
                    if self._secState == STATE_WIZARD1 and self.agentManager.getActiveAgent().agentName == "PC:wizard":
                        self.setState(STATE_PAUSE)
                        wizardTexts = TDS.get("rio", "wizardTexts")
                        self.agentManager.wizard.say(wizardTexts[4])
                        t = Timer(2.5, self.chem1)
                        t.start()
                    else:
                        self.agentManager.chemist.say(chemistTexts[0])
                else:
                    self.agentManager.chemist.say(chemistTexts[0])
            if instance.getObject().getId() == 'bee':
                beeTexts = TDS.get("rio", "beeTexts")
                self.agentManager.getAgentFromId(instance.getFifeId()).say(beeTexts)

    """
        The following methods are used to make an agent say another sentence or do some
        action after some seconds.
    """
    def warr1(self, *args):
        warriorTexts = TDS.get("rio", "warriorTexts")
        self.agentManager.warrior.say(warriorTexts[1])
        t = Timer(2.5, self.warr2)
        t.start()
        self._secState = STATE_WARRIOR2

    def warr2(self, *args):
        self.agentManager.warrior.follow_hero()
        self.agentManager.addNewPlayableAgent("PC:warrior")
        self.setState(STATE_PLAY)

    def wiz1(self, *args):
        wizardTexts = TDS.get("rio", "wizardTexts")
        self.agentManager.wizard.say(wizardTexts[2])
        t = Timer(2.5, self.wiz2)
        t.start()

    def wiz2(self, *args):
        self.setState(STATE_PLAY)
        self.agentManager.wizard.follow_hero()
        self.agentManager.addNewPlayableAgent("PC:wizard")

    def chem1(self, *args):
        chemistTexts = TDS.get("rio", "chemistTexts")
        self.agentManager.chemist.say(chemistTexts[1])
        t = Timer(2.5, self.chem2)
        t.start()

    def chem2(self, *args):
        chemistTexts = TDS.get("rio", "chemistTexts")
        self.agentManager.chemist.say(chemistTexts[2])
        t = Timer(2.5, self.chem3)
        t.start()

    def chem3(self, *args):
        self.setState(STATE_PLAY)
        self.event(EV_QUEST_3)

    """
        Handle the toggle agent functionality.
    """
    def onFacePress(self):
        if self._state == STATE_PLAY:
            self.agentManager.toggleAgent(self.world, self.face_button)
            self.setHealth()
            self.setMagic()

    def setFaceButton(self, face_button):
        self.face_button = face_button

    """
        Display the hint dialog.
    """
    def onHintsButtonPress(self):
        if self._state == STATE_PLAY:
            self.setState(STATE_PAUSE)
            if self._quest == 1:
                self.dialog.show("Continue", "misc/game/quest1.txt", self.closeDialog)
            elif self._quest == 2:
                self.dialog.show("Continue", "misc/game/quest2.txt", self.closeDialog)
            elif self._quest == 3:
                self.dialog.show("Continue", "misc/game/quest3.txt", self.closeDialog)

    def closeDialog(self):
        self.setState(STATE_PLAY)
        self.dialog.hide()

    """
        The following functions change the health and magic bars accordingly to the agent's properties
    """
    def setHealth(self):
        health = self.agentManager.getActiveAgent().health
        if health < 0:
            health = 0
        if health > 100:
            health = 100
        self.health_bar.size = (141*health/100, 11)

    def setMagic(self):
        magic = self.agentManager.getActiveAgent().magic
        if magic < 0:
            magic = 0
        if magic > 100:
            magic = 100
        self.magic_bar.size = (130*magic/100, 10)

    """
        These two methods are called from run.py to set the pointers to the widgets.
    """
    def setPercBar(self, health_bar, magic_bar, health_cont):
        self.health_bar = health_bar
        self.health_cont = health_cont
        self.magic_bar = magic_bar

    def setStatusBar(self, stbar):
        self.statusBar = stbar


    """
        Shows -------------------------------------------------------------
    """
    def show_instancemenu(self, clickpoint, instance):
        instance.setBlocking(False)
        fife_id = instance.getFifeId()
        id = instance.getId()
        if fife_id == self.agentManager.getActiveInstance().getFifeId():
            return
        if id[:-2] == "NPC:bee:" and self.agentManager.getAgentFromId(fife_id).mode == agents.bee._MODE_DEAD:
            return
        # Add the buttons according to circumstances.
        buttons = ['inspectButton']

        target_distance = self.agentManager.getActiveInstance().getLocationRef().getLayerDistanceTo(instance.getLocationRef())
        if target_distance > 5.0:
            buttons.append('moveButton')
        else:
            if self.instance_to_agent.has_key(fife_id) and id != "sword_crate":
                buttons.append('talkButton')

        if self._quest == 1:
            if id == "sword_crate" and self._secState == STATE_BEE1:
                buttons.append("openButton")
            if ((id[:-2] != "NPC:bee:" or int(id[-2:]) <= 3) and self.agentManager.getActiveAgent().agentName == "PC:boy"
                     and self._secState == STATE_WARRIOR2):
                    buttons.append('kickButton')
        elif self._quest == 2:
            if (self._secState == STATE_BEE2 and self.agentManager.getActiveAgent().agentName == "PC:warrior"
                and id[:-2] == "NPC:bee:" and int(id[-2:]) >= 4 and target_distance < 4.0):
                buttons.append('attackButton')
        elif self._quest == 3:
            if (self._secState == STATE_WIZARD2 and self.agentManager.getActiveAgent().agentName == "PC:wizard"
                and instance.getObject().getId() == "trees:05"):
                buttons.append('spellButton')
            elif instance.getObject().getId() == "shrine" and target_distance <= 6:
                buttons.append('activateButton')
        self.dialog.show_instancemenu(clickpoint, instance, buttons)

    """
        These functions call the respective functions in world.py
    """
    def load(self, map):
        self.world.load(map)
        self.loadStatus()
        self.setHealth()
        self.setMagic()

    def save(self, file):
        self.world.save(file)

    def pump(self):
        self.world.pump()

class LoadObject():
    def __init__(self, game, name):
        self.name = name
        self.game = game
    def callback(self):
        self.game.loadStatus("./saves/{:s}".format(self.name))
        self.game.dialog.hide_load_menu()
