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

fife_path = os.path.join('..','..','engine','python')
if os.path.isdir(fife_path) and fife_path not in sys.path:
    sys.path.insert(0,fife_path)

from fife import fife
print "Using the FIFE python module found here: ", os.path.dirname(fife.__file__)

from fife.extensions import *
from code.common import eventlistenerbase
import code.game
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

class ApplicationListener(eventlistenerbase.EventListenerBase):
    def __init__(self, engine, game):
        super(ApplicationListener, self).__init__(engine,regKeys=True,regCmd=True, regMouse=False, regConsole=False, regWidget=True)
        self.engine = engine
        self.game = game
        engine.getEventManager().setNonConsumableKeys([
            fife.Key.ESCAPE,])

        self.quit = False
        self.aboutWindow = None

        self.rootpanel = pychan.loadXML('gui/xml/rootpanel.xml')
        self.rootpanel.mapEvents({
            'quitButton' : self.onQuitButtonPress,
            'aboutButton' : self.onAboutButtonPress,
            'optionsButton' : TDS.showSettingsDialog
        })
        self.rootpanel.show()

        self.character_gui = pychan.loadXML('gui/xml/player.xml')
        self.character_gui.mapEvents({
            'face' : self.onFacePressed
        })
        self.character_gui.show()

        self.game.setApplicationListener(self)
        self.game.event(code.game.EV_QUEST_2)
        

    def keyPressed(self, evt):
        print ">>>>>> run.py --> keyPressed ", evt.getKey().getValue()
        keyval = evt.getKey().getValue()
        keystr = evt.getKey().getAsString().lower()
        consumed = False
        if keyval == fife.Key.ESCAPE:
            self.quit = True
            evt.consume()
        elif keystr == 'p':
            self.engine.getRenderBackend().captureScreen('screenshot.png')
            evt.consume()

    def onCommand(self, command):
        print ">>>>>> run.py --> onCommand"
        if command.getCommandType() == fife.CMD_QUIT_GAME:
            self.quit = True
            command.consume()

    def onQuitButtonPress(self):
        cmd = fife.Command()
        cmd.setSource(None)
        cmd.setCommandType(fife.CMD_QUIT_GAME)
        self.engine.getEventManager().dispatchCommand(cmd)

    def onAboutButtonPress(self):
        if not self.aboutWindow:
            self.aboutWindow = pychan.loadXML('gui/xml/help.xml')
            self.aboutWindow.mapEvents({ 'closeButton' : self.aboutWindow.hide })
            self.aboutWindow.distributeData({ 'helpText' : open("misc/infotext.txt").read() })
        self.aboutWindow.show()

    def onFacePressed(self):
        face_button = self.character_gui.findChild(name="face")
        self.game.onFacePressed(face_button)


class IslandDemo(PychanApplicationBase):
    def __init__(self):
        super(IslandDemo,self).__init__(TDS)
        self.game = code.game.Game(self.engine)
        self.listener = ApplicationListener(self.engine, self.game)
        self.game.load(str(TDS.get("rio", "MapFile")))

    def createListener(self):
        pass # already created in constructor

    def _pump(self):
        if self.listener.quit:
            self.breakRequested = True
            
            # get the correct directory to save the map file to
            mapSaveDir = getUserDataDirectory("fife", "rio_de_hola") + "/maps"
            
            # create the directory structure if it does not exist
            if not os.path.isdir(mapSaveDir):
                os.makedirs(mapSaveDir)
            
            # save map file to directory
            self.game.save(mapSaveDir + "/savefile.xml")
        else:
            self.game.pump()

def main():
    app = IslandDemo()
    app.run()

if __name__ == '__main__':
    main()
