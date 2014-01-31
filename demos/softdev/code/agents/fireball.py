from agent import Agent
from fife import fife
from fife.extensions.fife_settings import Setting
import code.game

_STATE_NONE, _STATE_IDLE, _STATE_RUN, _STATE_FOLLOW, _STATE_EXPLODE = xrange(5)

class Fireball(Agent):
    def __init__(self, settings, model, agentName, layer, uniqInMap=True):
        super(Fireball, self).__init__(settings, model, agentName, layer, uniqInMap)
        self.state = _STATE_NONE
        self.waypoints = ((67, 80), (75, 44))
        self.waypoint_counter = 0
        self.hero = self.layer.getInstance('PC')
        self.layer = layer
        
        self.SPEED = 5 * float(self.settings.get("rio", "TestAgentSpeed"))

    def onInstanceActionFinished(self, instance, action):
        if self.state == _STATE_RUN:
            self.explode()
        elif self.state == _STATE_EXPLODE:
            self.layer.deleteInstance(self.target)
            self.layer.setWalkable(True)
            self.idle()
        else:
            self.idle()

    def onInstanceActionCancelled(self, instance, action):
        pass

    def getNextWaypoint(self):
        self.waypoint_counter += 1
        l = fife.Location(self.layer)
        l.setLayerCoordinates(fife.ModelCoordinate(*self.waypoints[self.waypoint_counter % len(self.waypoints)]))
        return l

    def follow_hero(self):
        self.state = _STATE_FOLLOW
        self.agent.follow('fly', self.hero, self.SPEED)

    def run(self, location):
        self.state = _STATE_RUN
        self.agent.move('fly', location, self.SPEED)

    def start(self):
        self.state = _STATE_IDLE
        self.agent.actOnce('stand')

    def explode(self):
        self.state = _STATE_EXPLODE
        l = self.target.getLocation()
        c = l.getMapCoordinates()
        c.z = 0.3
        l.setMapCoordinates(c)
        self.agent.setLocation(l)
        self.agent.actOnce('explosion')

    def setTarget(self, target):
        self.target = target

    def idle(self):
        self.state = _STATE_IDLE
        self.agent.actOnce('stand')
        self.agent.setLocation(self.getNextWaypoint())
