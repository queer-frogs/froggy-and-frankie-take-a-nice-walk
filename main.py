import multiprocessing
from game import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE


def run_arcade(arcade_connection):
    import arcade
    from game import MainMenu

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MainMenu(arcade_connection)
    window.show_view(menu_view)
    arcade.run()

    """
    from game import Game
    game_instance = Game(arcade_connection)
    game_instance.setup()
    arcade.run()
    """

def run_kivy(kivy_connection):
    from uix import Input
    input_window = Input(kivy_connection)
    input_window.run()


def main():
    """ Main method """
    # Initialize connection between Arcade and Kivy through a (duplex) pipe
    arcade_connection, kivy_connection = multiprocessing.Pipe(duplex=True)

    # Initialize and start arcade and kivy processes
    arcade_process = multiprocessing.Process(target=run_arcade, args=[arcade_connection])
    arcade_process.start()

    kivy_process = multiprocessing.Process(target=run_kivy, args=[kivy_connection])
    kivy_process.start()


if __name__ == "__main__":
    main()
