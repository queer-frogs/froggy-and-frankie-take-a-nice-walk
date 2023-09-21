import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Game"

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 7
GRAVITY = 1.5
PLAYER_JUMP_SPEED = 30

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
        self.jump_needs_reset = False

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Create sprite lists here, and set them to None
        self.player_sprite = None

        # Our 'physics' engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        # A Camera that can be used to draw GUI elements (menu, score)
        self.gui_camera = None

        self.end_of_map = 0

        # Keep track of the score
        self.score = 0

        # Load sounds

    def setup(self):
        """ Set up the game here. Call this function to restart the game."""

        # Set up the Cameras
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_list = arcade.SpriteList()
        self.player_sprite = arcade.Sprite(image_source)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

        # Initialize map
        # Initialize sprites and sprite lists here
        # Keep track of score

        # Create the physics engine


    def on_draw(self):
        """ Render the screen. """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Clear the screen to the background color
        self.clear()

        # Activate the game camera
        self.camera.use()

        # Draw our Scene

        self.player_list.draw()


        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Draw score

    def on_update(self, delta_time):
        """
        All the logic to move goes here.
        Normally, you'll call update() on the sprite lists that need it.
        """
        # Move the player with the physics engine
        # self.physics_engine.update()

        # Update animations

        # Position the camera
        self.center_camera_to_player()

        pass

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
        # Process left/right

        pass

    def center_camera_to_player(self):
        """ Center camera to the player sprite """
        pass


def main():
    """ Main method """
    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
