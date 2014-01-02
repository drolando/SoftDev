from agent import Agent
from fife import fife
from fife.extensions.fife_settings import Setting
import random
import code.game

#TDS = Setting(app_name="rio_de_hola")

_STATE_NONE, _STATE_IDLE, _STATE_RUN, _STATE_FOLLOW, _STATE_RAND, _STATE_ATTACK = xrange(6)
_MODE_WILD, _MODE_BOX = xrange(2)

class Bee(Agent):
    def __init__(self, settings, model, agentName, layer, agentManager, uniqInMap=True):
        super(Bee, self).__init__(settings, model, agentName, layer, uniqInMap)
        self.state = _STATE_RAND
        self.agentManager = agentManager
        self.waypoint_counter = 0
        self.hero = self.layer.getInstance('PC')
        self.min_x = int(self.getX() - 8)
        self.max_x = int(self.getX() + 8)
        self.min_y = int(self.getY() - 8)
        self.max_y = int(self.getY() + 8)
        self.mode = _MODE_WILD
        
        self.BEE_SPEED_NORMAL = 1.5 * float(self.settings.get("rio", "TestAgentSpeed"))
        self.BEE_SPEED_FAST = 3 * float(self.settings.get("rio", "TestAgentSpeed"))

    def onInstanceActionFinished(self, instance=None, action=None):
        if self.state == _STATE_RAND:
            self.rand(self.getNextWaypoint())
        elif self.state == _STATE_FOLLOW:
            if self.nearBeeBoxes() == True:
                self.rand(self.getNextWaypoint())
                self.game.event(code.game.EV_BEE_ARRIVED)
            else:
                self.attack()
        elif self.state == _STATE_ATTACK:
            self.rand(self.getNextWaypoint())
            
    def start(self):
        self.onInstanceActionFinished()

    def onInstanceActionCancelled(self, instance, action):
        print "onInstanceActionCancelled: ", action.getId()
    
    def getNextWaypoint(self):
        self.waypoint_counter += 1
        l = fife.Location(self.layer)
        loc = (random.randint(self.min_x, self.max_x), random.randint(self.min_y, self.max_y))
        l.setLayerCoordinates(fife.ModelCoordinate(*loc))
        return l

    def follow_hero(self):
        self.state = _STATE_FOLLOW
        self.agent.follow('fly', self.agentManager.getActiveInstance(), self.BEE_SPEED_FAST)

    def run(self, location):
        self.state = _STATE_RUN
        self.agent.move('fly', location, self.BEE_SPEED_FAST)

    def rand(self, location):
        self.state = _STATE_RAND
        self.agent.move('fly', location, self.BEE_SPEED_NORMAL)

    def onKick(self):
        if self.mode == _MODE_WILD:
            self.follow_hero()

    def attack(self):
        self.state = _STATE_ATTACK
        self.agent.actOnce('attack', self.agentManager.getActiveInstance().getLocationRef())
        self.agentManager.event('attack')

    def nearBeeBoxes(self):
        print "nearBeeBoxes ", self.getX(), " ", self.getY()
        if self.getX() >= -48 and self.getX() <= -32 and self.getY() >= -40 and self.getY() <= -26:
            self.min_x = -48
            self.max_x = -32
            self.min_y = -40
            self.max_y = -26
            self.mode = _MODE_BOX
            return True
        return False

    #x -32 -48
    #y -26 -40