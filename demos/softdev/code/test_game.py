import unittest
import game
import sys, random, uuid
sys.path.insert(0,'..')

from test_main import Engine

class GameTests(unittest.TestCase):
    def setUp(self):
        self.game = game.Game(Engine())
        self.game.dialog = DummyDialog()
        self.game.agentManager = DummyAgentManager()

    def testEvents(self):
        self.game._state = None
        self.game.event(game.EV_START)
        self.failUnless(self.game._state == game.STATE_START)
        old_lives = self.game._lives
        self.game.event(game.EV_HIT)
        self.failUnless(self.game._lives == old_lives - 1)
        self.game._lives = 1
        self.game.event(game.EV_HIT)
        self.failUnless(self.game._state == game.STATE_START)
        self.game.event(game.EV_QUEST_2)
        self.failUnless(self.game._state == game.STATE_PAUSE)
        self.game.event(game.EV_QUEST_3)
        self.failUnless(self.game._state == game.STATE_PAUSE)
        self.game.event(game.EV_SHRINE)
        self.failUnless(self.game._state == game.STATE_END)
        self.failUnless(self.game._secState == game.STATE_END)
        self.game.event(game.EV_BEE_DEAD)
        self.failUnless(self.game._secState == game.STATE_BEE3)
        self.game.event(game.EV_BEE_ARRIVED)
        self.failUnless(self.game._secState == game.STATE_BEE1)
        res = self.game.event("testFoo")
        self.failUnless(res == False)

    def testClicks(self):
        self.game._state = game.STATE_PLAY
        self.game.agentManager.getActiveAgent().has_run = False
        self.game.dialog.hide_instancemenu_called = False
        self.game.leftClick(1)
        self.failUnless(self.game.agentManager.getActiveAgent().has_run == True)
        self.failUnless(self.game.dialog.hide_instancemenu_called == True)

        self.game.dialog.show_instancemenu_called = False
        self.game.rightClick([self.game.agentManager.girl], 1)
        self.failUnless(self.game.dialog.show_instancemenu_called == True)

    
    def setGame(self, game):
        pass

class DummyDialog():
    def __init__(self):
        self.show_called = False
        self.show_instancemenu_called = False
        self.hide_instancemenu_called = False
    def show(self, *args):
        self.show_called = True
    def show_instancemenu(self, clickpoint, instance, buttons):
        self.show_instancemenu_called = True
    def hide_instancemenu(self):
        self.hide_instancemenu_called = True

class DummyAgentManager():
    def __init__(self):
        self.activeAgent = DummyAgent()
        self.hero = DummyAgent()
        self.girl = DummyAgent()
    def beesAtHome(self):
        return True
    def beesDead(self):
        return True
    def getActiveAgent(self):
        return self.activeAgent
    def getActiveInstance(self):
        return self.activeAgent

class DummyAgent():
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.has_run = False
        self.location = Location()
    def run(self, location):
        self.has_run = True
    def getObject(self):
        return self
    def getId(self):
        return self.id
    def getFifeId(self):
        return self.id
    def getLocation(self):
        return self.location
    def getLocationRef(self):
        return self.location

class Location():
    def getLayerDistanceTo(self, location):
        return 1

def main():
    unittest.main()
