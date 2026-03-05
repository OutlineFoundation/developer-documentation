---
title: "Add Outline SDK to Your Go Code"
sidebar_label: "Go Integration"
---

Ten przewodnik przeprowadzi Cię przez proces konfigurowania środowiska Go i korzystania z pakietu Outline SDK w kodzie Go.

Utworzymy przykładową aplikację o nazwie `splitfetch`, aby zaprezentować cechy i funkcje tego pakietu SDK. Aplikacja ta pobiera stronę internetową, ale zamiast wysyłać żądanie w pojedynczym pakiecie sieciowym, **używa Outline SDK do podzielenia początkowego strumienia TCP na dwa osobne pakiety**. Może to ułatwić obchodzenie niektórych rodzajów interwencji w sieci.

Aplikacja będzie działać na platformach **Linux, Mac i Windows**.
Informacje na temat integracji z aplikacjami mobilnymi znajdziesz w temacie [Dodawanie pakietu Outline SDK do aplikacji mobilnej](mobile-app-integration).

## Krok 1. Skonfiguruj Go

Przede wszystkim potrzebujesz [języka programowania Go](https://go.dev/).
Jeśli masz już zainstalowane środowisko Go w wersji 1.21 lub nowszej, możesz przejść do następnego kroku.

Instrukcje instalacji znajdziesz w [oficjalnym przewodniku](https://go.dev/doc/install), a jeśli korzystasz z systemu zarządzania pakietami:

### Linux

Postępuj zgodnie z instrukcjami podanymi na stronie [Go Wiki: Ubuntu](https://go.dev/wiki/Ubuntu).

### Mac

### Windows

Po zainstalowaniu środowiska Go możesz sprawdzić, czy wszystko działa prawidłowo, uruchamiając w terminalu to polecenie:

## Krok 2. Utwórz aplikację `splitfetch`

Teraz skonfigurujemy projekt `splitfetch`. Najpierw utwórz katalog projektu i zainicjuj moduł Go:

Następnie pobierz pakiet Outline SDK i utwórz plik `main.go`:

## Krok 3. Użyj pakietu Outline SDK w aplikacji

Otwórz plik `main.go` w ulubionym edytorze kodu i wklej do niego podany niżej kod. Ten kod zawiera całą logikę działania aplikacji `splitfetch`.

Po zapisaniu kodu uruchom w terminalu podane niżej polecenie, aby się upewnić, że plik `go.mod` został prawidłowo zaktualizowany.

## Krok 4. Uruchom aplikację

Po dodaniu kodu możesz uruchomić aplikację `splitfetch`.

Z poziomu katalogu `splitfetch` uruchom w terminalu podane niżej polecenie, przekazując adres URL jako argument:

Aplikacja zostanie skompilowana i uruchomiona, a następnie wyświetli zawartość HTML strony internetowej.

Jeśli chcesz utworzyć i rozpowszechnić samodzielny program, który można uruchomić bez środowiska `go`, użyj polecenia `go build`:

### Linux i Mac

### Windows

Po skompilowaniu aplikacji możesz ją rozpowszechnić i zacząć z niej korzystać.
Przykład:
