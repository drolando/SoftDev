from fife import fife
import math, random
from code.common.common import ProgrammingError
from hero import Hero
from girl import Girl
from priest import Priest
from beekeeper import Beekeeper
import code.agents.bee
from warrior import Warrior
from fireball import Fireball
import code.game
from fife.extensions.fife_settings import Setting

TDS = Setting(app_name="rio_de_hola")

class AgentManager():

    def __init__(self, world):
        self.player = 0
        self.player_faces = ['gui/images/hud_boy.png', 'gui/images/hud_girl.png', 'gui/images/hud_boy.png']
        self.agent_list = []
        self.game = code.game.Game.getGame()

    def initAgents(self, world):
        self.agentlayer = world.map.getLayer('TechdemoMapGroundObjectLayer')
        world.agentlayer = self.agentlayer
        self.hero = Hero(TDS, world.model, 'PC', self.agentlayer)
        self.game.instance_to_agent[self.hero.agent.getFifeId()] = self.hero
        self.hero.start()
        self.agent_list.append(self.hero)

        self.girl = Girl(TDS, world.model, 'NPC:girl', self.agentlayer)
        self.game.instance_to_agent[self.girl.agent.getFifeId()] = self.girl
        self.girl.start()
        self.agent_list.append(self.girl)

        self.priest = Priest(TDS, world.model, 'NPC:priest', self.agentlayer)
        self.game.instance_to_agent[self.priest.agent.getFifeId()] = self.priest
        self.priest.start()

        self.beekeepers = create_anonymous_agents(TDS, world.model, 'beekeeper', self.agentlayer, Beekeeper)
        for beekeeper in self.beekeepers:
            self.game.instance_to_agent[beekeeper.agent.getFifeId()] = beekeeper
            beekeeper.start()
            self.agent_list.append(beekeeper)

        self.bees = []
        for i in range(1, 8):
            bee = code.agents.bee.Bee(TDS, world.model, 'NPC:bee:0{}'.format(i), self.agentlayer, self)
            self.bees.append(bee)
            self.game.instance_to_agent[bee.agent.getFifeId()] = bee
            bee.start()
            self.agent_list.append(bee)

        self.warrior = Warrior(TDS, world.model, 'NPC:warrior', self.agentlayer)
        self.game.instance_to_agent[self.warrior.agent.getFifeId()] = self.warrior
        self.warrior.start()

        self.active_agent = self.hero

    def beesAtHome(self):
        for bee in self.bees:
            print "-------------------------- bee name: ", bee.agentName[-2:]
            if bee.agentName[-2:] <= 2 and bee.mode == code.agents.bee._MODE_WILD:
                return False
        return True

    def reset(self):
        self.hero, self.girl, self.warrior = None, None, None

    def getActiveAgent(self):
        if self.player == 0:
            return self.hero
        elif self.player == 1:
            return self.girl
        elif self.player == 2:
            return self.warrior
        return None

    def getActiveInstance(self):
        if self.player == 0:
            return self.agentlayer.getInstance('PC')
        elif self.player == 1:
            return self.agentlayer.getInstance('NPC:girl')
        elif self.player == 2:
            return self.agentlayer.getInstance('NPC:warrior')
        return None

    def getActiveAgentLocation(self):
        return self.active_agent.agent.getLocation()

    def talk(self, instance):
        self.getActiveAgent().talk(instance.getLocationRef())

    def kick(self, location):
        self.hero.kick(location)

    def run(self, location):
        self.active_agent.run(location)

    def getHero(self):
        return self.hero

    def getGirl(self):
        return self.girl

    def event(self, ev):
        if ev == 'attack':
            self.game.event('hit')

    def toggleAgent(self, world, face_button):
        self.player = (self.player + 1) % 3

        face_button.up_image = self.player_faces[self.player]
        face_button.down_image = self.player_faces[self.player]
        face_button.hover_image = self.player_faces[self.player]
        self.hero.idle()
        self.girl.idle()
        self.warrior.idle()

        self.hero.isActive = True if self.player==0 else False
        self.girl.isActive = True if self.player==1 else False
        self.warrior.isActive = True if self.player==2 else False
        if self.player == 0:
            world.cameras['main'].attach(self.hero.agent)
            world.cameras['small'].attach(self.girl.agent)
            self.active_agent = self.hero
            self.girl.follow_hero()
            self.warrior.follow_hero()
        elif self.player == 1:
            world.cameras['main'].attach(self.girl.agent)
            world.cameras['small'].attach(self.hero.agent)
            self.active_agent = self.girl
            self.hero.follow_hero()
            self.warrior.follow_hero()
        elif self.player == 2:
            world.cameras['main'].attach(self.warrior.agent)
            world.cameras['small'].attach(self.hero.agent)
            self.active_agent = self.warrior
            self.hero.follow_hero()
            self.girl.follow_hero()

    def getAgentFromId(self, fifeId):
        for ag in self.agent_list:
            if ag.agent.getFifeId() == fifeId:
                return ag
        return None




def create_anonymous_agents(settings, model, objectName, layer, agentClass):
    agents = []
    instances = [a for a in layer.getInstances() if a.getObject().getId() == objectName]
    i = 0
    for a in instances:
        agentName = '%s:i:%d' % (objectName, i)
        i += 1
        agent = agentClass(settings, model, agentName, layer, False)
        agent.agent = a
        a.addActionListener(agent)
        agents.append(agent)
    return agents
