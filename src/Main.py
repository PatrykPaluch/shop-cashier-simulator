import arcade
from game.Views import TestView


def main():
    game = arcade.Window(800, 600, "Test")
    testView = TestView()
    game.show_view(testView)
    arcade.run()


if __name__ == "__main__":
    main()