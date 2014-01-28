from agent import Agent
from fife import fife
from fife.extensions.fife_settings import Setting
import code.game

#TDS = Setting(app_name="rio_de_hola")

_STATE_CLOSE, _STATE_OPENING, _STATE_OPEN = xrange(3)

class Cage(Agent):
    def __init__(self, settings, model, agentName, layer, uniqInMap=True):
        super(Cage, self).__init__(settings, model, agentName, layer, uniqInMap)
        self.state = _STATE_CLOSE
        self.game = code.game.Game.getGame()

    def onInstanceActionFinished(self, instance, action):
        if self.state == _STATE_OPENING:
            self.game.event(code.game.EV_QUEST_2)
            self.stand()
        elif self.state == _STATE_OPEN:
            self.stand()

    def stand(self):
        self.state = _STATE_OPEN
        self.agent.actOnce('stand')

    def open(self):
        self.state = _STATE_OPENING
        self.agent.actOnce('open')

    def start(self):
        pass

    def onInstanceActionCancelled(self, instance, action):
        pass
