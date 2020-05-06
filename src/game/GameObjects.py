from typing import *
import arcade
from arcade import Sprite

class ActionButton(arcade.TextButton):
    def __init__(self, x: float, y: float, w: float, h: float, text: str, theme: arcade.Theme = None, action: Callable[[arcade.TextButton], None] = None):
        """
        Do all registered actions on click
        :param action: Function to execute (params: [source]; returns: None)
        """
        super().__init__(x, y, w, h, text, theme=theme)
        self.actions = []
        if action:
            self.actions.append(action)

    def addAction(self, action: Callable[[arcade.TextButton], None]):
        self.actions.append(action)

    def removeAction(self, action: Callable[[arcade.TextButton], None]):
        self.actions.remove(action)

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            for action in self.actions:
                action(self)
            self.pressed = False

class Draggable:
    def __init__(self):
        self._isDragged = False

    def dragStart(self, x: float, y: float):
        """Called once when drag is started
        Override should check if (x,y) is contained in dragged object
        :param x: cursor x position
        :param y: cursor y position
        """
        pass

    def dragStop(self):
        self._isDragged = False
        """Called once when drag is ended
        Override should check if object isDragged before operation any operation and set _isDragged to False
        """
        pass

    def drag(self, x: float, y: float, dx: float, dy: float):
        """Will be called every time the cursor is moved
        Override should check if object isDragged before operation
        :param x: cursor x position
        :param y: cursor y position
        :param dx: cursor x position relative to last frame (delta x)
        :param dy: cursor y position relative to last frame (delta y)
        """
        pass

    def isDragged(self) -> bool:
        """
        :return: True if object is currently in drag, false otherwise
        """
        return self._isDragged


class Product(Sprite, Draggable):

    def __init__(self, texture: str, x: float, y: float, w: float, h: float, *, image_x=0.0, image_y=0.0, image_width=0.0, image_height=0.0):
        """
        :param texture:
        :param x: position x of sprite
        :param y: position y of sprite
        :param w: width of sprite
        :param h: height of sprite
        :see arcade.Sprite
        """
        super().__init__(texture, center_x=x, center_y=y, image_x=image_x, image_y=image_y, image_width=image_width, image_height=image_height) #Sprite
        self._isDragged = False
        self._dragOffsetX = 0.0
        self._dragOffsetY = 0.0
        self.width = w
        self.height = h
        # IntelliJ just thinks this function has no arguments -.-
        # noinspection PyArgumentList
        self.set_hit_box([[w / 2, h / 2], [w / 2, -h / 2], [-w / 2, -h / w], [-w / 2, h / 2]])


    def dragStart(self, x: float, y: float):
        if self.collides_with_point( (x,y) ):
            self._isDragged = True
            self._dragOffsetX = self.center_x - x
            self._dragOffsetY = self.center_y - y

    def dragStop(self):
        self._isDragged = False

    def drag(self, x: float, y: float, dx: float, dy: float):
        if not self._isDragged: return
        self.center_x = x + self._dragOffsetX
        self.center_y = y + self._dragOffsetY