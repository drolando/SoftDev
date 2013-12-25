from fife import fife
import math, random
from code.common.common import ProgrammingError
from hero import Hero
from girl import Girl
from beekeeper import Beekeeper
from bee import Bee
#from agent import create_anonymous_agents
from fife.extensions.fife_settings import Setting

TDS = Setting(app_name="rio_de_hola")

class AgentManager():

    def __init__(self, world):
        self.player = 0
        self.player_faces = ['gui/images/hud_boy.png', 'gui/images/hud_girl.png']
        self.world = world

    def initAgents(self):
        """
        Setup agents.

        For this techdemo we have a very simple 'active things on the map' model,
        which is called agents. All rio maps will have a separate layer for them.

        Note that we keep a mapping from map instances (C++ model of stuff on the map)
        to the python agents for later reference.
        """
        self.agentlayer = self.world.map.getLayer('TechdemoMapGroundObjectLayer')
        self.world.agentlayer = self.agentlayer
        self.hero = Hero(TDS, self.world.model, 'PC', self.agentlayer)
        self.world.instance_to_agent[self.hero.agent.getFifeId()] = self.hero
        self.hero.start()

        self.girl = Girl(TDS, self.world.model, 'NPC:girl', self.agentlayer)
        self.world.instance_to_agent[self.girl.agent.getFifeId()] = self.girl
        self.girl.start()

        self.beekeepers = create_anonymous_agents(TDS, self.world.model, 'beekeeper', self.agentlayer, Beekeeper)
        for beekeeper in self.beekeepers:
            self.world.instance_to_agent[beekeeper.agent.getFifeId()] = beekeeper
            beekeeper.start()

        '''self.bees = create_anonymous_agents(TDS, self.world.model, 'bee', self.agentlayer, Bee)
        for bee in self.bees:
            self.world.instance_to_agent[bee.agent.getFifeId()] = bee
            bee.start()'''
        self.bees = []
        for i in range(1, 8):
            bee = Bee(TDS, self.world.model, 'NPC:bee:0{}'.format(i), self.agentlayer)
            self.bees.append(bee)
            bee.start()

        self.active_agent = self.hero

    def reset(self):
        self.hero, self.girl = None, None

    def getActiveAgent(self):
        if self.player == 0:
            return self.hero
        return self.girl

    def getActiveAgentLocation(self):
        if self.player == 0:
            return self.hero.agent.getLocation()
        return self.girl.agent.getLocation()

    def talk(self, instance):
        self.hero.talk(instance.getLocationRef())
        if instance.getObject().getId() == 'beekeeper':
            beekeeperTexts = TDS.get("rio", "beekeeperTexts")
            instance.say(random.choice(beekeeperTexts), 5000)
        if instance.getObject().getId() == 'girl':
            girlTexts = TDS.get("rio", "girlTexts")
            instance.say(random.choice(girlTexts), 5000)

    def kick(self, location):
        self.hero.kick(location)

    def run(self, location):
        self.active_agent.run(location)

    def getHero(self):
        return self.hero;

    def getGirl(self):
        return self.girl

    def toggleAgent(self, world, face_button):
        self.player = (self.player + 1) % 2
        self.world.player = self.player
        
        face_button.up_image = self.player_faces[self.player]
        face_button.down_image = self.player_faces[self.player]
        face_button.hover_image = self.player_faces[self.player]
        self.hero.idle()
        self.girl.idle()
        self.girl.isActive = self.player;
        if self.player == 0:
            world.cameras['main'].attach(self.hero.agent)
            world.cameras['small'].attach(self.girl.agent)
            self.active_agent = self.hero
        else:
            world.cameras['main'].attach(self.girl.agent)
            world.cameras['small'].attach(self.hero.agent)
            self.active_agent = self.girl

    def rightButtonClicked(self, instances, clickpoint):
        if (self.player == 0):
            self.world.show_instancemenu(clickpoint, instances[0])



def create_anonymous_agents(settings, model, objectName, layer, agentClass):
    print ">>>>>> agent.py --> create_anonymous_agents"
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
