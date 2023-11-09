import arcade
import game


def place_block(arcade_game, pos, block_type="assets/tiled/tiles/sample_pack/Ground/Stone/stone.png"):
    """
    Places a block on the lowest slot avaible at the hoziontal position passed.

    Args:
        arcade_game: Game object target
        pos: horizontal position where the block should be placed, starts at 0
        block_type: type of the block that should be placed


    Returns: None

    TODO add ressources management for the player's inventory?
    TODO move to 'code_input.py' ; find a solution to have access to arcade_game variables (decorator?)
    TODO include scaling ?
    TODO add animation ?
    """

    tile_size = 16 * 1.8 # * arcade_game.level_data["scaling"]  # size of one tile in the grid

    # TODO for now we use block_type as a path to the png (wip)
    # Initialize block
    new_block = arcade.Sprite(block_type)
    new_block.scale = 1 / tile_size # arcade_game.level_data["scaling"]  # TODO trouver la formule mathématique
    new_block.left = pos * tile_size     # * arcade_game.level_data["scaling"]

    if new_block.center_x > game.SCREEN_WIDTH:
        raise ValueError("The position provided is out of the map borders.")

    # Get first vertical slot available at that x position, add + 10 to make sure we detect round-cornered sprites
    new_block.bottom = 0
    if not arcade.get_sprites_at_point((new_block.left + 10, new_block.bottom + 10), arcade_game.scene["Platforms"]):
        free = True
    else:
        free = False
    while not free:
        new_block.bottom += tile_size
        if not arcade.get_sprites_at_point((new_block.left + 10, new_block.bottom + 10),
                                           arcade_game.scene["Platforms"]):
            free = True
        if new_block.bottom > game.SCREEN_HEIGHT:
            raise ValueError("No room is avaible for this block at that position.")

    # Update sprite list and render the new sprite
    arcade_game.scene["Platforms"].append(new_block)
    arcade_game.scene["Platforms"].draw()
