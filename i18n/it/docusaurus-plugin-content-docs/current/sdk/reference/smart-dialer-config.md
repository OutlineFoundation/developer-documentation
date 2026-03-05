---
title: "Smart Dialer Configuration"
sidebar_label: "Smart Dialer Config"
---

Lo **Smart Dialer** cerca una strategia per sbloccare il DNS e il TLS per un elenco specificato di domini di test. Richiede una configurazione che descriva più strategie tra cui scegliere.

## Configurazione YAML per lo Smart Dialer

La configurazione per lo Smart Dialer deve essere in formato YAML. Ecco un esempio:

### Configurazione DNS

- Il campo `dns` specifica un elenco di resolver DNS da testare.

- Ogni resolver DNS può essere di uno dei tipi seguenti:

    - `system`: usa il resolver di sistema. Va specificato con un oggetto vuoto.

    - `https`: usa un resolver DNS over HTTPS (DoH) crittografato.

    - `tls`: usa un resolver DNS over TLS (DoT) crittografato.

    - `udp`: usa un resolver UDP.

    - `tcp`: usa un resolver TCP.

#### Resolver DNS over HTTPS (DoH)

- `name`: il nome di dominio del server DoH.

- `address`: l'indirizzo host:porta del server DoH. Il valore predefinito è `name`:443.

#### Resolver DNS over TLS (DoT)

- `name`: il nome di dominio del server DoT.

- `address`: l'indirizzo host:porta del server DoT. Il valore predefinito è `name`:853.

#### Resolver UDP

- `address`: l'indirizzo host:porta del resolver UDP.

#### Resolver TCP

- `address`: l'indirizzo host:porta del resolver TCP.

### Configurazione TLS

- Il campo `tls` specifica un elenco di trasporti TLS da testare.

- Ogni trasporto TLS è una stringa che specifica il trasporto da utilizzare.

- Ad esempio, `override:host=cloudflare.net|tlsfrag:1` specifica un trasporto che usa il domain fronting con Cloudflare e la frammentazione TLS. Vedi la [documentazione sulla configurazione](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x/configurl#hdr-Config_Format) per maggiori dettagli.

### Configurazione di fallback

La configurazione di fallback viene utilizzata se nessuna delle strategie senza proxy consente la connessione. Ad esempio, può specificare un server proxy di backup per tentare la connessione dell'utente. L'utilizzo di una strategia di fallback richiede più tempo, perché viene avviata dopo il timeout o l'esito negativo delle altre strategie DNS/TLS.

Le stringhe della configurazione di fallback devono essere:

- Una stringa di configurazione `StreamDialer` valida come definito in [`configurl`](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x/configurl#hdr-Proxy_Protocols).

- Un oggetto di configurazione Psiphon valido come elemento secondario di un campo `psiphon`.

#### Esempio di server Shadowsocks

#### Esempio di server SOCKS5

#### Esempio di configurazione Psiphon

Per utilizzare la rete [Psiphon](https://psiphon.ca/) dovrai:

1. Contattare il team di Psiphon per ottenere una configurazione di accesso alla loro rete. Può essere necessario stipulare un contratto.

2. Aggiungere la configurazione di Psiphon alla sezione `fallback` della configurazione del tuo Smart Dialer. Poiché JSON è compatibile con YAML, puoi copiare e incollare la configurazione di Psiphon direttamente nella sezione `fallback`, in questo modo:

### Come utilizzare lo Smart Dialer

Per utilizzare lo Smart Dialer, crea un oggetto `StrategyFinder` e chiama il metodo `NewDialer`, passando l'elenco dei domini di test e la configurazione YAML.
Il metodo `NewDialer` restituirà un oggetto `transport.StreamDialer` che può essere utilizzato per creare connessioni mediante la strategia trovata. Ad esempio:

Questo è un esempio di base e può essere necessario adattarlo al tuo caso d'uso specifico.
