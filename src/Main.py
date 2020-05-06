import arcade
from game.Views import MenuView

def main():
    game = arcade.Window(800, 600, "Test")
    menuView = MenuView()
    game.show_view(menuView)
    arcade.run()


if __name__ == "__main__":
    main()