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
    """
    if x_pos < 0:
        raise ValueError("The value must be positive.")

    # Size of one tile in the grid, adapted to current level scaling
    tile_size = arcade_game.tile_size * arcade_game.level_data["scaling"]

    # Initialize block
    new_block = arcade.Sprite(block_type)
    new_block.width = new_block.height = tile_size
    new_block.left = (x_pos + arcade_game.level_data["offset"]) * tile_size

    # y coord of the block is the first free available
    new_block.bottom = arcade_game.level_data["first_free_slots"][x_pos] * tile_size

    # Increment the first row available in the modified column
    arcade_game.level_data["first_free_slots"][x_pos] += 1

    if new_block.bottom > game.SCREEN_HEIGHT:
        raise ValueError("No room is avaible for this block at that position.")

    # Update sprite list and render the new sprite
    arcade_game.scene["Platforms"].append(new_block)
    arcade_game.scene["Platforms"].draw()


def is_empty(arcade_game, x_pos, y_pos):
    """
    Checks if there is a plotform at the (x_pos, y_pos) position.

    Args:
        arcade_game: arcade game instance
        x_pos: x position (int) checked
        y_pos: y position (int) checked

    Returns:

    """
    tile_size = arcade_game.level_data["scaling"] * arcade_game.tile_size
    coords = (x_pos + arcade_game.level_data["offset"]) * tile_size + 1, y_pos * tile_size + 1
    return arcade.get_sprites_at_point(coords, arcade_game.scene["Platforms"]) == [] \
        and arcade.get_sprites_at_point(coords, arcade_game.scene["BackgroundPlatforms"]) == []
