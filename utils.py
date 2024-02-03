import arcade
import json
import time
import threading


def compute_first_free_slots(arcade_game):
    """
    Computes the first_free_slots list containing the first y coordinate avaible to place a block for each x position.
    The function computes the list for the current level.
    It should be used only once each time a level is edited and is not a user feature.
    The list is saved in levels.json file.
    If an element of the list is -1, it means the column is full.

    Args:
        arcade_game: game instance

    Returns: List (first_free_slots)
    """
    first_free_slots = []
    tile_size = arcade_game.tile_size * arcade_game.level_data["scaling"]
    offset = arcade_game.level_data["offset"]

    # Caculate the number of rows of blocks in the level
    columns_num = int(arcade_game.screen_resolution[0] // tile_size)

    # For each column, get first free vertical slot
    for column in range(offset, columns_num):
        # Get the first row avaible of the column
        current_row = 0
        column_coord = column * tile_size
        row_coord = current_row * tile_size

        # Check if the first row is immediately free
        if not (arcade.get_sprites_at_point(
                (column_coord + 1, row_coord + 1), arcade_game.scene["Platforms"])
                or
                arcade.get_sprites_at_point(
                    (column_coord + 1, row_coord + 1), arcade_game.scene["BackgroundPlatforms"])):
            # + 1 on the coords makes sure we're not checking at zero which will never be True
            free = True
        else:
            free = False

        # Check if the row above is free, repeat until one is
        while not free:
            current_row += 1
            row_coord = current_row * tile_size
            if not (arcade.get_sprites_at_point(
                    (column_coord + 1, row_coord + 1), arcade_game.scene["Platforms"])
                    or
                    arcade.get_sprites_at_point(
                        (column_coord + 1, row_coord + 1), arcade_game.scene["BackgroundPlatforms"])):
                free = True

        first_free_slots.append(current_row)

    return first_free_slots


def save_free_slots(arcade_game):
    """
    Calls compute_first_free_slots and saves the result in levels.json.

    Args:
        arcade_game: game instance

    Returns:

    """

    # Compute
    first_free_slots = compute_first_free_slots(arcade_game)

    # Print in console (again, this should not be performed by players)
    print(first_free_slots)

    # Update the levels.json file
    arcade_game.level_data["first_free_slots"] = first_free_slots

    with open("assets/levels.json", "w") as levels_file:
        json.dump(arcade_game.levels, levels_file, indent=2)


def write_save(arcade_game):
    """
    Writes in the save.json file the new save file. Called when the game is closed.

    Args:
        arcade_game: arcade game instance object

    Returns:
    """
    with open("save.json", "w") as save_file:
        json.dump(arcade_game.save, save_file, indent=2)


class Ticker(threading.Thread):
  """A very simple thread that merely blocks for :attr:`interval` and sets a
  :class:`threading.Event` when the :attr:`interval` has elapsed. It then waits
  for the caller to unset this event before looping again.

  Example use::

    t = Ticker(1.0) # make a ticker
    t.start() # start the ticker in a new thread
    try:
      while t.evt.wait(): # hang out til the time has elapsed
        t.evt.clear() # tell the ticker to loop again
        print time.time(), "FIRING!"
    except:
      t.stop() # tell the thread to stop
      t.join() # wait til the thread actually dies

  """
  # SIGALRM based timing proved to be unreliable on various python installs,
  # so we use a simple thread that blocks on sleep and sets a threading.Event
  # when the timer expires, it does this forever.
  def __init__(self, interval):
    super(Ticker, self).__init__()
    self.interval = interval
    self.evt = threading.Event()
    self.evt.clear()
    self.should_run = threading.Event()
    self.should_run.set()

  def stop(self):
    """Stop the this thread. You probably want to call :meth:`join` immediately
    afterwards
    """
    self.should_run.clear()

  def consume(self):
    was_set = self.evt.is_set()
    if was_set:
      self.evt.clear()
    return was_set

  def run(self):
    """The internal main method of this thread. Block for :attr:`interval`
    seconds before setting :attr:`Ticker.evt`

    .. warning::
      Do not call this directly!  Instead call :meth:`start`.
    """
    while self.should_run.is_set():
      time.sleep(self.interval)
      self.evt.set()

