## Configuration
In the "conf" folder, you will find some examples of configuration of the Player, Agents and renderers. The syntax of this kind of files must be compliant with the python's ConfigParser module. See https://documentation.help/Python-2.5/module-ConfigParser.html about the official documentation.

### Player
The player is defined with the "player.ini" file.

Sections are:
* `ASSET`:
   - `name`: the name of the agent.
   - `source`: path to the asset.
   - `sprite_directions`: a list of 4 directions definition, with for each one, a list of the top-left point of the sprite.
   - `velocity`: the translation speed of the sprite on the renderer.
   - `animation_velocity`: the speed of the animation when the player moves (how fast the animation goes).

* `DIMENSION`: dimension of the sprite
   - `width`, `height`: width, height of the image to be displayed on the renderer.
   - `sort_position`: When the screen is displayed, a sort is done on objects to put on the current renderer. This value will be added to the top position of the player to adjust the sort order.
   - `pos_x`, `pos_x`: position on the first renderer, when the game starts. This feature have to be moved.

* `SHADOW`: how to compute the collision detection with the sprite.
   - `shadow_type`: `RECT` or `SPRITE`. If `SPRITE`, the shadow image will be used and the pink pixel will be detected. If `RECT`, the shadow have to be defined just after.
   - `shadow_left`, `shadow_top`, `shadow_width`, `shadow_height`: dimensions of the rectangle of the shadow, relatively to the top-left position of the player.

### Agent
Each agent have one unique definition, for every instance that will be added in the renderers.

Sections are:
* `ASSET`:
   - `name`: the name of the agent.
   - `source`: path to the asset.
   - `sprites`: a list of all sprites to animate the agent (set only 1 definition if no animation is needed).
   - `animation_velocity`: the speed of the animation.

* `DIMENSION`: dimension of the sprite.
   - `width`, `height`: width, height of the image to be displayed on the renderer.
   - `sort_position`: When the screen is displayed, a sort is done on objects to put on the current renderer. This value will be added to the top position of the player to adjust the sort order.
   - `pos_x`, `pos_x`: position on the first renderer, when the game starts.

* `SHADOW`: how to compute the collision detection with the sprite.
   - `shadow_type`: `RECT` or `SPRITE`. If `SPRITE`, the shadow image will be used and the pink pixel will be detected. If `RECT`, the shadow have to be defined just after.
   - `shadow_left`, `shadow_top`, `shadow_width`, `shadow_height`: dimensions of the rectangle of the shadow, relatively to the top-left position of the player.

* `COLLISION`: how will be the behavior of the player when he meets this agent.
   - `open_renderer`: set a directive to move the player in another renderer. This is usefull when you define a building and you want that the player goes into it, and open the interior of that building.

To display a tree, one definition of the agent "Tree-Agent" have to be done, with one "ini" file. Then, in renderers, just add some defintions to add some trees, using the `sprites` configueration on the "ini" file of the renderer.

### Renderer
The renderer is made to be displayed on the full screen, with all agent in the renderer. The player can move to another renderer.

Sections are:
* `ASSET`:
   - `source`: path to the asset (dimension is always the same).
   - `sprites`: list of agents to be placed in the renderer. You can set many times the same definition of agent to set many instance of agents.

* `COLLISION`: how will be the behavior of the player when he meets a specific rolor of the shadow layer.
   - `open_renderer`: set a directive to move the player in another renderer. This is usefull when you define another renderer and you want that the player goes into it when he reaches the border of the screen.

