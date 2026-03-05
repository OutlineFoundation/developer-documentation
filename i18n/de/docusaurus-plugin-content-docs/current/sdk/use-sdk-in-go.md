---
title: "Add Outline SDK to Your Go Code"
sidebar_label: "Go Integration"
---

In diesem Leitfaden werden Sie Schritt für Schritt durch die Einrichtung Ihrer Go-Umgebung geführt und Sie erfahren, wie Sie das Outline SDK in Ihrem Go-Code verwenden.

Wir werden eine Beispiel-App mit der Bezeichnung `splitfetch` erstellen, die eine Funktion des SDK vorstellt. Diese Anwendung ruft eine Webseite ab, doch anstatt die Anfrage in einem einzigen Netzwerk-Paket zu senden, **verwendet sie das Outline SDK, um den initialen TCP-Stream in zwei separate Pakete aufzuteilen**. Dies kann dazu beitragen, einige Formen der Netzintervention zu umgehen.

Sie können die App unter **Linux, Mac und Windows** ausführen.
Informationen zur Einbindung in mobile Apps finden Sie hier: [Outline SDK zu Ihrer mobilen App hinzufügen](mobile-app-integration).

## Schritt 1: Go einrichten

Zuerst brauchen Sie [Go (Programmiersprache)](https://go.dev/).
Wenn Sie Go bereits installiert haben (Version 1.21 oder höher), können Sie direkt zum nächsten Schritt weitergehen.

Für die Installation können Sie den Schritten im [offiziellen Leitfaden](https://go.dev/doc/install) folgen oder, wenn Sie einen Paketmanager verwenden:

### Linux

Folgen Sie den in [Go Wiki: Ubuntu](https://go.dev/wiki/Ubuntu) beschriebenen Schritten.

### Mac

### Windows

Nach der Installation von Go können Sie überprüfen, ob es korrekt installiert wurde, indem Sie den folgenden Befehl in einem Terminal ausführen:

## Schritt 2: `splitfetch`-App erstellen

Richten Sie das `splitfetch`-Projekt ein. Dazu müssen Sie zuerst das Projektverzeichnis erstellen und ein Go-Modul initialisieren:

Ziehen Sie dann das Outline SDK hinzu und erstellen Sie Ihre `main.go`-Datei:

## Schritt 3: Outline SDK in der Anwendung verwenden

Öffnen Sie die `main.go`-Datei in Ihrem bevorzugten Code-Editor und fügen Sie den folgenden Code ein. Dieser Code enthält sämtliche Logik für unsere `splitfetch`-App.

Nach dem Speichern des Codes führen Sie den folgenden Befehl in Ihrem Terminal aus, um zu prüfen, ob die `go.mod`-Datei ordnungsgemäß aktualisiert wurde.

## Schritt 4: Anwendung ausführen

Mit dem erstellten Code können Sie die `splitfetch`-App nun ausführen.

Führen Sie im `splitfetch`-Verzeichnis den folgenden Befehl in Ihrem Terminal aus und geben Sie dabei eine URL als Argument an:

Damit wird die Anwendung kompiliert und ausgeführt und der HTML-Inhalt der Webseite angezeigt.

Wenn Sie ein eigenständiges Programm erstellen und verteilen möchten, das ohne `go` ausgeführt werden kann, verwenden Sie den Befehl `go build`:

### Linux und Mac

### Windows

Sobald der Build erstellt ist, können Sie Ihre App verteilen und ausführen.
Beispiel:
