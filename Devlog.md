# Devlog
Czyli wpisy opisujące motywacje i problemy napotkane podczas pracy nad projektem.

## Przygotowanie
Jako środowisko wybrałem **IntelliJ** + **plugin Python**, ponieważ mam obycie z tym środowiskiem i
dobrze się nadaje do wygodnej pracy z Pythonem.

Wybór biblioteki graficznej był trudniejszy. Tkinter nie spełnia moich wymagań. Dokumentacja pygame,
z którym miałem już doświadczenie jest lekko odstraszająca, a i sama biblioteka nie była ciekawa.
Ostatecznie wybór padł na bibliotekę **arcade**, posiadającą bogaty zasób funkcji oraz czytelną
i miłą dla oka dokumentację.

## Budowa projektu
Projekt podzielony jest na główny plik zarządzający główną logiką gry, zawiera on wszystkie kluczowe
dane; Moduł obiektów gry, który zawiera elementy wykorzystywane w grze; Moduł funkcjonalności
dostarczający dodatkowych funkcji, które mogą być przydatne w różnych elementach gry. 

## Napotkane problemy

### Pixel Art
Jak się okazuje, biblioteka **arcade** nie jest przygotowana na pixelart. Nie wszystkie funkcje rysujące
pozwalają na ustawienie filtrów skalowania dla tekstur, a te ręczne ustawianie tych parametrów 
OpenGL nie zawsze działa. Poradziłem sobie z tym problemem zapisując tekstury powiększone w programie
graficznym i zapisywać większe (1 pixel jako 2x2px lub 4x4px).