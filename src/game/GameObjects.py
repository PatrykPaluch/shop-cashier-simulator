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
    __lastId = 0

    def __init__(self, name: str, type: ProductType, price: int, texture: str, x: float, y: float, w: float, h: float, *, weight=1, image_x=0.0, image_y=0.0, image_width=0.0, image_height=0.0):
        """
        :param name: name of product
        :param type: product type
        :param texture: path to texture
        :param x: position x of sprite
        :param y: position y of sprite
        :param w: width of sprite
        :param h: height of sprite
        :param type: type of product (by piece/weight)
        :param price: price of product (for piece/1kg)
        :param weight: weight of product, only for type=BY_WEIGHT
        :see arcade.Sprite
        """
        super().__init__(texture, center_x=x, center_y=y, image_x=image_x, image_y=image_y, image_width=image_width, image_height=image_height) #Sprite
        self.__texturePath = texture
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

        self.__id = Product.__lastId
        Product.__lastId += 1

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

    def clone(self, weight=-1):
        """Creates new identical product (can change weight)
        :param weight: weight to override or -1 to keep original
        :return: clone of self
        """
        return Product(self.__name, self.__type, self.__price, self.__texturePath,
                       self.center_x, self.center_y,
                       self.width, self.height,
                       weight= self.__weight if weight<0 else weight )

    def __eq__(self, other):
        if other is None or other.__class__ != self.__class__:
            return False

        # product is defined by hi params, not by Sprite
        return self.__name == other.__name and self.__price == other.__price \
           and self.__type == other.__type and self.__weight == other.__weight


    def __hash__(self):
        _hash = hash(self.__name) ^ hash(self.__price) ^ hash(self.__type) ^ hash(self.__weight)
        if self.__type == ProductType.BY_WEIGHT:
            _hash ^= hash(self.__id)
        return _hash

    def specialHash(self):
        # each product has unique id
        return hash(self.__id)

    def specialEquals(self, other):
        if other is None or other.__class__ != self.__class__:
            return False
        # each product has unique id
        return self.__id == other.__id

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

    def __init__(self, x: float, y: float,
                 onScan: Callable[[], list] = None,
                 onNext: Callable[[], None] = None,
                 onOk: Callable[[Union[Product, List[Product]], int], None] = None):
        """
        :param x: position x
        :param y: position y
        :param onScan: callback called when "Scan" button is pressed.
            <ol><li><b>param: Product | List[Product]</b> - Product if is by_piece,
                        otherwise multiple products by_weight as List[Product]</li>
                <li><b>param: int</b> - if Product is by_piece then entered number, otherwise 1 (when multiple products
                        by_weight)</li></ol>
        :param onNext: callback called when "Next" button is pressed.
        :param onOk: callback called when "Ok" button is pressed.
            <ul><li><b>returns</b> - list of object on scanner</li><ul>
        """
        from game.Utils import resourcePath
        super().__init__(x, y)

        self.__resetText = True

        self.onScanFunction = onScan
        self.onNextFunction = onNext
        self.onOkFunction   = onOk

        self.__lastScanProduct = None
        self.__lastScanCount = 0

        scale = 1.5

        # ======= Main sprite
        w = 160*scale
        h = 176*scale
        self.__sprite = Sprite(resourcePath("UI/cashRegister.png"), center_x=x, center_y=y)
        self.__sprite.width = w
        self.__sprite.height = h

        # ======= Text label
        textLabelTheme = arcade.Theme()
        textLabelTheme.set_font(int(4*scale), arcade.color.BLACK, resourcePath("Fonts/PS2P.ttf"))
        textLabelTheme.add_text_box_texture(resourcePath("UI/TextLabel.png"))

        lbW = int(143*scale)
        lbH = int(16*scale)
        self.__textLabel = arcade.TextDisplay( x-w/2 + 8*scale + lbW/2,
                                               y+h/2 - 4*scale  - lbH/2,
                                               lbW, lbH, theme=textLabelTheme
                                             )
        self.__textLabel.text = ""

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

    def __changeText(self, text, resetText = False):
        """ Appends or sets text in text field.

        :param text: Text to set/append
        :param resetText: if true then sets text, append text otherwise.
        """
        if self.__resetText or resetText:
            self.__textLabel.text = ""
            self.__resetText = False

        self.__textLabel.text += text

    def __setError(self):
        """
        Sets text to " ERROR " and sets self.__resetText flag
        :see __changeText:
        """
        self.__textLabel.text = " ERROR "
        self.__resetText = True

    def _buttonPress(self, bt):
        """
        Callback function for buttons
        :param bt: button name (str)
        """
        if bt in [ str(x) for x in range(10) ]:
            self.__changeText(bt)
        elif bt=="DEL":
            self.__textLabel.text = ""
        elif bt=="Scan":

            scannedProducts = self.onScanFunction()
            noScannedProducts = len(scannedProducts)

            if noScannedProducts > 0 and isinstance(scannedProducts[0], Product):

                noProductStr = self.__textLabel.text

                # ========= BY WEIGHT =========
                if scannedProducts[0].getType() == ProductType.BY_WEIGHT:
                    # Screen must be empty
                    if len(noProductStr) > 0:
                        self.__setError()
                        return

                    weightSum = 0
                    prdName = scannedProducts[0].getName()
                    for prd in scannedProducts:
                        # Only products by weight can be scanned with others at same time
                        if (not isinstance(prd, Product)) or prd.getType() != ProductType.BY_WEIGHT:
                            self.__setError()
                            return
                        # Each scanned product must have equal name (eg. 'onion', 'banana')
                        if prd.getName() != prdName:
                            self.__setError()
                            return
                        weightSum += prd.getWeight()

                    # Each with same name has same price
                    pricePerKgInKom = scannedProducts[0].getPrice() / 100
                    weightInKg = weightSum / 100
                    priceForAllInKom = int(pricePerKgInKom * weightInKg * 100) / 100
                    self.__textLabel.text = prdName + ": " \
                                            + str(weightInKg) + "kg | " + str(priceForAllInKom) + "kom"

                    self.__setLastScannedProduct(scannedProducts, 1)

                # ========= BY PIECE =========
                else:
                    # only one product by time
                    if noScannedProducts != 1:
                        self.__setError()
                        return

                    # must enter number
                    if not noProductStr.isdigit() or noProductStr.startswith("0"):
                        self.__setError()
                        return

                    noProduct = int(noProductStr)
                    prd: Product = scannedProducts[0]

                    self.__textLabel.text = noProductStr + "x " + prd.getName() + ": " +  str((prd.getPrice()*noProduct)/100) + "kom"

                    self.__setLastScannedProduct(prd, noProduct)

            else:
                self.__setError()

            self.__resetText = True
        elif bt=="Next":
            self.onNextFunction()
        elif bt=="OK":
            if not self.__lastScanProduct is None:
                self.__textLabel.text = ""
                self.onOkFunction(self.__lastScanProduct, self.__lastScanCount)
                self.__lastScanProduct = None
                self.__lastScanCount = 0
        #else: pass

    def __setLastScannedProduct(self, prd, count=1):
        self.__lastScanProduct = prd
        self.__lastScanCount = count

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
