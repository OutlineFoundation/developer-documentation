---
title: "Smart Dialer-configuratie"
sidebar_label: "Smart Dialer-configuratie"
---

De **Smart Dialer** zoekt naar een strategie waarmee DNS en TLS voor een bepaalde lijst testdomeinen wordt gedeblokkeerd. Je hebt hiervoor een configuratie nodig waarin meerdere strategieën worden beschreven om uit te kiezen.

## YAML-configuratie voor de Smart Dialer {#yaml_config_for_the_smart_dialer}

De configuratie die de Smart Dialer gebruikt, staat in de YAML-indeling. Een voorbeeld:

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

### DNS-configuratie {#dns_configuration}

- In het veld `dns` staat een lijst met DNS-resolvers om te testen.

- Elke DNS-resolver kan een van de volgende typen zijn:

    - `system`: Gebruik de systeemresolver. Specificeer met een leeg object.

    - `https`: Gebruik een versleutelde DNS-over-HTTPS-resolver (DoH).

    - `tls`: Gebruik een versleutelde DNS-over-TLS-resolver (DoT).

    - `udp`: Gebruik een UDP-resolver.

    - `tcp`: Gebruik een TCP-resolver.

#### DNS-over-HTTPS-resolver (DoH) {#dns-over-https_resolver_doh}

```yaml
https:
  name: dns.google
  address: 8.8.8.8
```

- `name`: De domeinnaam van de DoH-server.

- `address`: De host:port van de DoH-server. De standaardwaarde is `name`:443.

#### DNS-over-TLS-resolver (DoT) {#dns-over-tls_resolver_dot}

```yaml
tls:
  name: dns.google
  address: 8.8.8.8
```

- `name`: De domeinnaam van de DoT-server.

- `address`: De host:port van de DoT-server. De standaardwaarde is `name`:853.

#### UDP-resolver {#udp_resolver}

```yaml
udp:
  address: 8.8.8.8
```

- `address`: De host:port van de UDP-resolver.

#### TCP-resolver {#tcp_resolver}

```yaml
tcp:
  address: 8.8.8.8
```

- `address`: De host:port van de TCP-resolver.

### TLS-configuratie {#tls_configuration}

- In het veld `tls` staat een lijst met TLS-transporten om te testen.

- Elk TLS-transport is een tekenreeks die aangeeft welk transport moet worden gebruikt.

- `override:host=cloudflare.net|tlsfrag:1` geeft bijvoorbeeld een transport aan dat domain fronting gebruikt met Cloudflare en TLS-fragmentatie. In de [configuratiedocumentatie](https://pkg.go.dev/github.com/OutlineFoundation/outline-sdk/x/configurl#hdr-Config_Format) vind je meer informatie.

### Reserveconfiguratie {#fallback_configuration}

Een reserveconfiguratie wordt gebruikt als via geen van de proxyloze strategieën verbinding kan worden gemaakt. Je kunt er bijvoorbeeld een back-upproxyserver in opgeven om de verbinding van de gebruiker mee te proberen. Als je een reserveconfiguratie gebruikt, start deze langzamer, omdat de andere DNS-/TLS-strategieën eerst moeten mislukken of er een time-out voor moet optreden.

De reservetekenreeksen moeten de volgende zijn:

- Een geldige `StreamDialer`-configuratietekenreeks zoals beschreven in [`configurl`](https://pkg.go.dev/github.com/OutlineFoundation/outline-sdk/x/configurl#hdr-Proxy_Protocols).

- Een geldig Psiphon-configuratieobject als onderliggend object van een `psiphon`-veld.

#### Voorbeeld voor Shadowsocks-server {#shadowsocks_server_example}

```yaml
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

#### Voorbeeld voor SOCKS5-server {#socks5_server_example}

```yaml
fallback:
  - socks5://[USERINFO]@[HOST]:[PORT]
```

#### Voorbeeld van Psiphon-configuratie {#psiphon_config_example}

Als je het [Psiphon](https://psiphon.ca/)-netwerk wilt gebruiken, moet je het volgende doen:

1. Vraag het Psiphon-team om een configuratie waarmee je toegang krijgt tot hun netwerk. Je moet hiervoor misschien een contract aangaan.

2. Voeg de Psiphon-configuratie die je hebt gekregen toe aan het gedeelte `fallback` van je Smart Dialer-configuratie. Json is compatibel met YAML, dus je kunt je Psiphon-configuratie rechtstreeks in het gedeelte `fallback` kopiëren en plakken, zoals hier:

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

### De Smart Dialer gebruiken {#how_to_use_the_smart_dialer}

Als je de Smart Dialer wilt gebruiken, maak je een `StrategyFinder`-object en roep je de methode `NewDialer` aan. Geef hierbij de lijst met testdomeinen en de YAML-configuratie mee.
Via de methode `NewDialer` krijg je een `transport.StreamDialer` waarmee je verbinding kunt maken via de gevonden strategie. Bijvoorbeeld:

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

Dit is een algemeen voorbeeld, je moet het misschien aanpassen voor jouw specifieke use case.
