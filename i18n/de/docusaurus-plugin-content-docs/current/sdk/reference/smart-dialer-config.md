---
title: "Smart Dialer Configuration"
sidebar_label: "Smart Dialer Config"
---

Der **Smart Dialer** sucht nach einer Strategie, die DNS und TLS für eine bestimmte Liste von Test-Domains freigibt. Es wird eine Konfiguration benötigt, die mehrere Strategien beschreibt, aus denen ausgewählt werden kann.

## YAML config für den Smart Dialer

Die config, die der Smart Dialer auswählt, hat das YAML-Format. Hier ein Beispiel:

### DNS-Konfiguration

- Das `dns`-Feld führt eine Liste mit zu testenden DNS-Resolvern auf.

- Die DNS-Resolver können die folgenden Typen sein:

    - `system`: Verwenden Sie den System-Resolver. Spezifizieren Sie ihn mit einem leeren Objekt.

    - `https`: Verwenden Sie einen verschlüsselten DNS-over-HTTPS (DoH)-Resolver.

    - `tls`: Verwenden Sie einen verschlüsselten DNS-over-TLS (DoT)-Resolver.

    - `udp`: Verwenden Sie einen UDP-Resolver.

    - `tcp`: Verwenden Sie einen TCP-Resolver.

#### DNS-over-HTTPS-Resolver (DoH)

- `name`: Der Domainname des DoH-Servers.

- `address`: Der host:port des DoH-Servers. Die Standardeinstellung von `name` ist 443.

#### DNS-over-TLS Resolver (DoT)

- `name`: Der Domainname des DoT-Servers.

- `address`: Der host:port des DoT-Servers. Die Standardeinstellung von `name` ist 853.

#### UDP-Resolver

- `address`: Der host:port des UDP-Resolvers.

#### TCP-Resolver

- `address`: Der host:port des TCP-Resolvers.

### TLS-Konfiguration

- Das `tls`-Feld führt eine Liste mit zu testenden TLS-Transports auf.

- Jeder TLS-Transport ist ein String, der den zu verwendenden Transport angibt.

- Beispielsweise spezifiziert `override:host=cloudflare.net|tlsfrag:1` einen Transport, der Domain Fronting mit Cloudflare und TLS-Fragmentierung verwendet. In der [config-Dokumentation](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x/configurl#hdr-Config_Format) finden Sie weitere Details dazu.

### Fallback-Konfiguration

Eine Fallback-Konfiguration wird verwendet, wenn keine der proxylosen Strategien eine Verbindung herstellen kann. Sie kann beispielsweise einen Backup-Proxyserver angeben, der versucht, die Verbindung des Nutzers herzustellen. Die Verwendung einer Fallback-Konfiguration verlangsamt den Start, da zuerst die anderen DNS/TLS-Strategien fehlschlagen/eine Zeitüberschreitung verursachen müssen.

Die Fallback-Strings sollten Folgendes sein:

- Ein gültiger `StreamDialer` config-String, wie in [`configurl`](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x/configurl#hdr-Proxy_Protocols) definiert.

- Ein gültiges Psiphon-Konfigurationsobjekt als untergeordnetes Objekt eines `psiphon`-Feldes.

#### Shadowsocks-Server-Beispiel

#### SOCKS5-Server-Beispiel

#### Psiphon config-Beispiel

Um das [Psiphon](https://psiphon.ca/)-Netzwerk zu nutzen, ist Folgendes nötig:

1. Sie müssen sich an das Psiphon-Team wenden, um eine Konfiguration zu erhalten, die Ihnen den Zugriff auf deren Netzwerk ermöglicht. Dazu kann ein Vertrag erforderlich sein.

2. Fügen Sie die erhaltene Psiphon-Konfiguration in den `fallback`-Abschnitt Ihrer Smart Dialer-Konfiguration ein. Da JSON mit YAML kompatibel ist, können Sie Ihre Psiphon-Konfiguration kopieren und direkt in den `fallback`-Abschnitt einfügen, wie hier gezeigt:

### Verwendung des Smart Dialers

Um den Smart Dialer zu verwenden, erstellen Sie ein `StrategyFinder`-Objekt. Rufen Sie die `NewDialer`-Methode auf und übergeben Sie die Liste der Testdomains und die YAML-Konfiguration.
Die `NewDialer`-Methode wird einen `transport.StreamDialer` zurückgeben, der zur Erstellung von Verbindungen mit der gefundenen Strategie verwendet werden kann. Beispiel:

Dies ist ein einfaches Beispiel, das möglicherweise an Ihren speziellen Anwendungsfall angepasst werden muss.
