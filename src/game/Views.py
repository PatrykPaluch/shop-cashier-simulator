import arcade
from game.GameObjects import Product
from game.Utils import *
from random import random
import pyglet.gl as gl

class TestView(arcade.View):

    def __init__(self):
        super().__init__()
        self.gameObjects = arcade.SpriteList()
        for i in range(5):
            self.gameObjects.append( Product(resourcePath("pepti.png"), random()*300, random()*300, 100, 100) )

        self.draggableList = DraggableList(self.gameObjects)
        self.draggableList.reverse() # Makes sprites at top the most priority

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)


    def on_draw(self):
        arcade.start_render()
        # Pixel perfect settings (OpenGL)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)


        self.gameObjects.draw()
        pass

    def on_update(self, delta_time: float):
        self.gameObjects.update()
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.draggableList.dragStart(x, y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.draggableList.dragStop()


    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, _buttons: int, _modifiers: int):
        if _buttons & arcade.MOUSE_BUTTON_LEFT == arcade.MOUSE_BUTTON_LEFT:
            self.draggableList.drag(x, y, dx, dy)

