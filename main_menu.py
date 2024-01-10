import arcade
import arcade.gui as gui
from utils import write_save

import npc


class MenuView(arcade.View):
    """Main menu view class."""
    def __init__(self, game_view):
        super().__init__()
        self.manager = gui.UIManager()
        self.game_view = game_view

        resume = arcade.load_texture("assets/tiled/tiles/own/Play.png")
        resume_button = gui.UITextureButton(texture=resume, scale=4)

        sortie = arcade.load_texture("assets/tiled/tiles/own/Exit.png")
        exit_button = gui.UITextureButton(texture=sortie, scale=4)

        # Initialise a grid in which widgets can be arranged.
        self.box = gui.UIBoxLayout(x=100, y=100, vertical=True, children=[resume_button, exit_button])
        self.manager.add(gui.UIAnchorWidget(anchor_x='center', anchor_y='center', child=self.box))

        @exit_button.event("on_click")
        def on_click_exit_button(event):
            arcade.exit()
            write_save(self.game_view)

        @resume_button.event("on_click")
        def on_click_resume_button(event):
            # Pass already created view because we are resuming.
            self.window.show_view(self.game_view)


    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

    def on_show_view(self):
        """ This is run once when we switch to this view """
        # Makes the background darker
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.manager.enable()

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()
        self.manager.draw()


class HelpView(arcade.View):
    """Main menu view class."""
    def __init__(self, game_view):
        super().__init__()
        self.manager = gui.UIManager()
        self.game_view = game_view

        retour = arcade.load_texture("assets/tiled/tiles/own/Retour.png")
        retour_button = gui.UITextureButton(texture=retour, scale=2)
        self.box = gui.UIBoxLayout(x=100, y=100, vertical=True, children=[retour_button])

        self.manager.add(gui.UIAnchorWidget(anchor_x='right', anchor_y='bottom', child=self.box))

        self.scene = arcade.Scene()
        image_book = "assets/tiled/tiles/own/Book2.png"
        self.book = arcade.Sprite(image_book)
        self.book.scale = 2.3
        self.book.center_x = 500
        self.book.center_y = 250
        self.scene.add_sprite("Book", self.book)


        @retour_button.event("on_click")
        def on_click_retour_button(event):
            self.window.show_view(self.game_view)

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

    def on_show_view(self):
        """ This is run once when we switch to this view """
        # Makes the background darker
        arcade.set_background_color(arcade.color.ANTIQUE_WHITE)

        self.manager.enable()

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()
        self.scene.draw()
        self.manager.draw()
        i=0
        # Print the description of the is_empty function in the hint book
        arcade.draw_text("     place_block(x)    ", 550, 300 - i, arcade.color.BLACK, 12,
                         width=int(1000 - 20), align="left", anchor_x="left", anchor_y="top", bold=True, font_name=(
                "Times New Roman",  # Comes with Windows
                "Times",  # MacOS may sometimes have this variant
                "Liberation Serif"  # Common on Linux systems)
            ))
        i += 15
        self.foncts = "place a block at the x columns on the screen " \
                      "\n(the 0 is signified by the special tile). " \
                      "\nYou can stack them" \

        liste_ligne = self.foncts.splitlines()
        for ligne in liste_ligne:
            arcade.draw_text(ligne, 550, 300 - i, arcade.color.BLACK, 10,
                             width=int(1000 - 20), align="left", anchor_x="left", anchor_y="top", font_name=(
                    "Times New Roman",  # Comes with Windows
                    "Times",  # MacOS may sometimes have this variant
                    "Liberation Serif"  # Common on Linux systems)
                ))
            i += 15
        i+=30
        # Print the description of the is_empty function in the hint book
        arcade.draw_text("     is_empty(x,y)    ", 550, 300 - i, arcade.color.BLACK, 12,
                         width=int(1000 - 20), align="left", anchor_x="left", anchor_y="top", bold=True, font_name=(
                "Times New Roman",  # Comes with Windows
                "Times",  # MacOS may sometimes have this variant
                "Liberation Serif"  # Common on Linux systems)
            ))
        i += 15
        self.foncts = "return True if the block at the x,y coordinate " \
                                  "\nin the level are empty," \
                                  "\n return false if it isn’t the case"\

        liste_ligne = self.foncts.splitlines()
        for ligne in liste_ligne:
            arcade.draw_text(ligne, 550, 300 - i, arcade.color.BLACK, 10,
                             width=int(1000 - 20), align="left", anchor_x="left", anchor_y="top", font_name=(
                    "Times New Roman",  # Comes with Windows
                    "Times",  # MacOS may sometimes have this variant
                    "Liberation Serif"  # Common on Linux systems)
                ))
            i += 15

        #Print the text of the python loops in the hint book
        i=0
        arcade.draw_text("Python loops :  \n ", 222, 480 - i, arcade.color.BLACK, 12,
                         width=int(1000 - 20), align="left", anchor_x="left", anchor_y="top", bold=True, font_name=(
                "Times New Roman",  # Comes with Windows
                "Times",  # MacOS may sometimes have this variant
                "Liberation Serif"  # Common on Linux systems)
            ))
        i += 30

        self.foncts =            "For i in range (X):"\
                                  "\n\nThe “for loop” is used in order to repeat X time" \
                                  "\n the instructions. Placed in it (here place block)," \
                                  "\n i goes from 0 to X-1 "\
                                  "\n\n\n\n  For i in range (10):\n     For j in range(i): "\
                                  "\n\n The interlocked loops can be used to automate" \
                                  "\n a large number of actions"\
                                  "\n\n\n\nWhile (condition) : "\
                                  "\n    place_block(0) "\
                                  "\n\nWhile loops check if the condition is true," \
                                  "\n if it’s the case, it execute the instruction "
        liste_ligne = self.foncts.splitlines()
        for ligne in liste_ligne:
            arcade.draw_text(ligne, 200,480-i, arcade.color.BLACK, 11,
                             width=int(1000 - 20), align="left", anchor_x="left", anchor_y="top",font_name=(
                             "Times New Roman",  # Comes with Windows
                             "Times",  # MacOS may sometimes have this variant
                             "Liberation Serif"  # Common on Linux systems)
                ))
            i += 15
        i=0
        arcade.draw_text("HINT OF THE LEVEL", 550, 480 - i, arcade.color.BLACK, 10,
                         width=int(1000 - 20),bold=True , align="left", anchor_x="left", anchor_y="top", font_name=(
                "Times New Roman",  # Comes with Windows
                "Times",  # MacOS may sometimes have this variant
                "Liberation Serif"  # Common on Linux systems)
            ))
        for hint in self.game_view.level_data["hints"]:
            arcade.draw_text(hint, 550, 460 - i, arcade.color.BLACK, 10,
                             width=int(1000 - 20), align="left", anchor_x="left", anchor_y="top", font_name=(
                    "Times New Roman",  # Comes with Windows
                    "Times",  # MacOS may sometimes have this variant
                    "Liberation Serif"  # Common on Linux systems)
                ))
            i += 15
