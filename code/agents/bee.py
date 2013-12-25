from agent import Agent
from fife import fife
from fife.extensions.fife_settings import Setting
import random

#TDS = Setting(app_name="rio_de_hola")

_STATE_NONE, _STATE_IDLE, _STATE_RUN, _STATE_FOLLOW, _STATE_RAND = 0, 1, 2, 3, 4

class Bee(Agent):
    def __init__(self, settings, model, agentName, layer, uniqInMap=True):
        super(Bee, self).__init__(settings, model, agentName, layer, uniqInMap)
        self.state = _STATE_RAND
        self.waypoints = ((-15, -9), (-18, -10))
        self.waypoint_counter = 0
        self.hero = self.layer.getInstance('PC')
        self.following = False
        
        self.BEE_SPEED_NORMAL = 1.5 * float(self.settings.get("rio", "TestAgentSpeed"))
        self.BEE_SPEED_FAST = 3 * float(self.settings.get("rio", "TestAgentSpeed"))

    def onInstanceActionFinished(self, instance=None, action=None):
        if (self.state in (_STATE_RUN, _STATE_FOLLOW)):
            self.idle()
        elif self.state == _STATE_RAND:
            self.rand(self.getNextWaypoint())
        else:
            if (self.waypoint_counter % 3 and self.following):
                self.waypoint_counter += 1
                self.follow_hero()
            
    def start(self):
        self.onInstanceActionFinished()

    def onInstanceActionCancelled(self, instance, action):
        print "onInstanceActionCancelled"
        pass
    
    def getNextWaypoint(self):
        self.waypoint_counter += 1
        l = fife.Location(self.layer)
        loc = (random.randint(-25, -5), random.randint(-22, 0))
        l.setLayerCoordinates(fife.ModelCoordinate(*loc))
        return l

    def follow_hero(self):
        self.state = _STATE_FOLLOW
        self.agent.follow('fly', self.hero, self.BEE_SPEED_FAST)

    def run(self, location):
        self.state = _STATE_RUN
        self.agent.move('fly', location, self.BEE_SPEED_FAST)

    def rand(self, location):
        self.state = _STATE_RAND
        self.agent.move('fly', location, self.BEE_SPEED_NORMAL)
