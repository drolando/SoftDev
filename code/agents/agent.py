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

from fife import fife
from code.common.common import ProgrammingError

_STATE_NONE, _STATE_IDLE, _STATE_RUN, _STATE_KICK, _STATE_TALK = xrange(5)

class Agent(fife.InstanceActionListener):
	
	def __init__(self, settings, model, agentName, layer, uniqInMap=True):
		fife.InstanceActionListener.__init__(self)
		self.settings = settings
		self.model = model
		self.agentName = agentName
		self.layer = layer
		if uniqInMap:
			self.agent = layer.getInstance(agentName)
			self.agent.addActionListener(self)
		self.AGENT_SPEED = 2.5 * float(self.settings.get("rio", "TestAgentSpeed"))

	def onInstanceActionFinished(self, instance, action):
		raise ProgrammingError('No OnActionFinished defined for Agent')

	def onInstanceActionCancelled(self, instance, action):
		raise ProgrammingError('No OnActionFinished defined for Agent')
	
	def onInstanceActionFrame(self, instance, action, frame):
		raise ProgrammingError('No OnActionFrame defined for Agent')	

	def start(self):
		self.idle()

	def idle(self):
		self.state = _STATE_IDLE
		self.agent.actOnce('stand')

	def run(self, location):
		self.state = _STATE_RUN
		self.agent.move('run', location, self.GIRL_SPEED)

	def onKick(self):
		self.agent.say('Hey!', 1000)
