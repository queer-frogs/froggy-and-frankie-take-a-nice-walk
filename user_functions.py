import arcade
import game

def place_block(arcade_game, x_pos, block_type="assets/tiled/tiles/Minecraft tiles/acacia_planks.png"):
    """
    Places a block on the lowest slot avaible at the hoziontal position passed.

    Args:
        arcade_game: Game object target
        x_pos: horizontal position where the block should be placed, starts at 0, counted in tiles
        block_type: type of the block that should be placed


    Returns: None

    TODO add ressources management for the player's inventory, different tiles?
    TODO add animation ?
    """

    # Size of one tile in the grid, adapted to current level scaling
    tile_size = 16 * arcade_game.level_data["scaling"]

    # Position zero for x is not the same in every level
    x_pos += 0  # + arcade_game.level_data["offset"]
    y_pos = 0

    # Initialize block
    new_block = arcade.Sprite(block_type)
    new_block.width = new_block.height = tile_size
    new_block.left = (x_pos + arcade_game.level_data["offset"]) * tile_size
    new_block.bottom = 0

    # Check if blocks were precedently placed at that x_pos, allowing us to directly get the y coords of the next block
    try:
        if arcade_game.already_placed[x_pos] != 0:
            y_pos = arcade_game.already_placed[x_pos] + 1
            arcade_game.already_placed[x_pos] = y_pos
            new_block.bottom = y_pos * tile_size
            skip_check = True
        else:
            skip_check = False
    except IndexError:
        skip_check = False
        for i in range(x_pos - len(arcade_game.already_placed) + 1):
            arcade_game.already_placed.append(0)

    if new_block.center_x > game.SCREEN_WIDTH:
        raise ValueError("The position provided is out of the map borders.")

    if not skip_check:
        # Get first vertical slot available at that x position
        if not arcade.get_sprites_at_point((new_block.left, new_block.bottom), arcade_game.scene["Platforms"]):
            free = True
            y_pos += 1
        else:
            free = False
            # y_pos += 1
        while not free:
            y_pos += 1
            new_block.bottom += tile_size
            if not arcade.get_sprites_at_point((new_block.left, new_block.bottom),
                                               arcade_game.scene["Platforms"]):
                free = True

    if new_block.bottom > game.SCREEN_HEIGHT:
        raise ValueError("No room is avaible for this block at that position.")

    # Update sprite list and render the new sprite
    arcade_game.scene["Platforms"].append(new_block)
    arcade_game.scene["Platforms"].draw()

    # Keep in memory last y_pos at which a block was placed at x_pos
    arcade_game.already_placed[x_pos] = y_pos
