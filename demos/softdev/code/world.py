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
import math, random
from fife.extensions import pychan
from fife.extensions.pychan import widgets
from fife.extensions.pychan.internal import get_manager

from code.common.eventlistenerbase import EventListenerBase
from fife.extensions.savers import saveMapFile
from fife.extensions.soundmanager import SoundManager
from agents.boy import Boy
from agents.girl import Girl
from agents.beekeeper import Beekeeper
from agents.agent_manager import create_anonymous_agents
from agents.agent_manager import AgentManager
import code.game
from fife.extensions.fife_settings import Setting
from threading import Timer

TDS = Setting(app_name="rio_de_hola")

class World(EventListenerBase):
    """
    The world!

    This class handles:
      setup of map view (cameras ...)
      loading the map
      GUI for right clicks
      handles mouse/key events which aren't handled by the GUI.
       ( by inheriting from EventlistenerBase )

    That's obviously too much, and should get factored out.
    """
    def __init__(self, engine):
        super(World, self).__init__(engine, regMouse=True, regKeys=True)
        self.engine = engine
        self.eventmanager = engine.getEventManager()
        self.model = engine.getModel()
        self.filename = ''
        self.pump_ctr = 0 # for testing purposis
        self.ctrldown = False
        self.instance_to_agent = {}
        self.dynamic_widgets = {}

        self.light_intensity = 1
        self.light_sources = 0

        self.soundmanager = SoundManager(self.engine)
        self.music = None


        self.game = code.game.Game.getGame()

    def getAgentManager(self):
        return self.game.agentManager

    def reset(self):
        """
        Clear the agent information and reset the moving secondary camera state.
        """
        if self.music:
            self.music.stop()
            
        self.map, self.agentlayer = None, None
        self.cameras = {}
        #self.agentManager.reset()
        self.clouds, self.beekeepers = [], []
        self.cur_cam2_x, self.initial_cam2_x, self.cam2_scrolling_right = 0, 0, True
        self.target_rotation = 0
        self.instance_to_agent = {}

    def load(self, filename):
        """
        Load a xml map and setup agents and cameras.
        """
        self.filename = filename
        self.reset()
        loader = fife.MapLoader(self.engine.getModel(), 
                                self.engine.getVFS(), 
                                self.engine.getImageManager(), 
                                self.engine.getRenderBackend())
                                
        if loader.isLoadable(filename):
            self.map = loader.load(filename)

        

        self.getAgentManager().initAgents(self)
        self.initCameras()

        #Set background color
        self.engine.getRenderBackend().setBackgroundColor(80,80,255)

        Timer(0.1, self.loadTrees).start()

    def loadTrees(self):
        layer = self.map.getLayer('TechdemoMapGroundObjectLayer')
        for i in range(0, 226):
            tree = layer.getInstance("tree:{}".format(i))
            l = tree.getLocation()
            c = l.getMapCoordinates()
            if i <= 26:
                c.x = -2+(i/2.0)
                c.y = 3
            elif i <= 40:
                c.x = -2
                c.y = -4+((i-27)/2.0)
            elif i <= 65:
                c.x = -1.5+((i-41)/2.0)
                c.y = -4
            elif i <= 79:
                c.x = 11
                c.y = -4+((i-66)/2.0)
            elif i <= 98:
                c.x = 0+((i-80)/2.0)
                c.y = 1.5
            elif i <= 117:
                c.x = 0+((i-99)/2.0)
                c.y = -2.5
            elif i <= 159:
                c.x = 7+(((i-118)%5)/2.0)
                c.y = -2+((i-118)/6)/2.0
            elif i <= 195:
                c.x = 0+(((i-160)%5)/2.0)
                c.y = -2+((i-160)/5)/2.0

            l.setMapCoordinates(c)
            tree.setLocation(l)
        
    def initCameras(self):
        """
        Before we can actually see something on screen we have to specify the render setup.
        This is done through Camera objects which offer a viewport on the map.

        For this techdemo two cameras are used. One follows the hero(!) via 'attach'
        the other one scrolls around a bit (see the pump function).
        """
        camera_prefix = self.filename.rpartition('.')[0] # Remove file extension
        camera_prefix = camera_prefix.rpartition('/')[2] # Remove path
        camera_prefix += '_'
        
        for cam in self.map.getCameras():
            camera_id = cam.getId().replace(camera_prefix, '')
            self.cameras[camera_id] = cam
            cam.resetRenderers()
            
        self.cameras['main'].attach(self.getAgentManager().getActiveInstance())

        # Floating text renderers currntly only support one font.
        # ... so we set that up.
        # You'll se that for our demo we use a image font, so we have to specify the font glyphs
        # for that one.
        renderer = fife.FloatingTextRenderer.getInstance(self.cameras['main'])
        textfont = get_manager().createFont('fonts/rpgfont.png', 0, str(TDS.get("FIFE", "FontGlyphs")));
        renderer.setFont(textfont)
        renderer.activateAllLayers(self.map)
        renderer.setBackground(100, 255, 100, 165)
        renderer.setBorder(50, 255, 50)
        renderer.setEnabled(True)
        
        # Activate the grid renderer on all layers
        renderer = self.cameras['main'].getRenderer('GridRenderer')
        renderer.activateAllLayers(self.map)
        
        # The small camera shouldn't be cluttered by the 'humm di dums' of our hero.
        # So we disable the renderer simply by setting its font to None.
        renderer = fife.FloatingTextRenderer.getInstance(self.cameras['small'])
        renderer.setFont(None)

        # The following renderers are used for debugging.
        # Note that by default ( that is after calling View.resetRenderers or Camera.resetRenderers )
        # renderers will be handed all layers. That's handled here.
        renderer = fife.CoordinateRenderer.getInstance(self.cameras['main'])
        renderer.setFont(textfont)
        renderer.clearActiveLayers()
        renderer.addActiveLayer(self.map.getLayer(str(TDS.get("rio", "CoordinateLayerName"))))

        renderer = self.cameras['main'].getRenderer('QuadTreeRenderer')
        renderer.setEnabled(True)
        renderer.clearActiveLayers()
        if str(TDS.get("rio", "QuadTreeLayerName")):
            renderer.addActiveLayer(self.map.getLayer(str(TDS.get("rio", "QuadTreeLayerName"))))

        # Fog of War stuff
        renderer = fife.CellRenderer.getInstance(self.cameras['main'])
        renderer.setEnabled(True)
        renderer.clearActiveLayers()
        renderer.addActiveLayer(self.map.getLayer('TechdemoMapGroundObjectLayer'))
        concimg = self.engine.getImageManager().load("misc/black_cell.png")
        maskimg = self.engine.getImageManager().load("misc/mask_cell.png")
        renderer.setConcealImage(concimg)
        renderer.setMaskImage(maskimg)
        renderer.setFogOfWarLayer(self.map.getLayer('TechdemoMapGroundObjectLayer'))
        
        #disable FoW by default.  Users can turn it on with the 'f' key.
        renderer.setEnabledFogOfWar(False)
        
        # Set up the second camera
        # NOTE: We need to explicitly call setLocation, there's a bit of a messup in the Camera code.
        self.cameras['small'].setLocation(self.getAgentManager().getActiveAgentLocation())
        self.cameras['small'].attach(self.getAgentManager().getActiveAgent().agent)
        self.cameras['small'].setOverlayColor(100,0,0,100)
        self.cameras['small'].setEnabled(False)

        self.target_rotation = self.cameras['main'].getRotation()


    def save(self, filename):
        saveMapFile(filename, self.engine, self.map)

    def getInstancesAt(self, clickpoint):
        """
        Query the main camera for instances on our active(agent) layer.
        """
        return self.cameras['main'].getMatchingInstances(clickpoint, self.agentlayer)

    def getLocationAt(self, clickpoint):
        """
        Query the main camera for the Map location (on the agent layer)
        that a screen point refers to.
        """
        target_mapcoord = self.cameras['main'].toMapCoordinates(clickpoint, False)
        target_mapcoord.z = 0
        location = fife.Location(self.agentlayer)
        location.setMapCoordinates(target_mapcoord)
        return location

    def keyPressed(self, evt):
        keyval = evt.getKey().getValue()
        keystr = evt.getKey().getAsString().lower()
        if keystr == 't':
            r = self.cameras['main'].getRenderer('GridRenderer')
            r.setEnabled(not r.isEnabled())
        elif keystr == 'c':
            r = self.cameras['main'].getRenderer('CoordinateRenderer')
            r.setEnabled(not r.isEnabled())
        elif keystr == 's':
            c = self.cameras['small']
            c.setEnabled(not c.isEnabled())
        elif keystr == 'f':
            self.game.onFacePress()
        elif keystr == 'r':
            self.model.deleteMaps()
            self.load(self.filename)
        elif keystr == 'f':
            renderer = fife.CellRenderer.getInstance(self.cameras['main'])
            renderer.setEnabledFogOfWar(not renderer.isEnabledFogOfWar())
            self.cameras['main'].refresh()
        elif keystr == 'o':
            self.target_rotation = (self.target_rotation + 90) % 360
        elif keystr == '2':
            self.lightIntensity(0.1)
        elif keystr == '1':
            self.lightIntensity(-0.1)
        elif keystr == '5':
            self.lightSourceIntensity(25)
        elif keystr == '4':
            self.lightSourceIntensity(-25)
        elif keystr == '0' or keystr == fife.Key.NUM_0:
            if self.ctrldown:
                self.cameras['main'].setZoom(1.0)
        elif keyval in (fife.Key.LEFT_CONTROL, fife.Key.RIGHT_CONTROL):
            self.ctrldown = True

    def keyReleased(self, evt):
        keyval = evt.getKey().getValue()
        if keyval in (fife.Key.LEFT_CONTROL, fife.Key.RIGHT_CONTROL):
            self.ctrldown = False

    def mouseWheelMovedUp(self, evt):
        if self.ctrldown:
            self.cameras['main'].setZoom(self.cameras['main'].getZoom() * 1.05)

    def mouseWheelMovedDown(self, evt):
        if self.ctrldown:
            self.cameras['main'].setZoom(self.cameras['main'].getZoom() / 1.05)

    def changeRotation(self):
        """
        Smoothly change the main cameras rotation until
        the current target rotation is reached.
        """
        currot = self.cameras['main'].getRotation()
        if self.target_rotation != currot:
            self.cameras['main'].setRotation((currot + 5) % 360)

    """ This function is called when the user click one of the mouse's buttons.
        Send the event immediately to agent_manager instead of use it here???
    """
    def mousePressed(self, evt):
        if evt.isConsumedByWidgets():
            return

        clickpoint = fife.ScreenPoint(evt.getX(), evt.getY())
        if (evt.getButton() == fife.MouseEvent.LEFT):
            self.game.leftClick(self.getLocationAt(clickpoint))

        if (evt.getButton() == fife.MouseEvent.RIGHT):
            instances = self.getInstancesAt(clickpoint)
            self.game.rightClick(instances, clickpoint)
                

    def mouseMoved(self, evt):
        renderer = fife.InstanceRenderer.getInstance(self.cameras['main'])
        renderer.removeAllOutlines()

        pt = fife.ScreenPoint(evt.getX(), evt.getY())
        instances = self.getInstancesAt(pt);
        for i in instances:
            if i.getObject().getId() in ('girl', 'beekeeper'):
                renderer.addOutlined(i, 173, 255, 47, 2)

    def lightIntensity(self, value):
        if self.light_intensity+value <= 1 and self.light_intensity+value >= 0:
            self.light_intensity = self.light_intensity + value

            if self.lightmodel == 1:
                self.cameras['main'].setLightingColor(self.light_intensity, self.light_intensity, self.light_intensity)

    def lightSourceIntensity(self, value):
        if self.light_sources+value <= 255 and self.light_sources+value >= 0:
            self.light_sources = self.light_sources+value
            renderer = fife.LightRenderer.getInstance(self.cameras['main'])

            renderer.removeAll("beekeeper_simple_light")
            renderer.removeAll("hero_simple_light")
            renderer.removeAll("girl_simple_light")

            if self.lightmodel == 1:
                node = fife.RendererNode(self.getAgentManager().getHero())
                renderer.addSimpleLight("hero_simple_light", node, self.light_sources, 64, 32, 1, 1, 255, 255, 255)

                node = fife.RendererNode(self.getAgentManager().getGirl())
                renderer.addSimpleLight("girl_simple_light", node, self.light_sources, 64, 32, 1, 1, 255, 255, 255)

                for beekeeper in self.beekeepers:
                    node = fife.RendererNode(beekeeper.agent)
                    renderer.addSimpleLight("beekeeper_simple_light", node, self.light_sources, 120, 32, 1, 1, 255, 255, 255)       

    def onConsoleCommand(self, command):
        result = ''
        try:
            result = str(eval(command))
        except Exception, e:
            result = str(e)
        return result

    def pump(self):
        """
        Called every frame.
        """

        self.changeRotation()
        self.pump_ctr += 1
