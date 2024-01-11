import arcade

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

# How fast to run the animation
UPDATES_PER_FRAME = 5


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class Entity(arcade.Sprite):
    """ Basic structure of every sprite """

    def __init__(self, frog):
        # Set up classe parent
        super().__init__()

        # Set default values
        self.frog = frog
        # Default to facing right
        self.facing_direction = RIGHT_FACING

        # Used for image sequences
        self.cur_texture = 0

        if self.frog:
            image = "assets/backgrounds/frog.png"
            self.texture = arcade.load_texture(image)
            self.set_hit_box(self.texture.hit_box_points)

        else :
            main_path = f"assets/characters"
            self.idle_texture_pair = load_texture_pair(f"{main_path}/Personnage.png")

            # Load textures for walking
            self.walk_textures = []
            for i in range(8):
                texture = load_texture_pair(f"{main_path}/walk/char_walk_{i}.png")
                self.walk_textures.append(texture)

            # Set the initial texture
            self.texture = self.idle_texture_pair[0]
            # Hit box will be set based on the first image used
            self.set_hit_box(self.texture.hit_box_points)


class PlayerCharacter(Entity):
    """ Player Sprite """

    def __init__(self, frog):
        self.frog = frog

        super().__init__(frog)

        # Track state
        self.walking_right = False
        self.walking_left = False
        self.jumping = False
        self.current_pos = (0, 0)
        self.last_pos = (0, 0)

    def update_animation(self, delta_time: float = 1 / 60):

        if not self.frog :
            # Figure out if we need to flip face left or right
            if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
                self.facing_direction = LEFT_FACING
            elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
                self.facing_direction = RIGHT_FACING

            # Walking animation
            self.cur_texture += 1
            if self.cur_texture > 7 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME
            self.texture = self.walk_textures[frame][self.facing_direction]

            # Idle animation
            if self.change_x == 0:
                self.texture = self.idle_texture_pair[self.facing_direction]
                return

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
        liste_ligne = self.text.splitlines()
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, arcade.color.WHITE)

        # Draw the border
        arcade.draw_rectangle_outline(self.x, self.y, self.width, self.height, arcade.color.BLACK)

        # Draw the text
        i = 0
        for ligne in liste_ligne:
            arcade.draw_text(ligne, self.x - self.width / 2 + 10, self.y + self.height / 2 - 10 - i, arcade.color.BLACK,
                             12, width=int(self.width / 1 - 20), align="left", anchor_x="left", anchor_y="top")
            i += 20
