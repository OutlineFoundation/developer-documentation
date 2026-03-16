---
title: "Smart Dialer Configuration"
sidebar_label: "Smart Dialer Config"
---

Der **Smart Dialer** sucht nach einer Strategie, die DNS und TLS für eine bestimmte Liste von Test-Domains freigibt. Es wird eine Konfiguration benötigt, die mehrere Strategien beschreibt, aus denen ausgewählt werden kann.

## YAML config für den Smart Dialer {#yaml_config_for_the_smart_dialer}

Die config, die der Smart Dialer auswählt, hat das YAML-Format. Hier ein Beispiel:

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

### DNS-Konfiguration {#dns_configuration}

- Das `dns`-Feld führt eine Liste mit zu testenden DNS-Resolvern auf.

- Die DNS-Resolver können die folgenden Typen sein:

    - `system`: Verwenden Sie den System-Resolver. Spezifizieren Sie ihn mit einem leeren Objekt.

    - `https`: Verwenden Sie einen verschlüsselten DNS-over-HTTPS (DoH)-Resolver.

    - `tls`: Verwenden Sie einen verschlüsselten DNS-over-TLS (DoT)-Resolver.

    - `udp`: Verwenden Sie einen UDP-Resolver.

    - `tcp`: Verwenden Sie einen TCP-Resolver.

#### DNS-over-HTTPS-Resolver (DoH) {#dns-over-https_resolver_doh}

```yaml
https:
  name: dns.google
  address: 8.8.8.8
```

- `name`: Der Domainname des DoH-Servers.

- `address`: Der host:port des DoH-Servers. Die Standardeinstellung von `name` ist 443.

#### DNS-over-TLS Resolver (DoT) {#dns-over-tls_resolver_dot}

```yaml
tls:
  name: dns.google
  address: 8.8.8.8
```

- `name`: Der Domainname des DoT-Servers.

- `address`: Der host:port des DoT-Servers. Die Standardeinstellung von `name` ist 853.

#### UDP-Resolver {#udp_resolver}

```yaml
udp:
  address: 8.8.8.8
```

- `address`: Der host:port des UDP-Resolvers.

#### TCP-Resolver {#tcp_resolver}

```yaml
tcp:
  address: 8.8.8.8
```

- `address`: Der host:port des TCP-Resolvers.

### TLS-Konfiguration {#tls_configuration}

- Das `tls`-Feld führt eine Liste mit zu testenden TLS-Transports auf.

- Jeder TLS-Transport ist ein String, der den zu verwendenden Transport angibt.

- Beispielsweise spezifiziert `override:host=cloudflare.net|tlsfrag:1` einen Transport, der Domain Fronting mit Cloudflare und TLS-Fragmentierung verwendet. In der [config-Dokumentation](https://pkg.go.dev/github.com/OutlineFoundation/outline-sdk/x/configurl#hdr-Config_Format) finden Sie weitere Details dazu.

### Fallback-Konfiguration {#fallback_configuration}

Eine Fallback-Konfiguration wird verwendet, wenn keine der proxylosen Strategien eine Verbindung herstellen kann. Sie kann beispielsweise einen Backup-Proxyserver angeben, der versucht, die Verbindung des Nutzers herzustellen. Die Verwendung einer Fallback-Konfiguration verlangsamt den Start, da zuerst die anderen DNS/TLS-Strategien fehlschlagen/eine Zeitüberschreitung verursachen müssen.

Die Fallback-Strings sollten Folgendes sein:

- Ein gültiger `StreamDialer` config-String, wie in [`configurl`](https://pkg.go.dev/github.com/OutlineFoundation/outline-sdk/x/configurl#hdr-Proxy_Protocols) definiert.

- Ein gültiges Psiphon-Konfigurationsobjekt als untergeordnetes Objekt eines `psiphon`-Feldes.

#### Shadowsocks-Server-Beispiel {#shadowsocks_server_example}

```yaml
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

#### SOCKS5-Server-Beispiel {#socks5_server_example}

```yaml
fallback:
  - socks5://[USERINFO]@[HOST]:[PORT]
```

#### Psiphon config-Beispiel {#psiphon_config_example}

Um das [Psiphon](https://psiphon.ca/)-Netzwerk zu nutzen, ist Folgendes nötig:

1. Sie müssen sich an das Psiphon-Team wenden, um eine Konfiguration zu erhalten, die Ihnen den Zugriff auf deren Netzwerk ermöglicht. Dazu kann ein Vertrag erforderlich sein.

2. Fügen Sie die erhaltene Psiphon-Konfiguration in den `fallback`-Abschnitt Ihrer Smart Dialer-Konfiguration ein. Da JSON mit YAML kompatibel ist, können Sie Ihre Psiphon-Konfiguration kopieren und direkt in den `fallback`-Abschnitt einfügen, wie hier gezeigt:

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

### Verwendung des Smart Dialers {#how_to_use_the_smart_dialer}

Um den Smart Dialer zu verwenden, erstellen Sie ein `StrategyFinder`-Objekt. Rufen Sie die `NewDialer`-Methode auf und übergeben Sie die Liste der Testdomains und die YAML-Konfiguration.
Die `NewDialer`-Methode wird einen `transport.StreamDialer` zurückgeben, der zur Erstellung von Verbindungen mit der gefundenen Strategie verwendet werden kann. Beispiel:

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

Dies ist ein einfaches Beispiel, das möglicherweise an Ihren speziellen Anwendungsfall angepasst werden muss.
