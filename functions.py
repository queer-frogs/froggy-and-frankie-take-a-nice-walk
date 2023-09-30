def grid_position(screen_size_x, screen_size_y, grid_size_x, grid_size_y, coordinate_x, coordinate_y):
    """
    This function takes the size of the screen, of the grid that we went to apply to it and the coordinate in that grid
    and return the values in pixels of where to place your object for it to be where you want on the grid
    :param screen_size_x: horizontal size in pixel of the screen
    :param screen_size_y: vertical size in pixel of the screen
    :param grid_size_x:  horizontal size of the grid
    :param grid_size_y:  vertical size of the grid
    :param coordinate_x: horizontal coordinate on the grid
    :param coordinate_y: vertical coordinate on the grid
    :return: position_x, position_y AKA where in pixels to place your object
    """
    # things that will give us invalide values are send for error treatment
    if (coordinate_x > grid_size_x) or (coordinate_y > grid_size_y) or (grid_size_x > screen_size_x) or (
            grid_size_y > screen_size_y):
        return -1
    # calculate with basic maths the output coordinates
    cell_size_x = screen_size_x / grid_size_x
    cell_size_y = screen_size_y / grid_size_y
    position_x = cell_size_x * (coordinate_x - 1)
    position_y = (grid_size_y - (coordinate_y - 1)) * cell_size_y
    return position_x, position_y
