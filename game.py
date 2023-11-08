import arcade
import arcade.gui as gui
import json

import code_input
import npc

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 563
SCREEN_TITLE = "Game"
LAYER_NAME_NPC = "Npc"
GRAVITY = 1.5

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1


class Game(arcade.Window):
    """ Main application class. """

    def __init__(self, connection):
        """ Initializer for the game"""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Our textboxes
        self.textbox = None
        self.show_textbox = False

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

        # Open save and level files

        with open('save.json', 'r') as read_save_file:
            self.save = json.loads(read_save_file.read())

        with open('assets/levels.json', 'r') as read_levels_file:
            self.levels = json.loads(read_levels_file.read())

        # TODO add save & close somewhere ; save unsuppported as of today

        # Level data, loaded later on
        self.level_data = None

        # load collisions with npc
        self.player_collision_list = None

    def setup(self):
        """ Set up the game here. Call this function to restart the game."""

        # Set up the Cameras
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Load player save and levels data

        self.level_data = self.levels[self.save["current_level"]]
        map_path = self.level_data["tilemap_path"]

        # Initialize map

        layer_options = {  # options specific to each layer
            "Platforms": {
                "use_spatial_hash": True,
            },
            "Background": {
                "use_spatial_hash": True,
            },
        }
        self.tile_map = arcade.load_tilemap(map_path, self.level_data["scaling"], layer_options)
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
        self.player_sprite.scale = self.level_data["player_scaling"]
        self.player_sprite.center_x = self.level_data["spawn_x"]
        self.player_sprite.center_y = self.level_data["spawn_y"]

        # Initialize NPC sprite TODO   v---- choose which level in string below
        if self.level_data["name"] == "":
            image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
            self.npc_sprite = arcade.Sprite(image_source)
            self.npc_sprite.center_x = 740
            self.npc_sprite.center_y = 315
            self.scene.add_sprite("Npc", self.npc_sprite)

        self.scene.add_sprite("Player", self.player_sprite)
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

        # Draw score TODO

        # Draw the NPC textbox

        if self.show_textbox:
            self.textbox = npc.TextBox(400, 500, 700, 100,
                                       "Mais, vous savez, moi je ne crois pas qu’il y ait de bonne ou de mauvaise "
                                       "situation ^^ \nMoi, si je devais résumer ma vie aujourd’hui avec vous, "
                                       "\nje dirais que c’est d’abord des rencontres, des gens qui m’ont tendu la "
                                       "main")
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
            self.player_sprite.center_x = self.level_data["spawn_x"]
            self.player_sprite.center_y = self.level_data["spawn_y"]

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
                self.player_sprite.change_y = self.level_data["player_jump_speed"] # todo fix this

        # Process left/right
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -self.level_data["player_movement_speed"]
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = self.level_data["player_movement_speed"]
        else:
            self.player_sprite.change_x = 0

        if self.enter_pressed:
            if self.show_textbox:
                self.show_textbox = False
            elif npc.dist_between_sprites(self.player_sprite, self.npc_sprite) < 100:
                self.show_textbox = True
