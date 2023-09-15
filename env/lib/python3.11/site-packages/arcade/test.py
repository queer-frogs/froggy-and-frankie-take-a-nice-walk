"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
from pyglet.math import Vec2

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Starting Template"


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE)

        self.polygon = (-200, -200), (200, -200), (200, 200), (-200, 200)
        self.test_points = ((0, 0),
                            (-200, -200),
                            (0, -200),
                            (200, 0),
                            (200, -200),
                            (0, 200),
                            (200, 200),
                            (200, 0),
                            (-200, 200),
                            (-200, 0),

                            (-210, -210),
                            (0, -210),
                            (210, 0),
                            (210, -210),
                            (0, 210),
                            (210, 210),
                            (210, 0),
                            (-210, 210),
                            (-210, 0),

                            (-190, -190),
                            (0, -190),
                            (190, 0),
                            (190, -190),
                            (0, 190),
                            (190, 190),
                            (190, 0),
                            (-190, 190),
                            (-190, 0),

                            )

        self.camera = arcade.Camera(width, height)
        position = Vec2(-self.width / 2,
                        -self.height / 2)
        self.camera.move_to(position)

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()
        self.camera.use()
        arcade.draw_polygon_outline(self.polygon, arcade.color.BLACK, line_width=3)

        def test_point(x, y):
            if arcade.is_point_in_polygon(x, y, self.polygon):
                color = arcade.color.GREEN
            else:
                color = arcade.color.RED
            arcade.draw_circle_filled(x, y, 7, color)

        for point in self.test_points:
            x, y = point
            test_point(x, y)


def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
