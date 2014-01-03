from agent import Agent
from fife import fife
from fife.extensions.fife_settings import Setting
from fireball import Fireball

#TDS = Setting(app_name="rio_de_hola")

_STATE_NONE, _STATE_IDLE, _STATE_RUN, _STATE_FOLLOW = 0, 1, 2, 3

class Wizard(Agent):
    def __init__(self, settings, model, agentName, layer, agentManager, uniqInMap=True):
        super(Wizard, self).__init__(settings, model, agentName, layer, uniqInMap)
        self.state = _STATE_NONE
        self.waypoints = ((67, 80), (75, 44))
        self.waypoint_counter = 0
        self.agentManager = agentManager
        self.hero = self.layer.getInstance('PC')
        self.isActive = 0
        self.fireball = Fireball(settings, model, 'NPC:fireball', layer)
        self.fireball.start()
        
        self.SPEED = 3 * float(self.settings.get("rio", "TestAgentSpeed"))

    def onInstanceActionFinished(self, instance, action):
        self.idle()

    def onInstanceActionCancelled(self, instance, action):
        print "onInstanceActionCancelled"
        pass
    
    def getNextWaypoint(self):
        self.waypoint_counter += 1
        l = fife.Location(self.layer)
        l.setLayerCoordinates(fife.ModelCoordinate(*self.waypoints[self.waypoint_counter % len(self.waypoints)]))
        return l

    def follow_hero(self):
        self.state = _STATE_FOLLOW
        self.agent.follow('run', self.agentManager.getActiveInstance(), self.SPEED)

    def run(self, location):
        self.state = _STATE_RUN
        self.agent.move('run', location, self.SPEED)

    def cast_spell(self, instance):
        self.agent.actOnce('cast_spell', instance.getLocationRef())
        self.fireball.setTarget(instance)
        self.fireball.agent.setLocation(self.agent.getLocation())
        self.fireball.run(instance.getLocation())

