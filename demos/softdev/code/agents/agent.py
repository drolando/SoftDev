from fife import fife
from fife.fife import IAnimationLoader
from code.common.common import ProgrammingError
import code.game
from fife.extensions.soundmanager import SoundManager

_STATE_NONE, _STATE_IDLE, _STATE_RUN, _STATE_KICK, _STATE_TALK = xrange(5)
_MODE_NONE = 0

class Agent(fife.InstanceActionListener):
    
    def __init__(self, settings, world, agentName, layer, uniqInMap=True):
        fife.InstanceActionListener.__init__(self)
        self.settings = settings
        self.model = world.model
        self.agentName = agentName
        self.layer = layer
        self.isActive = False
        self._mode = _MODE_NONE
        if uniqInMap:
            self.agent = layer.getInstance(agentName)
            self.agent.addActionListener(self)
            self.position = self.agent.getLocation()
        self.SPEED = 2.5 * float(self.settings.get("rio", "TestAgentSpeed"))
        self.game = code.game.Game.getGame()
        self.health = 100
        self.magic = 0
        

    def onInstanceActionFinished(self, instance, action):
        self.game.event(code.game.Game.ACTION_FINISHED, "agent", action.getId())

    def onInstanceActionCancelled(self, instance, action):
        pass

    def onInstanceActionFrame(self, instance, action, frame):
        pass

    def start(self):
        self.idle()

    def idle(self):
        self.state = _STATE_IDLE
        self.agent.actOnce('stand')

    def run(self, location):
        self.state = _STATE_RUN
        self.agent.move('run', location, self.SPEED)

    def onKick(self):
        self.agent.say('Hey!', 1000)

    def getX(self):
        return self.agent.getLocation().getMapCoordinates().x * 2

    def getY(self):
        return self.agent.getLocation().getMapCoordinates().y * 2

    def say(self, text):
        self.agent.say(text, 2500)

    def talk(self, location):
        pass

    def destroy(self):
        pass

    def reset(self):
        if self.position != None and self.agent != None:
            self.agent.setLocation(self.position)
        self.start()
