```
__/\\\\\\\\\\\\\\\___/\\\\\\\\\\\___/\\\\\\\\\\\\\\\___/\\\\\\\\\\\\\\\_
_\/\\\///////////___\/////\\\///___\/\\\///////////___\/\\\///////////__
_\/\\\__________________\/\\\______\/\\\______________\/\\\_____________
_\/\\\\\\\\\\\__________\/\\\______\/\\\\\\\\\\\______\/\\\\\\\\\\\_____
_\/\\\///////___________\/\\\______\/\\\///////_______\/\\\///////______
_\/\\\__________________\/\\\______\/\\\______________\/\\\_____________
_\/\\\__________________\/\\\______\/\\\______________\/\\\_____________
_\/\\\_______________/\\\\\\\\\\\__\/\\\______________\/\\\\\\\\\\\\\\\_
_\///_______________\///////////___\///_______________\///////////////__
```
SOFTDEV GAME v2.0 - [![Build Status](https://travis-ci.org/fifengine/fifengine.png?branch=master)](https://bitbucket.org/drolando/softdev)
------------

INSTALL
------------
sudo apt-get install build-essential git cmake\\
sudo apt-get install libsdl1.2-dev libsdl-ttf2.0-dev libsdl-image1.2-dev\\
sudo apt-get install libboost-all-dev libboost-python-dev\\
sudo apt-get install libvorbis-dev libogg-dev libopenal-dev\\
sudo apt-get install libgl1-mesa-dev\\
sudo apt-get install swig\\
sudo apt-get install zlib1g-dev\\
sudo apt-get install scons\\
sudo apt-get install liballegro4.2-dev\\

Install fifechan:
git clone https://github.com/fifengine/fifechan.git
cd fifechan
git checkout e934293ed8a2f181156965c075560d05ef6414d6 .
cmake .
make
sudo make install

Install fife:
from inside fifengine dir (sdproject):
scons

cd /usr/lib
sudo ln -s /usr/local/lib/libfifechan.so.0.1.0 libfifechan.so.0.1.0
sudo ln -s /usr/local/lib/libfifechan_sdl.so.0.1.0 libfifechan_sdl.so.0.1.0
sudo ln -s /usr/local/lib/libfifechan_opengl.so.0.1.0 libfifechan_opengl.so.0.1.0

GAME
------------

v2.0 - 2014/01/28
------------

QUEST 1:
    - Speak with the warrior
    - Find him a new sword
        - speak with the beekeper
        - bring back his bees
            - kick the bees to get them follow you
            - run near the beekeper
            - you only need to bring back the 3 bees near the lake
        - speak again with the beekeper
        - take the sword from inside the crate
QUEST 2:
    - Free the wizard
        - use the warrior to kill the bees
        - speak with the wizard
    - Get a spell from the chemist
        - speak to the chemist controlling the wizard
QUEST 3:
    - Reach the shrine in the center of the map
        - Use the wizard's spell to burn the trees
        - When you arrive near the shrine activate it

You must do those stuff in the right sequence and with the right character (eg. speaking with the chemist
with the boy won't get you the spell and you can't kick the bees before talking with the warrior and the 
beekeper)

