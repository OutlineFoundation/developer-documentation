---
title: "Add Outline SDK to Your Go Code"
sidebar_label: "Go Integration"
---

Questa guida illustra il processo per configurare il tuo ambiente Go e usare Outline SDK nel codice Go.

Creeremo un'applicazione di esempio denominata `splitfetch` che illustra una funzionalità dell'SDK. Questa applicazione recupera una pagina web, ma invece di inviare la richiesta in un unico pacchetto di rete **utilizza Outline SDK per suddividere il flusso TCP iniziale in due pacchetti separati**. Questo può essere utile per aggirare alcuni tipi di interferenze di rete.

Potrai eseguire l'applicazione in **Linux, Mac e Windows**.
Per l'integrazione con le app mobile, vedi [Aggiungere Outline SDK alla tua app mobile](mobile-app-integration).

## Passaggio 1: configura Go

Per prima cosa avrai bisogno del [linguaggio di programmazione Go](https://go.dev/).
Se hai già installato Go (versione 1.21 o successiva), puoi andare al passaggio successivo.

Per l'installazione puoi seguire la [guida ufficiale](https://go.dev/doc/install) oppure, se usi un gestore di pacchetti:

### Linux

Segui la procedura nella pagina del [Wiki di Go per Ubuntu](https://go.dev/wiki/Ubuntu).

### Mac

### Windows

Al termine, puoi verificare che Go sia stato installato correttamente eseguendo il comando seguente in un terminale:

## Passaggio 2: crea l'applicazione `splitfetch`

È il momento di preparare il progetto `splitfetch`. Per prima cosa, crea la directory di progetto e inizializza un modulo Go:

Successivamente, aggiungi la dipendenza Outline SDK e crea il tuo file `main.go`:

## Passaggio 3: usa Outline SDK nell'applicazione

Apri il file `main.go` nel tuo editor di codice preferito e incolla il codice seguente nel file. Questo codice contiene tutta la logica per l'applicazione `splitfetch`.

Dopo aver salvato il codice, esegui il comando seguente nel terminale per assicurarti che il file `go.mod` sia aggiornato correttamente.

## Passaggio 4: esegui l'applicazione

Ora che il codice è pronto, puoi eseguire l'applicazione `splitfetch`.

Dalla directory `splitfetch` esegui il comando seguente nel tuo terminale, passando un URL come argomento:

L'applicazione viene compilata ed eseguita, visualizzando il contenuto HTML della pagina web.

Se vuoi creare e distribuire un programma autonomo eseguibile senza `go`, usa il comando `go build`:

### Linux e Mac

### Windows

Al termine della creazione, puoi distribuire ed eseguire la tua applicazione.
Ad esempio:
