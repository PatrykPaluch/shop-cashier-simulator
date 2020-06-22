import arcade
from game.Views import MenuView,GameEndView,LoseReason
import PIL.ImageFont
import game.Utils as Utils

def main():
    gameWindow = arcade.Window(800, 600, "Test")
    menuView = MenuView()
    gameWindow.show_view(menuView)
    arcade.run()


if __name__ == "__main__":
    main()