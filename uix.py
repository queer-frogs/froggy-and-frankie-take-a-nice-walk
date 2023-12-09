# Import UIX (User Interface XML) elements from kivy
from kivy.app import App
from kivy.uix.codeinput import CodeInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from pygments.lexers import PythonLexer


class Input(App):
    def __init__(self, kivy_connection, forbidden=[]):
        super().__init__()
        self.code = None
        self.output = None
        self.kivy_connection = kivy_connection
        self.forbidden = forbidden

        # Window parameters configuration
        Window.size = (500, 700)
        Window.clearcolor = (1, 1, 1, 1)

    def build(self):

        # Buttons layout
        buttons = BoxLayout(orientation="vertical", spacing=20, size_hint=(0.3,1))
        submit = Button(text="Submit", on_press=self.submit, size_hint=(1,0.3), background_color=(0, 1, 1, 1))
        reset = Button(text="Reset", on_press=self.reset, size_hint=(1,0.3), background_color=(1, 1, 1, 1))
        close = Button(text="Exit", on_press=self.close, size_hint=(1, 0.3), background_color=(1,0,1,1))
        buttons.add_widget(submit)
        buttons.add_widget(reset)
        buttons.add_widget(close)

        # Code layout with submit/reset buttons
        saisie = BoxLayout(orientation="horizontal", spacing=20, size_hint=(1,.65))
        self.code = CodeInput(multiline=True, hint_text="Enter code here ...", lexer=PythonLexer(), size_hint=(.7, 1))
        saisie.add_widget(self.code)
        saisie.add_widget(buttons)

        # Global layout with all the elements of the window
        layout = BoxLayout(orientation="vertical", spacing=10, padding=20, size=(600, 1200), size_hint=(1,1))
        label = Label(text="Output :", halign='left', valign='top', size_hint=(1, .03), color=(0,0,0,1))
        label.bind(size=label.setter('text_size'))
        self.output = Label(text="", halign='left', valign='top', size_hint=(1, .32), color=(0,0,0,1))
        self.output.bind(size=self.output.setter('text_size'))
        layout.add_widget(saisie)
        layout.add_widget(label)
        layout.add_widget(self.output)

        return layout

    def submit(self, obj):
        """
        Is called when the submit button is pressed
        It uses the user_instruction() function to execute the code, and
        prints the result inside the output label
        """

        # Send code input to arcade
        self.kivy_connection.send(self.code.text)

        # If there is some information to receive then display the output label
        if self.kivy_connection.poll(1):
            res = self.kivy_connection.recv()
            if res.startswith("/!\\"):  # error output
                self.output.color = "red"
            else:
                self.output.color = "black"
            self.output.text = res

    def reset(self,obj):
        """
        Clear the input window and the output label
        """
        self.code.text = ""
        self.output.text = ""

    def close(self, obj):
        # closing application
        App.get_running_app().stop()
        # removing window
        Window.close()

