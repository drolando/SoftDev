from fife import fife
import math, random
from code.common.common import ProgrammingError
from boy import Boy
from girl import Girl
from wizard import Wizard
from beekeeper import Beekeeper
from chemist import Chemist
from cage import Cage
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

    """
        Intializes all the agents. All these instances are also added to the self.agent_list list
        to simplify the searches by name or id.
    """
    def initAgents(self, world):
        self.agentlayer = world.map.getLayer('TechdemoMapGroundObjectLayer')
        world.agentlayer = self.agentlayer
        self.boy = Boy(TDS, world, 'PC:boy', self.agentlayer)
        self.game.instance_to_agent[self.boy.agent.getFifeId()] = self.boy
        self.boy.start()
        self.agent_list.append(self.boy)

        self.girl = Girl(TDS, world, 'PC:girl', self.agentlayer, self)
        self.game.instance_to_agent[self.girl.agent.getFifeId()] = self.girl
        self.girl.start()
        self.agent_list.append(self.girl)

        self.wizard = Wizard(TDS, world, 'PC:wizard', self.agentlayer, self)
        self.game.instance_to_agent[self.wizard.agent.getFifeId()] = self.wizard
        self.wizard.start()
        self.agent_list.append(self.wizard)

        self.beekeepers = create_anonymous_agents(TDS, world, 'beekeeper', self.agentlayer, Beekeeper)
        for beekeeper in self.beekeepers:
            self.game.instance_to_agent[beekeeper.agent.getFifeId()] = beekeeper
            beekeeper.start()
            self.agent_list.append(beekeeper)

        self.cage = Cage(TDS, world, 'sword_crate', self.agentlayer)
        self.game.instance_to_agent[self.cage.agent.getFifeId()] = self.cage
        self.cage.start()
        self.agent_list.append(self.cage)

        self.bees = []
        for i in range(1, 8):
            bee = code.agents.bee.Bee(TDS, world, 'NPC:bee:0{}'.format(i), self.agentlayer, self)
            self.bees.append(bee)
            self.game.instance_to_agent[bee.agent.getFifeId()] = bee
            bee.start()
            self.agent_list.append(bee)

        self.warrior = Warrior(TDS, world, 'PC:warrior', self.agentlayer)
        self.game.instance_to_agent[self.warrior.agent.getFifeId()] = self.warrior
        self.warrior.start()
        self.agent_list.append(self.warrior)

        self.chemist = Chemist(TDS, world, 'NPC:chemist', self.agentlayer)
        self.game.instance_to_agent[self.chemist.agent.getFifeId()] = self.chemist
        self.chemist.start()
        self.agent_list.append(self.chemist)

        self.playableAgent = [self.boy, self.girl]
        self.active_agent = self.boy

    """
        This method checks if the first 3 bees are near the beeboxes.
    """
    def beesAtHome(self):
        for bee in self.bees:
            if int(bee.agentName[-2:]) <= 3 and bee.mode == code.agents.bee._MODE_WILD:
                return False
        return True

    """
        This method checks if the bees whith id >= 4 are all dead.
    """
    def beesDead(self):
        for bee in self.bees:
            if int(bee.agentName[-2:]) >= 4 and bee.mode != code.agents.bee._MODE_DEAD:
                return False
        return True

    def reset(self):
        self.boy, self.girl, self.warrior = None, None, None

    """
        Returns the current active agent.
    """
    def getActiveAgent(self):
        return self.active_agent

    """
        Returns the FIFE instance of the current active agent.
    """
    def getActiveInstance(self):
        return self.active_agent.agent

    """
        Returns the current active agent's location.
    """
    def getActiveAgentLocation(self):
        return self.active_agent.agent.getLocation()

    def getHero(self):
        return self.active_agent

    def getGirl(self):
        return self.girl

    """
        Changes the current active agent. The list self.playableAgent contains all the
        currently playable characters.
    """
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

    """
        Returns the Agent to the agent with a specific fifeId.
    """
    def getAgentFromId(self, fifeId):
        for ag in self.agent_list:
            if ag.agent.getFifeId() == fifeId:
                return ag
        return None

    """
        Returns the Agent to the agent with a specific name.
    """
    def getAgentByName(self, name):
        for ag in self.agent_list:
            if ag.agentName == name:
                return ag
        return None

    """
        Adds a new playable agent if it's not yet present inside the playableAgent list.
    """
    def addNewPlayableAgent(self, name):
        for a in self.playableAgent:
            if a.agentName == name:
                return
        for a in self.agent_list:
            if a.agentName == name:
                self.playableAgent.append(a)
                if a.agentName != self.active_agent.agentName:
                    a.follow_hero()

    def destroy(self):
        for a in self.agent_list:
            a.destroy()


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
