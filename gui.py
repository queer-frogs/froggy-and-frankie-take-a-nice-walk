import arcade
import arcade.gui as gui

from code_input import user_instructions

class Fenetre_Code():

    """
    Class of all the elements used inside the Text Input Area
    """
    def __init__(self, width=250, height=200):

        self.code = gui.UIInputText(color=arcade.color.DARK_BLUE_GRAY,font_size=10, width=width, height=height, multiline=True, text='')
        self.submit_button = gui.UIFlatButton(color=arcade.color.DARK_POWDER_BLUE, text='Submit', width=100)
        self.submit_button.on_click = self.on_click

        self.box = gui.UIBoxLayout(vertical=True)
        self.box.add(self.code)
        self.box.add(self.submit_button)

        self.widget = gui.UIPadding(bg_color=arcade.color.APRICOT, child=self.box)

        self.input_field = gui.UIAnchorWidget(anchor_x="right", anchor_y="top", child=self.widget)

    def on_click(self, event):
        res = user_instructions(self.code.text)
        print(res)