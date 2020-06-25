# Raport
Zobacz [założenia projektu](ProjectTopic.md).

Zobacz motywacje oraz napotkane problemy w [devlogu](Devlog.md).

Program lekko odbiega od założeń, ale realizuje ich zdecydowanie większą część z pewnym marginesem
własnej interpretacji.


# Elementy 
Linki odnoszą się do projektu z commit'a `3973907` o tagowanego jako `v1.0`

- [Wyrażenia Lambda (2)](https://github.com/Patrykas1000/shop-cashier-simulator/blob/v1.0/src/game/Views.py#L234-L235)
- [Callback - argument](https://github.com/Patrykas1000/shop-cashier-simulator/blob/v1.0/src/game/Views.py#L46-L50)
oraz [Callback - parametr](https://github.com/Patrykas1000/shop-cashier-simulator/blob/v1.0/src/game/GameObjects.py#L218-L220)
-  [List comprehensions](https://github.com/Patrykas1000/shop-cashier-simulator/blob/v1.0/src/game/Utils.py#L47)
- [Moduły](https://github.com/Patrykas1000/shop-cashier-simulator/tree/v1.0/src/game):
`game/GameObjects.py`, `game/Utils.py`, `game/Views.py`, `Definitions.py`, `Main.py`
- [Enum 1](https://github.com/Patrykas1000/shop-cashier-simulator/blob/v1.0/src/game/GameObjects.py#L67-L69),
 [Enum 2](https://github.com/Patrykas1000/shop-cashier-simulator/blob/v1.0/src/game/Views.py#L10-L12)
- Klasy:
[GameView](https://github.com/Patrykas1000/shop-cashier-simulator/blob/v1.0/src/game/Views.py#L14),
[MenuView](https://github.com/Patrykas1000/shop-cashier-simulator/blob/v1.0/src/game/Views.py#L205),
[GameEndView](https://github.com/Patrykas1000/shop-cashier-simulator/blob/v1.0/src/game/Views.py#L260),
[ActionButton](https://github.com/Patrykas1000/shop-cashier-simulator/blob/v1.0/src/game/GameObjects.py#L5),
[Draggable](https://github.com/Patrykas1000/shop-cashier-simulator/blob/v1.0/src/game/GameObjects.py#L31),
[Product](https://github.com/Patrykas1000/shop-cashier-simulator/blob/v1.0/src/game/GameObjects.py#L71),
[GameObject](https://github.com/Patrykas1000/shop-cashier-simulator/blob/v1.0/src/game/GameObjects.py#L173),
[CashRegister](https://github.com/Patrykas1000/shop-cashier-simulator/blob/v1.0/src/game/GameObjects.py#L211),
[DraggableList](https://github.com/Patrykas1000/shop-cashier-simulator/blob/v1.0/src/game/Utils.py#L35),
- Dziedziczenie: 
  - **ActionButton**(arcade.TextButton)
  - **Product**(arcade.Sprite, **Draggable**)
  - **CashRegister**(**GameObject**)
  - **GameView**(arcade.View)
  - **MenuView**(arcade.View)
  - **GameEndView**(arcade.View)   
- Algorytmy ponad opisane wymagania:
  - [Drag'n'drop](https://github.com/Patrykas1000/shop-cashier-simulator/blob/39739076b9de15af4a857b745a2f876b60ca09f0/src/game/GameObjects.py#L112-L124)
  - [Skanowanie produktów](https://github.com/Patrykas1000/shop-cashier-simulator/blob/39739076b9de15af4a857b745a2f876b60ca09f0/src/game/GameObjects.py#L339-L397)
  - Generowanie produktów pasujące do formy rozgrywki:
[nextClient()](https://github.com/Patrykas1000/shop-cashier-simulator/blob/39739076b9de15af4a857b745a2f876b60ca09f0/src/game/Views.py#L80-L105)
oraz [generateClient()](https://github.com/Patrykas1000/shop-cashier-simulator/blob/39739076b9de15af4a857b745a2f876b60ca09f0/src/game/Views.py#L136-L159)

# Repo GitHub
Repozytorium GitHub:
- [master](https://github.com/Patrykas1000/shop-cashier-simulator)
- [Omawiany v1.0](https://github.com/Patrykas1000/shop-cashier-simulator/tree/v1.0)