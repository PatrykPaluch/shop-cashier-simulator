import arcade
from arcade import View
from game.Utils import DraggableList, resourcePath
from game.GameObjects import Product, CashRegister, ActionButton
from random import random
import pyglet.gl as gl

class TestView(View):

    def __init__(self):
        from game.Utils import resourcePath
        super().__init__()
        self.gameObjects = arcade.SpriteList()
        for i in range(5):
            self.gameObjects.append( Product(resourcePath("pepti.png"), random()*300, random()*300, 100, 100) )

        self.draggableList = DraggableList(self.gameObjects)
        self.draggableList.reverse() # Makes sprites at top the most priority
        self.cashRegister = CashRegister(400, 300)


    def on_show(self):
        arcade.set_background_color(arcade.color.ALICE_BLUE)


    def on_draw(self):
        arcade.start_render()
        # Pixel perfect settings (in OpenGL)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

        self.cashRegister.draw()

        #self.gameObjects.draw()

        pass

    def on_update(self, delta_time: float):
        self.gameObjects.update()
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.draggableList.dragStart(x, y)
            self.cashRegister.onMousePress(x, y)


    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.draggableList.dragStop()
            self.cashRegister.onMouseRelease(x, y)


    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, _buttons: int, _modifiers: int):
        if _buttons & arcade.MOUSE_BUTTON_LEFT == arcade.MOUSE_BUTTON_LEFT:
            self.draggableList.drag(x, y, dx, dy)


    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.cashRegister.onMouseMove(x, y, dx, dy)

class MenuView(View):

    def __init__(self):
        super().__init__()

        self.theme = arcade.Theme()
        self.sprites = arcade.SpriteList()

    def startGame(self):
        self.window.show_view(TestView())

    def exitGame(self):
        self.window.close()

    def setupTheme(self):
        self.theme.set_font(18, arcade.color.BLACK, resourcePath("Fonts/PS2P.ttf"))
        normal = resourcePath("UI/menuButton.png")
        hover = resourcePath("UI/menuButton_hover.png")
        clicked = resourcePath("UI/menuButton_clicked.png")
        locked = resourcePath("UI/menuButton_locked.png")
        self.theme.add_button_textures(normal, hover, clicked, locked)

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

        self.setupTheme()

        (w, h) = self.window.get_size()

        self.button_list.append(ActionButton(150, h-75, 200, 50, "Start", self.theme, action=lambda source: self.startGame()))
        self.button_list.append(ActionButton(150, h-150, 200, 50, "Wyjście", self.theme, action=lambda source: self.exitGame()))

        backgroundImage = arcade.Sprite(resourcePath("UI/menuBg.png"), 4, 0, 0, 0, 0, w/2, h/2)
        self.sprites.append(backgroundImage)

    def on_draw(self):
        arcade.start_render()

        # Pixel perfect settings (in OpenGL)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)


        self.sprites.draw( filter=gl.GL_NEAREST )

        for button in self.button_list:
            button.draw()


class GameLoadingView(View):
    pass