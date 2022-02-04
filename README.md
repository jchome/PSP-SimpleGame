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

Please note that for the moment, any agent is static. It does not move in the renderer.

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
The renderer is the playground for agents. It is the container, where each instance of agent have a position. Only one renderer is displayed (where the player is) and take the whole screen.

Each renderer where the user goes is loaded if it's not already done, and is stored in memory, keeping position of all agents. Like that, when the player goes from one renderer to another, agents have the same position than before. Agents are not updated in non-displayed renderers.


## Assets (pitures)
This section have to be filled...
About "shadow", for collision detection.

## Configuration
In the conf folder, you will find some examples of configuration of le Player, Agents and renderers. The syntax of this kind of files must be compliant with the python's ConfigParser module. See https://documentation.help/Python-2.5/module-ConfigParser.html about the official documentation.

### Player
The player is defined with the "player.ini" file.

Sections are:
* ASSET:
 - name: the name of the agent.
 - source: path to the asset.
 - sprite_directions: a list of 4 directions definition, with, for each one, a list of the top-left point of the sprite.
 - velocity: the translation speed of the sprite on the renderer.
 - animation_velocity: the speed of the animation when the player moves.

* DIMENSION: dimension of the sprite
 - width, height: width, height of the image to be displayed on the renderer.
 - sort_position: When the screen is displayed, a sort is done on objects to put on the current renderer. This value will be added to the top position of the player to adjust the sort order.
 - pos_x, pos_x: position on the first renderer, when the game starts.

* SHADOW: how to compute the collision detection with the sprite.
 - shadow_type: RECT or SPRITE. If "SPRITE", the shadow image will be used and the pink pixel will be detected. If "RECT", the shadow have to be defined just after.
 - shadow_left, shadow_top, shadow_width, shadow_height: dimensions of the rectangle of the shadow, relatively to the top-left position of the player.

### Agent
Each agent have one unique definition, for every instance that will be added in the renderers.

Sections are:
* ASSET:
 - name: the name of the agent.
 - source: path to the asset.
 - sprites: a list of all sprites to animate the agent (set only 1 definition if no animation is needed).
 - animation_velocity: the speed of the animation.

* DIMENSION: dimension of the sprite.
 - width, height: width, height of the image to be displayed on the renderer.
 - sort_position: When the screen is displayed, a sort is done on objects to put on the current renderer. This value will be added to the top position of the player to adjust the sort order.
 - pos_x, pos_x: position on the first renderer, when the game starts.

* SHADOW: how to compute the collision detection with the sprite.
 - shadow_type: RECT or SPRITE. If "SPRITE", the shadow image will be used and the pink pixel will be detected. If "RECT", the shadow have to be defined just after.
 - shadow_left, shadow_top, shadow_width, shadow_height: dimensions of the rectangle of the shadow, relatively to the top-left position of the player.

* COLLISION: how will be the behavior of the player when he meets this agent.
 - open_renderer: set a directive to move the player in another renderer. This is usefull when you define a building and you want that the player goes into it, and open the interior of that building.


### Renderer
The renderer is made to be displayed on the full screen, but the player can go into another renderer.

Sections are:
* ASSET:
 - source: path to the asset (dimension is always the same).
 - sprites: list of agents to be placed in the renderer. You can set many times the same definition of agent to set many instance of agents.

* COLLISION: how will be the behavior of the player when he meets a specific rolor of the shadow layer.
 - open_renderer: set a directive to move the player in another renderer. This is usefull when you define another renderer and you want that the player goes into it when he reaches the border of the screen.
