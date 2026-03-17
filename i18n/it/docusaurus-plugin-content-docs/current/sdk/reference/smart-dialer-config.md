---
title: "Configura lo Smart Dialer"
sidebar_label: "Configura lo Smart Dialer"
---

Lo **Smart Dialer** cerca una strategia per sbloccare il DNS e il TLS per un elenco specificato di domini di test. Richiede una configurazione che descriva più strategie tra cui scegliere.

## Configurazione YAML per lo Smart Dialer {#yaml_config_for_the_smart_dialer}

La configurazione per lo Smart Dialer deve essere in formato YAML. Ecco un esempio:

```yaml
dns:
  - system: {}
  - https:
      name: 8.8.8.8
  - https:
      name: 9.9.9.9
tls:
  - ""
  - split:2
  - tlsfrag:1

fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

### Configurazione DNS {#dns_configuration}

- Il campo `dns` specifica un elenco di resolver DNS da testare.

- Ogni resolver DNS può essere di uno dei tipi seguenti:

    - `system`: usa il resolver di sistema. Va specificato con un oggetto vuoto.

    - `https`: usa un resolver DNS over HTTPS (DoH) crittografato.

    - `tls`: usa un resolver DNS over TLS (DoT) crittografato.

    - `udp`: usa un resolver UDP.

    - `tcp`: usa un resolver TCP.

#### Resolver DNS over HTTPS (DoH) {#dns-over-https_resolver_doh}

```yaml
https:
  name: dns.google
  address: 8.8.8.8
```

- `name`: il nome di dominio del server DoH.

- `address`: l'indirizzo host:porta del server DoH. Il valore predefinito è `name`:443.

#### Resolver DNS over TLS (DoT) {#dns-over-tls_resolver_dot}

```yaml
tls:
  name: dns.google
  address: 8.8.8.8
```

- `name`: il nome di dominio del server DoT.

- `address`: l'indirizzo host:porta del server DoT. Il valore predefinito è `name`:853.

#### Resolver UDP {#udp_resolver}

```yaml
udp:
  address: 8.8.8.8
```

- `address`: l'indirizzo host:porta del resolver UDP.

#### Resolver TCP {#tcp_resolver}

```yaml
tcp:
  address: 8.8.8.8
```

- `address`: l'indirizzo host:porta del resolver TCP.

### Configurazione TLS {#tls_configuration}

- Il campo `tls` specifica un elenco di trasporti TLS da testare.

- Ogni trasporto TLS è una stringa che specifica il trasporto da utilizzare.

- Ad esempio, `override:host=cloudflare.net|tlsfrag:1` specifica un trasporto che usa il domain fronting con Cloudflare e la frammentazione TLS. Vedi la [documentazione sulla configurazione](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#hdr-Config_Format) per maggiori dettagli.

### Configurazione di fallback {#fallback_configuration}

La configurazione di fallback viene utilizzata se nessuna delle strategie senza proxy consente la connessione. Ad esempio, può specificare un server proxy di backup per tentare la connessione dell'utente. L'utilizzo di una strategia di fallback richiede più tempo, perché viene avviata dopo il timeout o l'esito negativo delle altre strategie DNS/TLS.

Le stringhe della configurazione di fallback devono essere:

- Una stringa di configurazione `StreamDialer` valida come definito in [`configurl`](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#hdr-Proxy_Protocols).

- Un oggetto di configurazione Psiphon valido come elemento secondario di un campo `psiphon`.

#### Esempio di server Shadowsocks {#shadowsocks_server_example}

```yaml
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

#### Esempio di server SOCKS5 {#socks5_server_example}

```yaml
fallback:
  - socks5://[USERINFO]@[HOST]:[PORT]
```

#### Esempio di configurazione Psiphon {#psiphon_config_example}

Per utilizzare la rete [Psiphon](https://psiphon.ca/) dovrai:

1. Contattare il team di Psiphon per ottenere una configurazione di accesso alla loro rete. Può essere necessario stipulare un contratto.

2. Aggiungere la configurazione di Psiphon alla sezione `fallback` della configurazione del tuo Smart Dialer. Poiché JSON è compatibile con YAML, puoi copiare e incollare la configurazione di Psiphon direttamente nella sezione `fallback`, in questo modo:

```yaml
fallback:
  - psiphon: {
      "PropagationChannelId": "FFFFFFFFFFFFFFFF",
      "SponsorId": "FFFFFFFFFFFFFFFF",
      "DisableLocalSocksProxy" : true,
      "DisableLocalHTTPProxy" : true,
      ...
    }
```


:::note
l'utilizzo del codebase di Psiphon è concesso ai sensi della licenza GPL, che può imporre limitazioni sul tuo codice. Valuta l'opportunità di richiedere una licenza speciale.
:::

### Come utilizzare lo Smart Dialer {#how_to_use_the_smart_dialer}

Per utilizzare lo Smart Dialer, crea un oggetto `StrategyFinder` e chiama il metodo `NewDialer`, passando l'elenco dei domini di test e la configurazione YAML.
Il metodo `NewDialer` restituirà un oggetto `transport.StreamDialer` che può essere utilizzato per creare connessioni mediante la strategia trovata. Ad esempio:

```go
finder := &smart.StrategyFinder{
    TestTimeout:  5 * time.Second,
    LogWriter:   os.Stdout,
    StreamDialer: &transport.TCPDialer{},
    PacketDialer: &transport.UDPDialer{},
}

configBytes := []byte(`
dns:
  - system: {}
  - https:
      name: 8.8.8.8
  - https:
      name: 9.9.9.9
tls:
  - ""
  - split:2
  - tlsfrag:1
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
`)

dialer, err := finder.NewDialer(
  context.Background(),
  []string{"www.google.com"},
  configBytes
)
if err != nil {
    // Handle error.
}

// Use dialer to create connections.
```

Questo è un esempio di base e può essere necessario adattarlo al tuo caso d'uso specifico.
