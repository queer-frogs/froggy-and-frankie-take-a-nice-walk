import arcade


class Entity(arcade.Sprite):
    """ Basic structure of every sprite """

    def __init__(self, image_source):
        # Set up classe parent
        super().__init__(image_source)

        # Set default values
        # Load different textures for different states of action
        # with main_path + _ + action + nb

        # Set initial texture
        # Set hit boxes


class PlayerCharacter(Entity):
    """ Player Sprite """

    def __init__(self, image_source):
        super().__init__(image_source)

        # Track state
        self.walking_right = False
        self.walking_left = False
        self.jumping = False
        self.current_pos = (0, 0)
        self.last_pos = (0, 0)

    def update_animation(self, delta_time: float = 1 / 60):
        # Update sprite based on state
        pass


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
