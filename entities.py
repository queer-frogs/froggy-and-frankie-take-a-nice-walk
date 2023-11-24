import arcade


class Entity(arcade.Sprite):
    """ Basic structure of every sprite """

    def __init__(self, image_source):
        # Set up classe parent
        super().__init__(image_source)

        # Set default values
        # Load different textures for different states of action
        # with main_path + _ + action + nb

        # Set initial texture
        # Set hit boxes


class PlayerCharacter(Entity):
    """ Player Sprite """

    def __init__(self, image_source):
        super().__init__(image_source)

        # Track state
        self.walking = False
        self.jumping = False

    def update_animation(self, delta_time: float = 1 / 60):
        # Update sprite based on state
        pass
