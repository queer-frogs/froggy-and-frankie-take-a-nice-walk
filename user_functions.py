import arcade
import game


def place(pos):
    """

    Args:
        pos:

    Returns:

    """

    place_block(game_instance, "assets/tiled/tiles/sample_pack/Tiles/switchBlue_pressed.png", pos)


def place_block(arcade_game, block_type, pos):
    """
    Places a block on the lowest slot avaible at the hoziontal position passed.

    Args:
        arcade_game: Game object target
        block_type: type of the block that should be placed
        pos: horizontal position where the block should be placed, starts at 0


    Returns: None

    TODO add ressources management for the player's inventory?
    TODO move to 'code_input.py' ; find a solution to have access to arcade_game variables (decorator?)
    TODO include scaling ?
    TODO add animation ?
    """

    # TODO should be defined earlier in code, or in the specific level
    tile_size = (128, 128)  # size of one tile in the grid

    # TODO for now we use block_type as a path to the png (wip)
    # Initialize block
    new_block = arcade.Sprite(block_type)
    new_block.left = pos * tile_size[0]

    if new_block.center_x > game.SCREEN_WIDTH:
        raise ValueError("The position provided is out of the map borders.")

    # Get first vertical slot available at that x position, add + 10 to make sure we detect round-cornered sprites
    new_block.bottom = 0
    if not arcade.get_sprites_at_point((new_block.left + 10, new_block.bottom + 10), arcade_game.scene["Platforms"]):
        free = True
    else:
        free = False
    while not free:
        new_block.bottom += tile_size[1]
        if not arcade.get_sprites_at_point((new_block.left + 10, new_block.bottom + 10),
                                           arcade_game.scene["Platforms"]):
            free = True
        if new_block.bottom > game.SCREEN_HEIGHT:
            raise ValueError("No room is avaible for this block at that position.")

    # Update sprite list and render the new sprite
    arcade_game.scene["Platforms"].append(new_block)
    arcade_game.scene["Platforms"].draw()
