from typing import *
from Definitions import *
import game.GameObjects as go
import time


def resourcePath(resource: str) -> str:
    """
    Joins res/ and 'resource' paths and return it as str
    :param resource: resource in res/ directory
    :return: return absolute path to resource
    """
    return str(PATH_RES.joinpath(resource).absolute())


def currTimeMs():
    """
    :return: current time in milliseconds
    """
    return int(time.time()*1000)


def noProducts(productDict : Dict[Any, int]):
    """Counts all products
    :param productDict: product dict (Product, count) pair
    :return: Number of all products in dict
    """
    n = 0
    for key in productDict.keys():
        n += productDict[key]

    return n


class DraggableList:
    """
    Keeps list of Draggable objects and provide functions to update them.
    """

    def __init__(self, initList = None):
        """
        Create list of draggable objects
        :param initList: (Optional) list of objects to add.
                         Will be added only object of instance Draggable
        """
        if initList:
            self._objects: List[go.Draggable] = [ obj for obj in initList if isinstance(obj, go.Draggable) ]
        else:
            self._objects: List[go.Draggable] = []

        self._isAnyInDrag = False

    def reverse(self):
        self._objects.reverse()


    def append(self, obj : go.Draggable):
        if isinstance(obj, go.Draggable):
            self._objects.append(obj)


    def remove(self, obj : go.Draggable):
        self._objects.remove(obj)

    def isAnyInDrag(self):
        return self._isAnyInDrag

    def dragStart(self, x: float, y:float, *, onlyOneAtTime=True):
        """Calls dragStart on every object in list
        :see game.GameObject.Draggable.dragStart
        """
        for obj in self._objects:
            if onlyOneAtTime and self._isAnyInDrag:
                return
            obj.dragStart(x, y)
            self._isAnyInDrag |= obj.isDragged()


    def dragStop(self):
        """Calls dragStart on every object in list
        :see game.GameObject.Draggable.dragStop
        """
        self._isAnyInDrag = False
        for obj in self._objects:
            obj.dragStop()


    def drag(self, x: float, y: float, dx: float, dy: float):
        """Calls dragStart on every object in list
        :see game.GameObject.Draggable.drag
        """
        for obj in self._objects:
            obj.drag(x, y, dx, dy)

    def __getitem__(self, i: int) -> go.Draggable:
        return self._objects[i]

    def __iter__(self):
        return iter(self._objects)