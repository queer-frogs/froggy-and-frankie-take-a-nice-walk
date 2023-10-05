import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Game"

# Player starting position
PLAYER_START_X = 100
PLAYER_START_Y = 240

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 7
GRAVITY = 1.5
PLAYER_JUMP_SPEED = 30

# Tiled constants
TILE_SCALING = 1

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

        main_path = f"sprites/{name_folder}/{name_file}"

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


class Game(arcade.Window):
    """ Main application class. """

    def __init__(self):
        """ Initializer for the game"""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.AMAZON)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        # self.jump_needs_reset = False

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Create sprite lists here, and set them to None
        self.player_sprite = None
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

        # Level
        self.level = 1

        # Load sounds

    def setup(self):
        """ Set up the game here. Call this function to restart the game."""

        # Set up the Cameras
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Initialize map
        map_path = "assets/tiled/tilemaps/sample.tmx"
        layer_options = {  # options specific to each layer
            "Platforms": {
                "use_spatial_hash": True,
            },
        }
        self.tile_map = arcade.load_tilemap(map_path, TILE_SCALING, layer_options)
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Initialize Scene
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # ⚠️to redefine with the correct value
        self.end_of_map = 1000

        # Initialize Player Sprite
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y

        self.scene.add_sprite("Player", self.player_sprite)
        self.scene.add_sprite_list("Walls", True, self.walls_list)

        # Initialize sprites and sprite lists here

        # Keep track of the score, make sure we keep the score if the player finishes a level
        if self.reset_score:
            self.score = 0
        self.reset_score = True

        # Create the physics engine
        # self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.walls_list)

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

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Indicate level number
        nb_level = f"Level: {self.level}"
        arcade.draw_text(nb_level, 10, 600, arcade.csscolor.WHITE, 18)

        # Draw score

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
            self.level += 1

            # Make sure to keep the score from this level when setting up the next level
            self.reset_score = False

            # Load the next level
            self.setup()

    def on_key_press(self, key, modifiers):
        """ Called whenever a key is pressed."""

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

        # Process up/down

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


def main():
    """ Main method """
    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
