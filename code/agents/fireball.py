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

from agent import Agent
from fife import fife
from fife.extensions.fife_settings import Setting
import code.game

#TDS = Setting(app_name="rio_de_hola")

_STATE_NONE, _STATE_IDLE, _STATE_RUN, _STATE_FOLLOW, _STATE_EXPLODE = xrange(5)

class Fireball(Agent):
    def __init__(self, settings, model, agentName, layer, uniqInMap=True):
        super(Fireball, self).__init__(settings, model, agentName, layer, uniqInMap)
        self.state = _STATE_NONE
        self.waypoints = ((67, 80), (75, 44))
        self.waypoint_counter = 0
        self.hero = self.layer.getInstance('PC')
        self.isActive = False
        
        self.SPEED = 5 * float(self.settings.get("rio", "TestAgentSpeed"))

    def onInstanceActionFinished(self, instance, action):
        if self.state == _STATE_RUN:
            self.explode()
        elif self.state == _STATE_EXPLODE:
            self.game.event(code.game.EV_EXPLOSION, self.target)
            self.idle()
        else:
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
        self.agent.follow('fly', self.hero, self.SPEED)

    def run(self, location):
        self.state = _STATE_RUN
        self.agent.move('fly', location, self.SPEED)

    def start(self):
        self.state = _STATE_IDLE
        self.agent.actOnce('stand')

    def explode(self):
        self.state = _STATE_EXPLODE
        self.agent.setLocation(self.target.getLocation())
        self.agent.actOnce('explosion')

    def setTarget(self, target):
        self.target = target

    def idle(self):
        self.state = _STATE_IDLE
        self.agent.actOnce('stand')
        self.agent.setLocation(self.getNextWaypoint())
