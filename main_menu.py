import arcade
import arcade.gui as gui

class MenuView(arcade.View):
    """Main menu view class."""
    def __init__(self, main_view):
        super().__init__()
        self.manager = gui.UIManager()
        self.main_view = main_view

        resume_button = gui.UIFlatButton(text="Resume", width=150)
        # reset_level = gui.UIFlatButton(text="Reset Level", width=150)

        exit_button = gui.UIFlatButton(text="Exit", width=150)

        # Initialise a grid in which widgets can be arranged.
        self.box = gui.UIBoxLayout(x=100, y=100, vertical=True, children=[resume_button, exit_button])

        self.manager.add(gui.UIAnchorWidget(anchor_x='center', anchor_y='center', child=self.box))

        @exit_button.event("on_click")
        def on_click_exit_button(event):
            arcade.exit()

        @resume_button.event("on_click")
        def on_click_resume_button(event):
            # Pass already created view because we are resuming.
            self.window.show_view(self.main_view)

        #@reset_level.event("on_click")
        def on_click_reset_level(event):
            self.main_view.setup()
            self.window.show_view(self.main_view)


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