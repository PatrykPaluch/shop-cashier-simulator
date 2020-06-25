# Devlog
Czyli wpisy opisujące motywacje i problemy napotkane podczas pracy nad projektem.

Raport dostępny w pliku [Raport.md](Raport.md)

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
pozwalają na ustawienie filtrów skalowania dla tekstur, a ręczne ustawianie tych parametrów 
OpenGL nie zawsze działa. Poradziłem sobie z tym problemem zapisując tekstury powiększone w programie
graficznym i zapisywać większe (1 pixel jako 2x2px lub 4x4px). 

### Porównywanie produktów
W pewnym momencie miałem potrzebę zaimplementowania dwóch różnych metod `__eq__` oraz `__hash__`
ponieważ okazało się że biblioteka arcade w swojej klasie `SpriteList` wykorzystuje Python'owy
słownik przez co produkty które miały być uważane za równe sobie (np. `a==b`) ale jednak traktowane
oddzielnie, przestawały być wyświetlane na ekranie bo `SpriteList` nie dodawał kolejnych kopi tego
samego produktu do listy (Biblioteka *arcade* korzysta z dość złożonego systemu zarządzania
sprite'ami). 

Rozwiązałem ten problem implementując własną listę na sprite co nie było trudne, musiałem jedynie
sam napisać pętle do wywołania odpowiednich funkcji na nich (`SpriteList` realizuje to samodzielnie).
Więc obyło się bez zmuszenia słownika by korzystał z innej implementacji funkcji "hash".

### Inne
Standardowo większość problemów to było proste opracowanie algorytmów i ich implementacja - nic 
szczególnego. 

## Podsumowanie po skończeniu
Doświadczony innymi rozwiązaniami w dziedzinie GameDev, Python okazał się złym narzędziem do tego.
Wolałbym go nie używać do tworzenia gier. Są języki znacznie wydajniejsze, dające większą kontrolę i
bardziej przystępne do tworzenia gier. Oczywiście nie skreślam Pythona w innych zastosowaniach,
ale nieprzyjemnie mi się w nim pracowało.
   