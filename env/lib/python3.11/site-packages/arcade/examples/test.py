import arcade
import pyglet

arcade.open_window(600, 600, "Drawing Primitives Example")
pyglet_window = arcade.get_window()

arcade.set_background_color(arcade.color.WHITE)
arcade.start_render()

text = "ABCDEF"
label = pyglet.text.Label(
    text=text,
    x=100,
    y=100,
    font_name=('calibri', 'arial'),
    font_size=16,
    anchor_x='left',
    anchor_y='baseline',
    color=(0, 0, 0, 255)
)

with pyglet_window.ctx.pyglet_rendering():
    label.draw()

label.text = "ABCDEF"
label.position = 205, 200, 0
with pyglet_window.ctx.pyglet_rendering():
    label.draw()

arcade.finish_render()

pyglet.app.run()
