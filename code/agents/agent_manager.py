from fife import fife
from code.common.common import ProgrammingError
from hero import Hero
from girl import Girl
from beekeeper import Beekeeper
from agent import create_anonymous_agents
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

    def toggleAgent(self, world):
        self.player = (self.player + 1) % 2
        self.world.player = self.player
        
        face_button.up_image = self.player_faces[self.player]
        face_button.down_image = self.player_faces[self.player]
        face_button.hover_image = self.player_faces[self.player]
        world.hero.idle()
        world.girl.idle()
        world.girl.isActive = self.player;
        if self.player == 0:
            world.cameras['main'].attach(world.hero.agent)
            world.cameras['small'].attach(world.girl.agent)
        else:
            world.cameras['main'].attach(world.girl.agent)
            world.cameras['small'].attach(world.hero.agent)





