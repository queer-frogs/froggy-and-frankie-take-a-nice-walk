import arcade

import math
import arcade.gui as gui
import json

import code_input

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 563
SCREEN_TITLE = "Game"
LAYER_NAME_NPC = "Npc"

# Player starting position
PLAYER_START_X = 10
PLAYER_START_Y = 50

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 15
GRAVITY = 1.5
PLAYER_JUMP_SPEED = 35

# Tiled constants (for level 1:0.45 for level 2: 0.3415
TILE_SCALING = 0.3415 #TODO Function that calculate autaumaticly the scaling (seems exponential)

# Constants used to scale our sprites from their original size

# How many pixels to keep as a minimum margin between the character and the edge of the screen.

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1


class Entity(arcade.Sprite):
    """ Basic structure of every sprite """

    def __init__(self, name_folder, name_file, ):
        # Set up classe parent
        super().__init__()

        # Set default values
        # Load different textures for different states of action
        # with main_path + _ + action + nb

        # Set initial texture
        # Set hit boxes


class PlayerCharacter(Entity):
    """ Player Sprite """

    def __init__(self):
        super().__init__("player", "player")

        # Track state
        self.walking = False
        self.jumping = False

    def update_animation(self, delta_time: float = 1 / 60):
        # Update sprite based on state
        pass

class Npc(Entity):
    def __init__(self):

        # Setup parent class
        super().__init__("npc", "npc")



class TextBox(arcade.Sprite):
    def __init__(self, x, y, width, height, text):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def show(self):
        # Draw the background rectangle
        liste_ligne=self.text.splitlines()
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, arcade.color.WHITE)

        # Draw the border
        arcade.draw_rectangle_outline(self.x, self.y, self.width, self.height, arcade.color.BLACK)

        # Draw the text
        i=0
        for ligne in liste_ligne:
            arcade.draw_text(ligne, self.x - self.width/2 + 10,self.y+self.height/2-10-i, arcade.color.BLACK, 12, width=self.width - 20, align="left", anchor_x="left", anchor_y="top")
            i+=20

# A fonction to calculate the distance between two sprites

def dist_between_sprites(sprite1, sprite2):
    return math.sqrt((sprite1.center_x - sprite2.center_x)**2 + (sprite1.center_y - sprite2.center_y)**2)

class Game(arcade.Window):
    """ Main application class. """

    def __init__(self, connection):
        """ Initializer for the game"""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Our textboxes
        self.textbox = None
        self.show_textbox= False

        # gui manager to create and add gui elements
        self.manager = None

        # Set background color
        arcade.set_background_color(arcade.color.BEAU_BLUE)

        # Track the current state of what key is pressed
        self.enter_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        # arcade_game.jump_needs_reset = False

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Create sprite lists here, and set them to None
        self.player_sprite = None
        self.npc_sprite = None
        self.walls_list = None

        # Our 'physics' engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        # A Camera that can be used to draw GUI elements (menu, score)
        self.gui_camera = None

        # Keep track of the score
        self.score = 0

        # Do we need to reset the score?
        self.reset_score = True

        # Where is the right edge of the map?
        self.end_of_map = 0

        # Load sounds
        self.connection = connection

        with open('save.json', 'r') as read_save_file:
            self.save = json.loads(read_save_file.read())

        with open('assets/levels.json', 'r') as read_levels_file:
            self.levels = json.loads(read_levels_file.read())

        # TODO add close somewhere

        # load collisions with npc
        self.player_collision_list = None

    def setup(self):
        """ Set up the game here. Call this function to restart the game."""

        # Set up the Cameras
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Load player save and levels data

        level_data = self.levels[self.save["current_level"]]
        map_path = level_data["tilemap_path"]

        # Initialize map

        layer_options = {  # options specific to each layer
            "Platforms": {
                "use_spatial_hash": True,
            },
            "Background": {
                "use_spatial_hash": True,
            },
        }
        self.tile_map = arcade.load_tilemap(map_path, level_data["scaling"], layer_options)
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Gui elements
        self.manager = gui.UIManager()
        self.manager.enable()

        # Initialize Scene
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # TODO redefine with the correct value
        self.end_of_map = 1000

        # Initialize Player Sprite
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y

        # Initialize NPC sprite
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.npc_sprite = arcade.Sprite(image_source)
        self.npc_sprite.center_x = 740
        self.npc_sprite.center_y = 315

        self.scene.add_sprite("Player", self.player_sprite)
        self.scene.add_sprite("Npc",self.npc_sprite)
        self.scene.add_sprite_list("Walls", True, self.walls_list)

        # Keep track of the score, make sure we keep the score if the player finishes a level
        if self.reset_score:
            self.score = 0
        self.reset_score = True



        # Create the physics engine

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.scene["Platforms"],
                                                             gravity_constant=GRAVITY)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        self.clear()

        # Activate the game camera
        self.camera.use()

        # Draw our Scene

        self.scene.draw()
        self.manager.draw()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Indicate level number
        nb_level = f"Level: {self.levels[self.save['current_level']]['name']}"
        arcade.draw_text(nb_level, 10, 600, arcade.csscolor.WHITE, 18)

        # Draw score

        #Draw the NPC textbox

        if self.show_textbox:
                self.textbox = TextBox(400, 500, 700, 100, "Mais, vous savez, moi je ne crois pas qu’il y ait de bonne ou de mauvaise situation ^^ \nMoi, si je devais résumer ma vie aujourd’hui avec vous, \nje dirais que c’est d’abord des rencontres, des gens qui m’ont tendu la main")
                self.textbox.show()


    def on_update(self, delta_time):
        """
        All the logic to move goes here.
        Normally, you'll call update() on the sprite lists that need it.
        """
        # Move the player with the physics engine
        self.physics_engine.update()

        # Update animations

        # Did the player fall off the map?
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y


        # See if the user got to the end of the level
        if self.player_sprite.center_x >= self.end_of_map:
            # Advance to the next level

            self.save["current_level"] += 1

            # Make sure to keep the score from this level when setting up the next level
            self.reset_score = False

            # Load the next level
            self.setup()

        # Check if kivy sent something

        if self.connection.poll():
            kivy_message = self.connection.recv()

            # The self parameter allows us to have access to the game object inside the function user_instructions
            res = code_input.user_instructions(self, kivy_message, [])
            if res:
                self.connection.send(res)


    def on_key_press(self, key, modifiers):
        """ Called whenever a key is pressed."""

        if key == arcade.key.ENTER:
            self.enter_pressed = True
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        self.process_keychange()

    def on_key_release(self, key, key_modifiers):
        """ Called whenever the user lets off a previously pressed key. """

        if key == arcade.key.ENTER:
            self.enter_pressed = False
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False


        self.process_keychange()

    def process_keychange(self):
        """ Called when we change a key """

        # Process jump
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.can_jump(y_distance=10):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

        # Process left/right
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

        if self.enter_pressed:
            if self.show_textbox:
                self.show_textbox = False
            elif dist_between_sprites(self.player_sprite, self.npc_sprite) < 100:
                self.show_textbox = True

