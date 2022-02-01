# PSP-SimpleGame
This is a quite simple game on PSP, using Staskless python + PSP2D.

I would like to try on a some small hardware the game creation. I've started with the fantasy-console Pyxel ("Pyxel is a retro game engine for Python" - https://github.com/kitao/pyxel), but the result was too limited.

## About the content of this repo
In this reposory, you will find:
* The binary file "EBOOT.PBP" (just copied from the strackless python port for PSP) ;
* The startup script "script.py" ;
* A set of files in the folder "engine". This is the game-engine I've created to provide a kind of framework, to build a RPG game (a zelda-like game) ;
* The "asset" folder contains pictures for the game - See the chapter dedicated to this part, for collision detection ;
* The "conf" filder is the description of the game: how trhe engine have to work with assets to provide a kind of game.

## Objects of the game
### Goals of each object


### Agent

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

