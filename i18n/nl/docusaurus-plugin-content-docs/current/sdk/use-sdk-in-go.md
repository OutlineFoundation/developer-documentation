---
title: "Add Outline SDK to Your Go Code"
sidebar_label: "Go Integration"
---

Deze handleiding leidt je door het proces om je Go-omgeving in te stellen en de Outline SDK te gebruiken in je Go-code.

We maken een voorbeeld-app met de naam `splitfetch` waarin een functie van de SDK wordt getoond. Deze app haalt een webpagina op, maar in plaats van het verzoek in één netwerkpakket te sturen, **wordt de Outline SDK gebruikt om de eerste TCP-stream op te splitsen in 2 aparte pakketten**. Hierdoor kunnen sommige soorten netwerkinterventies worden overgeslagen.

Je kunt de app gebruiken op **Linux, Mac en Windows**.
Ga voor integratie met mobiele apps naar [Outline SDK toevoegen aan een mobiele app](mobile-app-integration).

## Stap 1: Stel Go in

Hiervoor heb je de [Programmeertaal Go](https://go.dev/) nodig.
Als je Go (versie 1.21 of hoger) al hebt geïnstalleerd, kun je doorgaan met de volgende stap.

Volg voor de installatie de [officiële handleiding](https://go.dev/doc/install) of doe het volgende als je een pakketmanager gebruikt:

### Linux

Volg de stappen in [Go Wiki: Ubuntu](https://go.dev/wiki/Ubuntu).

### Mac

### Windows

Nadat Go is geïnstalleerd, kun je controleren of dit goed is gegaan door de volgende opdracht uit te voeren in een terminal:

## Stap 2: Maak de `splitfetch`-app

Nu gaan we het `splitfetch`-project instellen. Maak eerst de projectdirectory en initialiseer een Go-module:

Gebruik dan de Outline SDK en maak het `main.go`-bestand:

## Stap 3: Gebruik Outline SDK in de app

Open het `main.go`-bestand in je favoriete code-editor en plak er de volgende code in. Deze code bevat alle logica voor onze `splitfetch`-app.

Voer nadat je de code hebt opgeslagen de volgende opdracht uit in je terminal om te controleren of het `go.mod`-bestand juist is geüpdatet.

## Stap 4: Voer de app uit

Nu de code is toegevoegd, kun je de `splitfetch`-app uitvoeren.

Voer in de `splitfetch`-directory de volgende opdracht uit in je terminal, waarbij een URL wordt meegegeven als argument:

Hierdoor wordt de app samengesteld en uitgevoerd en wordt de HTML-content van de webpagina getoond.

Als je een los programma wilt maken en distribueren dat je kunt uitvoeren zonder `go`, gebruik je de opdracht `go build`:

### Linux en Mac

### Windows

Nadat de build klaar is, kun je de app distribueren en uitvoeren.
Bijvoorbeeld:
