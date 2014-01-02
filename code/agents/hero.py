# -*- coding: utf-8 -*-

# ####################################################################
#  Copyright (C) 2005-2013 by the FIFE team
#  http://www.fifengine.net
#  This file is part of FIFE.
#
#  FIFE is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the
#  Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
# ####################################################################

import random
from agent import Agent
from fife.extensions.fife_settings import Setting
from fife import fife

#TDS = Setting(app_name="rio_de_hola")

_STATE_NONE, _STATE_IDLE, _STATE_RUN, _STATE_KICK, _STATE_TALK, _STATE_FOLLOW = xrange(6)

class Hero(Agent):
    def __init__(self, settings, model, agentName, layer, uniqInMap=True):
        super(Hero, self).__init__(settings, model, agentName, layer, uniqInMap)
        self.state = _STATE_NONE
        self.waypoints = ((67, 80), (75, 44))
        self.waypoint_counter = 0
        self.isActive = True
        self.SPEED = 4 * self.settings.get("rio", "TestAgentSpeed")

    def onInstanceActionFinished(self, instance, action):
        if ((self.state in (_STATE_RUN, _STATE_FOLLOW)) or (self.isActive == True)):
            self.idle()
        else:
            if self.waypoint_counter % 3:
                self.waypoint_counter += 1
                self.follow_hero()
            else:
                self.run(self.getNextWaypoint())

    def getNextWaypoint(self):
        self.waypoint_counter += 1
        l = fife.Location(self.layer)
        l.setLayerCoordinates(fife.ModelCoordinate(*self.waypoints[self.waypoint_counter % len(self.waypoints)]))
        return l

    def onInstanceActionCancelled(self, instance, action):
        pass
    
    def run(self, location):
        print "------- run ", location
        self.state = _STATE_RUN
        self.agent.move('run', location, self.SPEED)

    def kick(self, target):
        self.state = _STATE_KICK
        self.agent.actOnce('kick', target)

    def talk(self, target):
        self.state = _STATE_TALK
        self.agent.actOnce('talk', target)

    def follow_hero(self):
        self.state = _STATE_FOLLOW
        self.agent.follow('run', self.game.agentManager.getActiveInstance(), self.SPEED)
