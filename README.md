# PSP-SimpleGame
This is a quite simple game on PSP, using Staskless python + PSP2D.

Contact: julien.coron@gmail.com

I would like to try on a some small hardware the game creation. I've started with the fantasy-console Pyxel ("Pyxel is a retro game engine for Python" - https://github.com/kitao/pyxel), but the result was too limited.

## About the content of this repo
In this reposory, you will find:
* The binary file "EBOOT.PBP" (just copied from the strackless python port for PSP) - Find it here: https://code.google.com/archive/p/pspstacklesspython/downloads ;
* The startup script "script.py" ;
* A set of files in the folder "engine". This is the game-engine I've created to provide a kind of framework, to build a RPG game (a zelda-like game) ;
* The "asset" folder contains pictures for the game - See the chapter dedicated to this part, for collision detection ;
* The "conf" filder is the description of the game: how trhe engine have to work with assets to provide a kind of game.

## Objects of the game
### Goals of each object
There is 3 main classes in the engine, to build the game:
- Agent: Any object in the game (a sprite)
- Player: The player of the game (user's avatar)
- Renderer: The playground where the player and agents are placed

The main script of the game have to instantiate the first renderer and put the player into.

### Agent
Link to [Class Agent](https://github.com/jchome/PSP-SimpleGame/blob/main/engine/agent.py)

An agent is an object in the playground (like phyisical object). In will interact with the player in many ways:
 - a simple wall or something that cannot be overlap by the player
 - an ennemy that hurts the player
 - a bonus (coins, gems, etc)
 - a gate to a new renderer

To detect the collision, the sprite has more data that the simple bounding box around the sprite. It have a "shadow". This can be a rectagle, or a set of pixels with a specific color (pink).

Bush agent:
![Bush with shadow](assets/trees/tree-01.png "Example of bush")

As you see, a rectangle would not be precise enought to set the borders.

This image is composed of 2 parts:
1. The sprite that will be displayed
2. The shadow of the sprite, to use for collision detection

See configuration file of an agent to set this feature.


### Player
Link to [Class Player](https://github.com/jchome/PSP-SimpleGame/blob/main/engine/player.py)

The Player is an Agent, that is controlled by the user (the player of the game).
The control is ensured by the cross buttons, for 4 directions. You will find a commented code about the joystick, but on my old PSP, it does not works well.

Until now, this spcific agent has a specific configuration, but this can be merged with any "moving" agent. The difference should be "the player is controlled by the user". 
We can imagin an "automatic" game, that have no player, a list of agents, interacting together... We are just here (as user) to look at them and their interactions, like a king of god.

So, the collision detection for this agent is managed by a heavy method in this class.

### Renderer
This section have to be filled...
I have to explain the Player, the Agent, the Renderer.

## Assets (pitures)
This section have to be filled...
About "shadow", for collision detection.

