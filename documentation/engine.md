
## Objects of the game
### Goals of each object
There is 3 main classes in the engine, to build the game:
- Agent: Any interactive object in the game (= a sprite)
- Player: The player of the game (user's avatar)
- Display: A background image, maybe some text and user interaction object. This is the case for the Welcome screen, the Menu screen, and boards.
  - Board (extension of Display): The playground where the player and agents are placed

The main script of the game have to instantiate the first display.

To ease the user interface, another object is used : Widget. This kind of object is rendered at the top of the game. The usual widget is the player's life, or the player object's inventory.

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

### Display
The display is used to crezate the Welcome screen, the menu, and the playground for agents. It is the container, where each instance of agent have a position. Only one display is rendered in the screen of the console and takes the whole screen.

Like written before, the Display class is extended in the Board class, to play the game, with the player's sprite.

Each Board where the user goes is loaded if it's not already done, and is stored in memory, keeping position of all agents. Like that, when the player goes from one board to another, agents have the same position than before. Agents are not updated in non-displayed boards.

### Widget
The widget is not a part of the Board, but is global to the game. That's why each one is instantiated in the Game class.

Examples of widgets:

* The "Controller widget" is used to ask the user how the player have to interact with an agent.

<p align="center" alt="The controller widget" title="The controller widget">
  <img src="https://raw.githubusercontent.com/jchome/PSP-SimpleGame/main/assets/controls.png">
</p>

* The "Debug widget" will help the developper to add a text during the execution of the game. Il will display a debug text at top left of the screen.


### Game
The game is the global container of all used objects:
 - the player
 - the current Display (Welcone screen, menu or playing board)
 - widgets

At startup, the Welcome display is rendered, and a Thread is started to load other objects (the menu Display, the player, the first play board, the music, etc.)
