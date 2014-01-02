from agent import Agent
import code.game

from fife import fife
from fife.extensions.fife_settings import Setting

#TDS = Setting(app_name="rio_de_hola")

_STATE_NONE, _STATE_IDLE, _STATE_RUN, _STATE_FOLLOW = 0, 1, 2, 3

class Warrior(Agent):
    def __init__(self, settings, model, agentName, layer, uniqInMap=True):
        super(Warrior, self).__init__(settings, model, agentName, layer, uniqInMap)
        self.state = _STATE_NONE
        self.waypoints = ((67, 80), (75, 44))
        self.waypoint_counter = 0
        self.isActive = False
        
        self.SPEED = 3 * float(self.settings.get("rio", "TestAgentSpeed"))

    def onInstanceActionFinished(self, instance, action):
        self.game.event(code.game.EV_ACTION_FINISHED, 'warrior', action.getId())
        if self.state == _STATE_FOLLOW:
            self.follow_hero()
        elif self.state == _STATE_IDLE:
            self.idle()
        elif self.state == _STATE_RUN:
            self.idle()

    def onInstanceActionCancelled(self, instance, action):
        print "onInstanceActionCancelled ", action.getId()
        pass
    
    def getNextWaypoint(self):
        self.waypoint_counter += 1
        l = fife.Location(self.layer)
        l.setLayerCoordinates(fife.ModelCoordinate(*self.waypoints[self.waypoint_counter % len(self.waypoints)]))
        return l

    def follow_hero(self):
        self.state = _STATE_FOLLOW
        self.agent.follow('run', self.game.agentManager.getActiveInstance(), self.SPEED)

    def run(self, location):
        self.state = _STATE_RUN
        self.agent.move('run', location, self.SPEED)

