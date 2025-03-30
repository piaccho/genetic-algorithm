# Wprowadzenie 

Celem projektu jest implementacja algorytmu genetycznego do optymalizacji funkcji wielu zmiennych. Projekt powinien być zaimplementowany w języku programowania Python. 

# Założenia projektu 

1. Implementacja algorytmu genetycznego dla problemów maksymalizacji i minimalizacji funkcji. 
2. Możliwość konfiguracji liczby zmiennych (np. 5, 10, 20, 27). 
 
# Elementy implementacji 

 - Binarna reprezentacja chromosomu i konfiguracja dokładności.
 - Konfiguracja wielkości populacji.
 - Konfiguracja liczby epok.
 - Metody selekcji: najlepszych, ruletki, turniejowa.
 - Krzyżowanie: jednopunktowe, dwupunktowe, jednorodne, ziarniste.
 - Mutacje: brzegowa, jedno- i dwupunktowa.
 - Operator inwersji i strategia elitarna. 
 
# Wybór funkcji testowych
 
 Funkcją wielu zmiennych jaką algortym genetczny będzie optymalizował będzie funkcja Hyperellipsoid.
- Wzór w Latex:
$$
f(x)=\sum_{i=0}^{N-1} \sum_{j=0}^{i} x_j^2
$$
- Sugerowany zakres poszukiwań: `[-65.536, 65.536]` 
- Globalne minima: `(0.0, [0.0, 0.0])`

# Aplikacja i wizualizacja 

 1. Graficzny interfejs użytkownika. 
 2. Możliwość konfiguracji parametrów algorytmu poprzez GUI. 
 3. Wyświetlanie czasu obliczeń. 
 4. Generowanie wykresów wartości funkcji w iteracjach. 
 5. Zapisywanie wyników do pliku/bazy danych. 
 
# Sprawozdanie

- Technologie użyte w projekcie.
- Wymagania środowiskowe.
- Opis wybranych funkcji testowych i ich optima.
- Wykresy wyników.
- Porównanie wyników dla różnych konfiguracji algorytmu.
- Podsumowanie i analiza błędów. 
