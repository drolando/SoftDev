import unittest
import game
import sys, random, uuid
from mock import MagicMock
from mock import patch
sys.path.insert(0,'..')


class GameTests(unittest.TestCase):
    def setUp(self):
        self.game = game.Game(MagicMock())
        self.game.dialog = MagicMock()
        self.game.agentManager = MagicMock()
        self.game.statusBar = MagicMock()
        self.game.world = MagicMock()

    def testEvents(self):
        self.game._state = None
        self.game.event(game.EV_START)
        assert self.game._state == game.STATE_PLAY
        self.game._state = game.STATE_START
        self.game.event(game.EV_START)
        assert self.game.dialog.show.called
        #ToDO EV_HIT
        self.game.event(game.EV_BEE_ARRIVED)
        assert self.game._secState == game.STATE_BEE1
        self.game.event(game.EV_QUEST_2)
        assert self.game._state == game.STATE_PAUSE
        assert self.game.dialog.show.called
        self.game.event(game.EV_BEE_DEAD)
        assert self.game._secState == game.STATE_BEE3
        self.game.event(game.EV_QUEST_3)
        assert self.game._state == game.STATE_PAUSE
        assert self.game.dialog.show.called
        self.game.event(game.EV_SHRINE)
        assert self.game._state == game.STATE_END
        assert self.game._secState == game.STATE_END
        assert self.game.dialog.show.called

    def testSaveLoad(self):
        self.game._old_state = 1
        self.game._secState = 2
        self.game._quest = 3
        c = MagicMock()
        l = MagicMock()
        c.x = 1
        c.y = 2
        l.getMapCoordinates = MagicMock(return_value=c)
        a = MagicMock()
        a.agent = MagicMock()
        a.agent.getLocation = MagicMock(return_value=l)
        a.health = 100
        a.magic = 100
        a._mode = 0
        a.agentName = "a:1"
        b = MagicMock()
        b.agent.getLocation = MagicMock(return_value=l)
        b.health = 100
        b.magic = 100
        b._mode = 0
        b.agentName = "b:1"
        self.game.agentManager.playableAgent = [a, b]
        self.game.saveStatus()
        assert a.agent.getLocation.called
        assert b.agent.getLocation.called
        self.game._state = 0
        self.game._secState = 0
        self.game.quest = 0
        self.game.loadStatus()
        assert self.game._state == 1
        assert self.game._secState == 2
        assert self.game._quest == 3
        assert self.game.agentManager.addNewPlayableAgent.call_count == 2

    def testSetState(self):
        self.game._state = game.STATE_START
        self.game.setState(game.STATE_PLAY)
        assert self.game._state == game.STATE_PLAY
        assert self.game.statusBar.hide.called
        self.game.setState(game.STATE_PAUSE)
        assert self.game._state == game.STATE_PAUSE
        assert self.game.statusBar.show.called

        
    def testClicks(self):
        self.game._state = game.STATE_PLAY
        self.game.leftClick(1)
        assert self.game.agentManager.getActiveAgent.called
        assert self.game.dialog.hide_instancemenu.called
        assert self.game.agentManager.getActiveAgent().run.called

        self.game.rightClick([self.game.agentManager.girl], 1)
        assert self.game.dialog.show_instancemenu.called

    def onMoveButtonTest(self):
        self.game._state = game.STATE_PLAY
        self.game.onMoveButtonPress()
        assert self.game.dialog.hide_instancemenu.called
        assert self.game.agentManager.getActiveAgent().run.called

    def onTalkButtonTest(self):
        pass

    
    def setGame(self, game):
        pass

def main():
    unittest.main()
