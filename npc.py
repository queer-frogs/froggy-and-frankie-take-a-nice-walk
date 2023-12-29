import math
import game
import entities
import arcade


class Npc(entities.Entity):
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
        liste_ligne = self.text.splitlines()
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, arcade.color.WHITE)

        # Draw the border
        arcade.draw_rectangle_outline(self.x, self.y, self.width, self.height, arcade.color.BLACK)

        # Draw the text
        i = 0
        for ligne in liste_ligne:
            arcade.draw_text(ligne, self.x - self.width / 2 + 10, self.y + self.height / 2 - 10 - i, arcade.color.BLACK,
                             12,
                             width=int(self.width - 20), align="left", anchor_x="left", anchor_y="top")
            i += 20


def dist_between_sprites(sprite1, sprite2):
    """
    A function to calculate the distance between two sprites
    Args:
        sprite1
        sprite2

    Returns: float, distance between the sprites
    """
    return math.sqrt((sprite1.center_x - sprite2.center_x) ** 2 + (sprite1.center_y - sprite2.center_y) ** 2)
