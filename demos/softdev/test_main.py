#!/usr/bin/env python

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
# This is the rio de hola client for FIFE.

import sys, os, re, math, random, shutil
import unittest

fife_path = os.path.join('..','..','engine','python')
if os.path.isdir(fife_path) and fife_path not in sys.path:
    sys.path.insert(0,fife_path)

from fife import fife
print "Using the FIFE python module found here: ", os.path.dirname(fife.__file__)

from fife.extensions import *
from code.common import eventlistenerbase
import code.game
import code.test_game
from fife.extensions import pychan
from fife.extensions.pychan.pychanbasicapplication import PychanApplicationBase
from fife.extensions.pychan.fife_pychansettings import FifePychanSettings
from fife.extensions.pychan import widgets
from fife.extensions.pychan.internal import get_manager
from fife.extensions.fife_settings import Setting
from fife.extensions.fife_utils import getUserDataDirectory

settings_path = os.path.expanduser(os.path.join('~', '.fife', 'rio_de_hola'))
print settings_path
if os.path.isdir(settings_path):
    os.remove(os.path.join(settings_path, 'settings.xml'))

TDS = FifePychanSettings(app_name="rio_de_hola")

class Engine():
    def __init__(self):
        self.eventManager = EventManager()
        self.soundManager = SoundManager()
        self.soundClipManager = SoundClipManager()
        self.model = Model()
    def getEventManager(self):
        return self.eventManager
    def getModel(self):
        return self.model
    def getSoundClipManager(self):
        return self.soundClipManager
    def getSoundManager(self):
        return self.soundManager

class Model():
    def __init__(self):
        self.debug = True

class SoundManager():
    def __init__(self):
        self.debug = True
    def init(self):
        pass
    def setListenerOrientation(self, *args):
        pass

class SoundClipManager():
    def __init__(self):
        self.debug = True

class EventManager():
    def __init__(self):
        self.debug = True
    def addKeyListener(self, val):
        pass
    def addMouseListener(self, val):
        pass

class MyTests(unittest.TestCase):
    def setUp(self):
        engine = Engine()
        self.game = code.game.Game(engine)

    def testGameCreated(self):
        self.failUnless(self.game != None)
    
    def testWorldExist(self):
        self.failUnless(self.game.world != None)

    def testDialogExist(self):
        self.failUnless(self.game.dialog != None)

    def testAgentManagerCreated(self):
        self.failUnless(self.game.agentManager != None)

    '''def testEventStart(self):
        tests = unittest.TestLoader().loadTestsFromModule(code.test_game)
        unittest.TextTestRunner(verbosity=5).run(tests)
    '''
def main():
    print dir(unittest.runner)
    unittest.main()

if __name__ == '__main__':
    #main()
    #print dir(unittest.TestLoader())
    testsuite = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=5).run(testsuite)
