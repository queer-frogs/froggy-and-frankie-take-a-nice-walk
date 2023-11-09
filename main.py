import multiprocessing

def run_arcade(arcade_connection):
    import arcade
    from game import Game
    game_instance = Game(arcade_connection)
    game_instance.setup()
    arcade.run()


def run_kivy(kivy_connection):
    from uix import Input
    input_window = Input(kivy_connection)
    input_window.run()


def main():
    """ Main method """
    # Initialize connection between Arcade and Kivy through a (duplex) pipe
    arcade_connection, kivy_connection = multiprocessing.Pipe(duplex=True)
    # TODO pass the connections through run functions into the windows classes in order to send and receive info

    # Initialize and start arcade and kivy processes
    arcade_process = multiprocessing.Process(target=run_arcade, args=[arcade_connection])
    arcade_process.start()

    kivy_process = multiprocessing.Process(target=run_kivy, args=[kivy_connection])
    kivy_process.start()


if __name__ == "__main__":
    main()