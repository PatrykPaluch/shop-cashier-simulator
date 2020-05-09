from typing import *
import arcade
from arcade import Sprite
from enum import Enum

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


class ProductType(Enum):
    BY_PIECE = 1
    BY_WEIGHT = 2

class Product(Sprite, Draggable):

    def __init__(self, name: str, type: ProductType, price: int, texture: str, x: float, y: float, w: float, h: float, *, weight=1, image_x=0.0, image_y=0.0, image_width=0.0, image_height=0.0):
        """
        :param name: name of product
        :param type: product type
        :param texture: path to texture
        :param x: position x of sprite
        :param y: position y of sprite
        :param w: width of sprite
        :param h: height of sprite
        :see arcade.Sprite
        """
        super().__init__(texture, center_x=x, center_y=y, image_x=image_x, image_y=image_y, image_width=image_width, image_height=image_height) #Sprite
        self.__name = name
        self.__type = type
        self.__price = price
        if type == ProductType.BY_PIECE:
            self.__weight = 1
        else:
            self.__weight = weight

        # from Draggable
        self._isDragged = False
        self._dragOffsetX = 0.0
        self._dragOffsetY = 0.0
        # from Sprite
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

    def getName(self):
        return self.__name

    def getType(self):
        return self.__type

    def getPrice(self):
        return self.__price

    def getWeight(self):
        return self.__weight


class GameObject:
    """
    Describe Object with basic functionality (like arcade.Sprite) but is not a Sprite.
    Has own position (x,y)
    """

    # Przykład samodokumentującego się kodu
    def __init__(self, x: float=0, y: float=0):
        self.__x = x
        self.__y = y

    def draw(self):
        pass

    def update(self, dT):
        pass

    def onMouseMove(self, x, y, dx, dy):
        pass

    def onMousePress(self, x, y):
        pass

    def onMouseRelease(self, x, y):
        pass

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def setX(self, x):
        self.__x = x

    def setY(self, y):
        self.__y = y

class CashRegister(GameObject):
    """
    Represents Cash Register, has own num pad and "screen" (text label)
    Will sends events to callback functions
    """

    def __init__(self, x: float, y: float, onScan: Callable[[], list] = None, onNext: Callable[[], None] = None ):
        """
        :param x: position x
        :param y: position y
        :param onScan: callback called when "Scan" button is pressed
        :param onNext: callback called when "Next" button is pressed
        """
        from game.Utils import resourcePath
        super().__init__(x, y)

        self.onScanFunction = onScan
        self.onNextFunction = onNext

        scale = 1.5

        # ======= Main sprite
        w = 160*scale
        h = 176*scale
        self.__sprite = Sprite(resourcePath("UI/cashRegister.png"), center_x=x, center_y=y)
        self.__sprite.width = w
        self.__sprite.height = h

        # ======= Text label
        textLabelTheme = arcade.Theme()
        textLabelTheme.set_font(int(6*scale), arcade.color.BLACK, resourcePath("Fonts/PS2P.ttf"))
        textLabelTheme.add_text_box_texture(resourcePath("UI/TextLabel.png"))

        lbW = int(143*scale)
        lbH = int(16*scale)
        self.__textLabel = arcade.TextDisplay( x-w/2 + 8*scale + lbW/2,
                                               y+h/2 - 4*scale  - lbH/2,
                                               lbW, lbH, theme=textLabelTheme
                                             )
        self.__textLabel.text = "test"

        # ======= buttons
        btSize = 32*scale
        btOffsetTop = 32 * scale
        btOffsetLeft = 10 * scale
        btSizeWithMargin = btSize + 4*scale

        buttonTheme = arcade.Theme()
        buttonTheme.set_font(int(9*scale), arcade.color.BLACK, resourcePath("Fonts/PS2P.ttf"))
        buttonTheme.add_button_textures(
            resourcePath("UI/numpadButton.png"),
            resourcePath("UI/numpadButton_hover.png"),
            resourcePath("UI/numpadButton_clicked.png"),
            resourcePath("UI/numpadButton_locked.png")
        )

        # None value will be ignored
        buttonMap = [
            ["1",   "2",  "3",  "OK"   ],
            ["4",   "5",  "6",  "Scan" ],
            ["7",   "8",  "9",  None   ],
            ["DEL", "0", None,  "Next" ]
        ]


        self.__buttons : List[arcade.TextButton] = []
        for by in range(4):
            for bx  in range(4):
                if buttonMap[by][bx]:
                    bt = ActionButton( x-w/2 + btOffsetLeft + bx*btSizeWithMargin + btSize/2,
                                       y+h/2 - btOffsetTop  - by*btSizeWithMargin - btSize/2,
                                       int(btSize), int(btSize), buttonMap[by][bx], theme=buttonTheme,
                                       action=lambda source: self._buttonPress(source.text)
                                     )

                    if len(buttonMap[by][bx]) > 2:
                        bt.font_size -= int(4*scale)

                    self.__buttons.append(bt)

        #<<<<END __init__

    def _buttonPress(self, bt):
        """
        Callback function for buttons
        :param bt: button name (str)
        """
        if bt in [ str(x) for x in range(10) ]:
            self.__textLabel.text += bt
        elif bt=="DEL":
            self.__textLabel.text = ""
        elif bt=="Scan":
            scannedProducts = self.onScanFunction()
            if len(scannedProducts) == 1 and isinstance(scannedProducts[0], Product):
                prd: Product = scannedProducts[0]
                self.__textLabel.text = prd.getName() + " "
                if prd.getType() == ProductType.BY_PIECE:
                    self.__textLabel.text += str(prd.getPrice()/100) + "kom"
                else:
                    self.__textLabel.text += str(prd.getWeight()/100) + "kg"
                pass
            else:
                self.__textLabel.text = " ERROR "
        elif bt=="Next":
            self.onNextFunction()
        #else: pass

    def draw(self):
        self.__sprite.draw()
        for bt in self.__buttons:
            bt.draw()

        self.__textLabel.draw()

    def onMousePress(self, x, y):
        for bt in self.__buttons:
            bt.check_mouse_press(x, y)

    def onMouseRelease(self, x, y):
        for bt in self.__buttons:
            bt.check_mouse_release(x, y)

    def setX(self, x):
        diff = x - self.getX()
        super().setX(x)
        for bt in self.__buttons:
            bt.center_x += diff

    def setY(self, y):
        diff = y - self.getY()
        super().setY(y)
        for bt in self.__buttons:
            bt.center_y += diff
