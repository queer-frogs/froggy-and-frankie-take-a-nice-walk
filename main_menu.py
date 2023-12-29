import arcade
import arcade.gui as gui

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
    def __init__(self, menu_view):
        super().__init__()
        self.manager = gui.UIManager()
        self.menu_view = menu_view

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
            self.window.show_view(self.menu_view)

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
