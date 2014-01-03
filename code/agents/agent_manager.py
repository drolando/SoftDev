from fife import fife
import math, random
from code.common.common import ProgrammingError
from boy import Boy
from girl import Girl
from wizard import Wizard
from beekeeper import Beekeeper
from chemist import Chemist
import code.agents.bee
from warrior import Warrior
from fireball import Fireball
import code.game
from fife.extensions.fife_settings import Setting

TDS = Setting(app_name="rio_de_hola")

class AgentManager():

    def __init__(self, world):
        self.player = 0
        self.player_faces = ['gui/images/hud_boy.png', 'gui/images/hud_girl.png', 'gui/images/hud_warrior.png', 'gui/images/hud_wizard.png']
        self.agent_list = []
        self.game = code.game.Game.getGame()

    def initAgents(self, world):
        self.agentlayer = world.map.getLayer('TechdemoMapGroundObjectLayer')
        world.agentlayer = self.agentlayer
        self.boy = Boy(TDS, world.model, 'PC:boy', self.agentlayer)
        self.game.instance_to_agent[self.boy.agent.getFifeId()] = self.boy
        self.boy.start()
        self.agent_list.append(self.boy)

        self.girl = Girl(TDS, world.model, 'PC:girl', self.agentlayer, self)
        self.game.instance_to_agent[self.girl.agent.getFifeId()] = self.girl
        self.girl.start()
        self.agent_list.append(self.girl)

        self.wizard = Wizard(TDS, world.model, 'PC:wizard', self.agentlayer, self)
        self.game.instance_to_agent[self.wizard.agent.getFifeId()] = self.wizard
        self.wizard.start()
        self.agent_list.append(self.wizard)

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

        self.warrior = Warrior(TDS, world.model, 'PC:warrior', self.agentlayer)
        self.game.instance_to_agent[self.warrior.agent.getFifeId()] = self.warrior
        self.warrior.start()
        self.agent_list.append(self.warrior)

        self.chemist = Chemist(TDS, world.model, 'NPC:chemist', self.agentlayer)
        self.game.instance_to_agent[self.chemist.agent.getFifeId()] = self.chemist
        self.chemist.start()
        self.agent_list.append(self.chemist)

        self.playableAgent = [self.boy, self.girl]
        self.active_agent = self.boy

    def beesAtHome(self):
        for bee in self.bees:
            if int(bee.agentName[-2:]) <= 3 and bee.mode == code.agents.bee._MODE_WILD:
                return False
        return True

    def beesDead(self):
        for bee in self.bees:
            if int(bee.agentName[-2:]) >= 4 and bee.mode != code.agents.bee._MODE_DEAD:
                return False
        return True

    def reset(self):
        self.boy, self.girl, self.warrior = None, None, None

    def getActiveAgent(self):
        return self.active_agent

    def getActiveInstance(self):
        return self.active_agent.agent
        if self.player == 0:
            return self.agentlayer.getInstance('PC:boy')
        elif self.player == 1:
            return self.agentlayer.getInstance('PC:girl')
        elif self.player == 2:
            return self.agentlayer.getInstance('PC:warrior')
        elif self.player == 3:
            return self.agentlayer.getInstance('PC:wizard')
        return None

    def getActiveAgentLocation(self):
        return self.active_agent.agent.getLocation()

    def talk(self, instance):
        self.getActiveAgent().talk(instance.getLocationRef())

    def kick(self, location):
        self.boy.kick(location)

    def run(self, location):
        self.active_agent.run(location)

    def getHero(self):
        return self.active_agent

    def getGirl(self):
        return self.girl

    def event(self, ev):
        if ev == 'attack':
            self.game.event('hit')

    def toggleAgent(self, world, face_button):
        self.player = (self.player + 1) % len(self.playableAgent)

        face_button.up_image = self.player_faces[self.player]
        face_button.down_image = self.player_faces[self.player]
        face_button.hover_image = self.player_faces[self.player]

        for i in range(len(self.playableAgent)):
            self.playableAgent[i].idle()
            if i == self.player:
                self.playableAgent[i].isActive = True
                world.cameras['main'].attach(self.playableAgent[i].agent)
                world.cameras['small'].attach(self.girl.agent)
                self.active_agent = self.playableAgent[i]
            else:
                self.playableAgent[i].isActive = False
                self.playableAgent[i].follow_hero()

    def getAgentFromId(self, fifeId):
        for ag in self.agent_list:
            if ag.agent.getFifeId() == fifeId:
                return ag
        return None

    def addNewPlayableAgent(self, name):
        for a in self.playableAgent:
            if a.agentName == name:
                return
        for a in self.agent_list:
            if a.agentName == name:
                self.playableAgent.append(a)


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
