import arcade
import json


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
        # TODO add check on platforms background layer
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

        '''probably useless
        # Check if the position is on the screen
        if row_coord > arcade_game.screen_resolution[1]:
            current_row = -1
        '''

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
