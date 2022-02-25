
## Objects of the game
### Goals of each object
There is 3 main classes in the engine, to build the game:
- Agent: Any object in the game (a sprite)
- Player: The player of the game (user's avatar)
- Renderer: The playground where the player and agents are placed

The main script of the game have to instantiate the first renderer and put the player into.

To ease the user interface, another object is used : Widget. This kind of object is rendered at the top of the game. The usual widget is the player's life, or the player inventory.

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
![Bush with shadow](../assets/trees/tree-01.png "Example of bush")

As you see, a rectangle would not be precise enought to set the borders.

This image is composed of 2 parts:
1. The sprite that will be displayed
2. The shadow of the sprite, to use for collision detection

See configuration file of an agent to set this feature.


### Player
Link to [Class Player](https://github.com/jchome/PSP-SimpleGame/blob/main/engine/player.py)

The Player is an Agent, that is controlled by the user (the player of the game).
The control is ensured by the cross buttons, for 4 directions. You will find a commented code about the joystick, but on my old PSP, it does not works well.

Until now, this specific agent has a specific configuration, but this can be merged with any other agent. The difference should be "the player is controlled by the user". 
We can imagine an "automatic" game, that have no player, but only a list of agents, interacting together... We are just here (as user) to look at them and their interactions, like a king of god.

So, the collision detection for this agent is managed by a heavy method in this class.

### Renderer
The renderer is the playground for agents, displayed to the user. It is the container, where each instance of agent have a position. Only one renderer is displayed (where the player is) and take the whole screen.

Each renderer where the user goes is loaded if it's not already done, and is stored in memory, keeping position of all agents. Like that, when the player goes from one renderer to another, agents have the same position than before. Agents are not updated in non-displayed renderers.

### Widget
The widget is not a part of the renderer, but is global to the game. That's why each one is instantiated in the Game class.

* The "Controller widget" is used to ask the user how the player have to interact with an agent.

<p align="center" alt="The controller widget" title="The controller widget">
  <img src="https://raw.githubusercontent.com/jchome/PSP-SimpleGame/main/assets/controls.png">
</p>

* The "Debug widget" will help the developper to add a text during the execution of the game. Il will display a debug text at top left of the screen.


### Game
This section have to be filled...
Talk about the renderers, all widgets, the player.
