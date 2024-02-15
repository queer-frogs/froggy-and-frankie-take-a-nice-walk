import arcade
import arcade.gui as gui

import pyglet
import json

import code_input
import npc
import utils
import entities

from main_menu import MenuView, HelpView

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 563
SCREEN_TITLE = "Game"
LAYER_NAME_NPC = "Npc"
GRAVITY = 1.5
TILE_SIZE = 16


# Set up the screen
SCREEN_NUM = 0
SCREENS = pyglet.canvas.Display().get_screens()
SCREEN = SCREENS[SCREEN_NUM]

class MainMenu(arcade.View):
    """Class that manages the 'menu' view."""
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.manager = gui.UIManager()

        play = arcade.load_texture("assets/menu/Play_intro.png")
        play_button = gui.UITextureButton(texture=play, scale=4)
        self.manager.add(gui.UIAnchorWidget(anchor_x='center', anchor_y='center', child=play_button))

        @play_button.event("on_click")
        def on_click_play_button(event):
            """Use a click button to advance to the 'game' view."""
            game_view = Game(self.connection)
            game_view.setup()
            self.window.show_view(game_view)
            self.manager.disable()

        self.background = arcade.load_texture("assets/menu/starting_image.png")
        self.scene = arcade.Scene()
        image_character = "assets/backgrounds/Character.png"
        self.character_menu = arcade.Sprite(image_character)
        self.character_menu.scale = 2.3
        self.character_menu.center_x = 50
        self.character_menu.center_y = 270
        self.scene.add_sprite("character_menu", self.character_menu)
        image_character = "assets/backgrounds/frog.png"
        self.frog = arcade.Sprite(image_character)
        self.frog.scale = 4
        self.frog.center_x = 170
        self.frog.center_y = 180
        self.scene.add_sprite("frog", self.frog)

    def on_show_view(self):
        """Called when switching to this view."""
        arcade.set_background_color(arcade.color.WHITE)
        self.manager.enable()

    def on_draw(self, pixelated=True):
        """Draw the menu"""
        self.clear()

        arcade.draw_texture_rectangle(500, 280, 1000,
                                      563, self.background)
        arcade.draw_text("Froggie and Frankie take a nice walk", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2+220, arcade.color.BLACK, font_size=30,
                         anchor_x='center', italic=True, font_name=(
                "Times New Roman",  # Comes with Windows
                "Times",  # MacOS may sometimes have this variant
                "Liberation Serif"  # Common on Linux systems)
            ))
        self.scene.draw()
        self.manager.draw()


class Game(arcade.View):
    """ Main application class. """

    def __init__(self, connection):
        """ Initializer for the game"""
        super().__init__()

        # Textboxes
        self.textbox = None
        self.show_textbox = False
        self.textbox_npc = False    # NPC corresponding to the level texbox

        # gui manager to create and add gui elements
        self.manager = None

        # Track the current state of what key is pressed
        self.enter_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.p_pressed = False

        self.frog = False

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Create sprite lists here, and set them to None
        self.player_sprite = None
        self.npc_sprite = None

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

        # Connection to kivy interface
        self.connection = connection

        # Screen resolution
        self.screen_resolution = (SCREEN_WIDTH, SCREEN_HEIGHT)

        # Default tile size
        self.tile_size = TILE_SIZE

        # Open save file
        with open('save.json', 'r') as read_save_file:
            self.save = json.loads(read_save_file.read())

        self.levels = {}

        # Level data, loaded later on
        self.level_data = None

        # Load collisions with npc
        self.player_collision_list = None

        # Initialize fall timer, used for fall damage
        self.fall_timer = 0.
        self.show_timer = False  # If true, prints the timer at every update, useful for setting up levels

    def setup(self):
        """ Set up the game here. Call this function to restart the game."""

        # Set up the Cameras
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        # hide textbox
        self.show_textbox = False

        # Reset positions available to precomputed values
        with open("levels.json", "r") as read_levels_file:
            self.levels = json.loads(read_levels_file.read())

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
        else:
            arcade.set_background_color(arcade.color.BEAU_BLUE)

        # Gui elements
        self.manager = gui.UIManager()
        self.manager.enable()

        # Menu
        reset = arcade.load_texture("assets/menu/Reset.png")
        reset_button = gui.UITextureButton(texture=reset, scale=2)
        reset_button.on_click = self.on_click_reset

        help = arcade.load_texture("assets/menu/Help.png")
        help_button = gui.UITextureButton(texture=help, scale=2)
        help_button.on_click = self.on_click_help

        pause = arcade.load_texture("assets/menu/Stop.png")
        switch_menu_button = gui.UITextureButton(texture=pause, scale=2)
        switch_menu_button.on_click = self.on_click_menu

        self.box = gui.UIBoxLayout(x=100, y=100, vertical=True, children=[reset_button, help_button, switch_menu_button])
        self.manager.add(gui.UIAnchorWidget(anchor_x="right", anchor_y="top", child=self.box))

        # Initialize Scene
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # End of map value
        self.end_of_map = 1000

        # Initialize Player Sprite
        self.player_sprite = entities.PlayerCharacter(self.frog)
        self.player_sprite.scale = 1.2 * self.level_data["player_scaling"] * self.level_data["scaling"]
        self.player_sprite.center_x = self.level_data["spawn_x"]
        self.player_sprite.center_y = self.level_data["spawn_y"]

        # Initialize NPCs of the level ; TODO currently only the last npc added to the json has the level textbox
        if self.level_data["npc"]:
            for npc_index in range(len(self.level_data["npc"])):
                npc_data = self.level_data["npc"][npc_index]
                npc_sprite = arcade.Sprite(npc_data["sprite_path"])
                npc_sprite.scale = npc_data["scale"]
                npc_sprite.center_x = npc_data["x"]
                npc_sprite.center_y = npc_data["y"]
                self.scene.add_sprite(f"NPC {npc_index}", npc_sprite)
                self.textbox_npc = npc_sprite

        # Initialize the TextBox of the level ; will be displayed when pressed enter next to an NPC
        if self.level_data["textbox"]:
            textbox_data = self.level_data["textbox"]
            self.textbox = npc.TextBox(textbox_data["x"], textbox_data["y"], textbox_data["w"], textbox_data["h"],
                                       textbox_data["text"])


        # Add player to the scene
        self.scene.add_sprite("Player", self.player_sprite)

        # Blue tile showing the place_block() offset to the player

        if self.level_data["offset"] != -1:
            offset_block = arcade.Sprite("assets/backgrounds/start.png")

            offset_block.width = offset_block.height = TILE_SIZE * self.level_data["scaling"]
            offset_block.left = self.level_data["offset"] * TILE_SIZE * self.level_data["scaling"]
            offset_block.bottom = self.level_data["first_free_slots"][0] * TILE_SIZE * self.level_data["scaling"]
            self.scene.add_sprite("offset", offset_block)

        # Keep track of the score, make sure we keep the score if the player finishes a level
        if self.reset_score:
            self.score = 0
        self.reset_score = True

        # Create the physics engine

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.scene["Platforms"],
                                                             gravity_constant=GRAVITY)

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()


    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        self.clear()

        # Activate the game camera
        self.camera.use()

        # Draw our Scene

        self.scene.draw(pixelated=True)
        self.manager.draw()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Indicate level number
        nb_level = f"Level: {self.levels[self.save['current_level']]['name']}"
        arcade.draw_text(nb_level, 10, 600, arcade.csscolor.WHITE, 18)

        # Draw the NPC textbox

        if self.show_textbox:
            self.textbox.show()

        # Draw hit boxes.
        # self.player_sprite.draw_hit_box(arcade.color.BLUE, 3)


    def on_update(self, delta_time):
        """
        All the logic to move goes here.
        Normally, you'll call update() on the sprite lists that need it.
        """
        # Move the player with the physics engine
        self.physics_engine.update()
        self.player_sprite.current_pos = (self.player_sprite.center_x, self.player_sprite.center_y)

        # Update animations

        # Check if the player is still jumping
        if self.player_sprite.jumping:
            if self.physics_engine.can_jump():
                self.player_sprite.jumping = False
                # Has he fallen for too long ?
                # max_fall_time == -1 means the level has no fall damage
                if self.level_data["max_fall_time"] != -1 and self.fall_timer >= self.level_data['max_fall_time']:
                    self.setup()  # reset the level
                self.fall_timer = 0
            else:
                self.fall_timer += delta_time

        # Update the jumping state
        self.player_sprite.jumping = not self.physics_engine.can_jump()

        # If debug option enabled, show the jump timer in console
        if self.show_timer:
            print(self.fall_timer)

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

        # Trigger auto-jump if needed
        if (
                self.player_sprite.walking_right or self.player_sprite.walking_left) and self.player_sprite.last_pos == self.player_sprite.current_pos:
            self.player_sprite.change_y = self.level_data["player_jump_speed"]


        try:
            if self.connection.poll():
                kivy_message = self.connection.recv()

                # The self parameter allows us to have access to the game object inside the function user_instructions
                res = code_input.user_instructions(self, kivy_message, [])
                if res:
                    self.connection.send(res)
        except EOFError as e:
            print(e)
            # save and quit

        self.player_sprite.last_pos = self.player_sprite.current_pos

        # Update the players animation
        self.scene.update_animation(delta_time)

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
        elif key == arcade.key.P:
            self.p_pressed = True

        self.process_keychange()

    def on_key_release(self, key, key_modifiers):
        """ Called whenever the user lets off a previously pressed key. """

        if key == arcade.key.ENTER:
            self.enter_pressed = False
        # if key == arcade.key.UP or key == arcade.key.W:
        # self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.P:
            self.p_pressed = False

        self.process_keychange()

    def process_keychange(self):
        """ Called when we change a key """

        # Process jump — unused now
        """
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.can_jump(y_distance=10):
                self.player_sprite.change_y = self.level_data["player_jump_speed"]
                """

        # Process left/right
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = (-self.level_data["player_movement_speed"] * self.level_data["scaling"])
            self.player_sprite.walking_right = True
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = (self.level_data["player_movement_speed"] * self.level_data["scaling"])
            self.player_sprite.walking_right = True
        else:
            self.player_sprite.change_x = 0
            self.player_sprite.walking_right = False
            self.player_sprite.walking_left = False

        # TODO
        if self.enter_pressed:
            if self.show_textbox:
                self.show_textbox = False
            elif npc.dist_between_sprites(self.player_sprite, self.textbox_npc) < 100:
                self.show_textbox = True

        if self.p_pressed:
            utils.save_free_slots(self)

    def on_click_reset(self, event):
        self.setup()

    def on_click_help(self,event):
        help_view = HelpView(self)
        self.window.show_view(help_view)

    def on_click_menu(self, event):
        # Passing the main view into menu view as an argument.
        menu_view = MenuView(self)
        self.window.show_view(menu_view)
    def save_and_quit(self):
        utils.write_save(self)
        self.on_close()

