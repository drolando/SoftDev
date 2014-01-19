from agent import Agent
from fife import fife
from fife.extensions.fife_settings import Setting
from fireball import Fireball
from threading import Timer
from fife.extensions.soundmanager import SoundManager

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
        self.lastFireballUsed = 0
        self.fireballs = []
        for i in range(1, 5):
            fireball = Fireball(settings, model, 'NPC:fireball:0{}'.format(i), layer)
            fireball.start()
            self.fireballs.append(fireball)
        self.health = 65
        self.magic = 100
        self.layer = layer
        
        self.SPEED = 3 * float(self.settings.get("rio", "TestAgentSpeed"))
        self.SPELL_COST = 15

        self.t = Timer(1, self.addMagic)
        self.t.start()

        self.soundmanager = SoundManager(model.engine)

    def onInstanceActionFinished(self, instance, action):
        self.idle()

    def onInstanceActionCancelled(self, instance, action):
        print "onInstanceActionCancelled"
    
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
        if (self.magic >= self.SPELL_COST):
            self.agent.actOnce('cast_spell', instance.getLocationRef())
            self.lastFireballUsed = (self.lastFireballUsed + 1) % len(self.fireballs)
            fireball = self.fireballs[self.lastFireballUsed]
            fireball.agent.refresh()
            fireball.setTarget(instance)
            fireball.agent.setLocation(self.agent.getLocation())
            fireball.run(instance.getLocation())
            self.magic -= self.SPELL_COST
            self.game.setMagic()
            if self.t == None:
                self.addMagic()

            '''self.music = self.soundmanager.createSoundEmitter('/home/daniele/Documents/SoftDev/sdproject/demos/softdev/code/agents/fire.ogg')
            self.music.looping = True
            self.music.gain = 128 # volume: da 0 a 255

            self.music.play()'''


    def addMagic(self):
        if self.magic < 100:
            self.magic += 2
            self.game.setMagic()
            self.t = Timer(1, self.addMagic)
            self.t.start()
        else:
            self.t = None

    def destroy(self):
        if self.t != None:
            self.t.cancel()
        self.magic = 100
        self.t = None
