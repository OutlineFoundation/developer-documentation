---
title: "Access Key Configuration Reference"
sidebar_label: "Access Key Config"
---

## Tunnel

### TunnelConfig

„Tunnel“ ist das Objekt auf oberster Ebene in einer Outline-Konfiguration, mit dem die Einstellungen für das VPN festgelegt werden.

**Format:** [ExplicitTunnelConfig](#explicittunnelconfig) | [LegacyShadowsocksConfig](#legacyshadowsocksconfig) | [LegacyShadowsocksURI](#legacyshadowsocksuri)

### ExplicitTunnelConfig

**Format:** *struct*

**Felder:**

- `transport` ([TransportConfig](#transportconfig)): die Transportmethode für den Austausch von Paketen mit dem Ziel.

- `error` (*struct*): die Informationen, die Nutzer im Fall eines Dienstfehlers erhalten (z. B. Schlüssel abgelaufen, Kontingent überschritten).

    - `message` (*string*): die Meldung, die Nutzern angezeigt wird.

    - `details` (*string*): die Meldung, die angezeigt wird, wenn ein Nutzer die Details zum Fehler aufruft. Diese Informationen sind hilfreich bei der Fehlerbehebung.

Die Felder `error` und `transport` schließen sich gegenseitig aus.

Fehlerfreies Beispiel:

```yaml
transport:
  $type: tcpudp
  tcp:
    ...  # Stream Dialer for TCP
  udp:
    ...  # Packet Listener for UDP
```

Beispiel mit Fehler:

```yaml
error:
  message: Quota exceeded
  details: Used 100GB out of 100GB
```

## Transport

### TransportConfig

Hiermit wird angegeben, wie Pakete mit dem Ziel ausgetauscht werden.

**Format:** [Interface](#interface)

Unterstützte Schnittstellentypen:

- `tcpudp`: [TCPUDPConfig](#tcpudpconfig)

### TCPUDPConfig

Mit TCPUDPConfig lassen sich separate TCP- und UDP-Strategien festlegen.

**Format:** *struct*

**Felder:**

- `tcp` ([DialerConfig](#dialerconfig)): der Stream-Dialer, der für TCP-Verbindungen verwendet werden soll.

- `udp` ([PacketListenerConfig](#packetlistenerconfig)): der Packet-Listener, der für UDP-Pakete verwendet werden soll.

Beispiel für das Senden von TCP und UDP an verschiedene Endpunkte:

```yaml
tcp:
  $type: shadowsocks
  endpoint: ss.example.com:80
  <<: &cipher
    cipher: chacha20-ietf-poly1305
    secret: SECRET
  prefix: "POST "

udp:
  $type: shadowsocks
  endpoint: ss.example.com:53
  <<: *cipher
```

## Endpunkte

Hiermit werden Verbindungen zu bestimmten Endpunkten hergestellt. Diese Option ist besser als Dialer, da sie endpunktspezifische Optimierungen ermöglicht. Es gibt Stream-Endpunkte und Packet-Endpunkte.

### EndpointConfig

**Format:** *string* | [Interface](#interface)

Der Endpunkt mit dem Format *string* fungiert als host:port-Adresse des ausgewählten Endpunkts. Die Verbindung wird über den Standard-Dialer hergestellt.

Unterstützte Interface-Typen für Stream-Endpunkte und Packet-Endpunkte:

- `dial`: [DialEndpointConfig](#dialendpointconfig)

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `websocket`: [WebsocketEndpointConfig](#websocketendpointconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

### DialEndpointConfig

Stellt Verbindungen her, indem eine feste Adresse gewählt wird. Hierfür kann ein Dialer genutzt werden, was eine Kombination von Strategien ermöglicht.

**Format:** *struct*

**Felder:**

- `address` (*string*): die zu wählende Adresse des Endpunkts.

- `dialer` ([DialerConfig](#dialerconfig)): der zu verwendende Dialer.

### WebsocketEndpointConfig

Leitet Stream- und Paketverbindungen über WebSockets an einen Endpunkt weiter.

Bei Stream-Verbindungen wird jeder Schreibvorgang in eine WebSocket-Nachricht umgewandelt. Bei Paketverbindungen wird jedes Paket in eine WebSocket-Nachricht umgewandelt.

**Format:** *struct*

**Felder:**

- `url` (*string*): die URL für den WebSocket-Endpunkt. Das Schema muss `https` oder `wss` für verschlüsselte WebSocket-Verbindungen über TLS und `http` oder `ws` für unverschlüsselte Verbindungen sein.

- `endpoint` ([EndpointConfig](#endpointconfig)): der Webserver-Endpunkt, mit dem die Verbindung hergestellt werden soll. Ist dieser nicht erreichbar, wird die in der URL angegebene Adresse für die Verbindung verwendet.

## Dialer

Dialer stellen Verbindungen mithilfe einer gegebenen Endpunktadresse her. Es gibt Stream-Dialer und Packet-Dialer.

### DialerConfig

**Format:** *null* | [Interface](#interface)

*null* (absent) entspricht dem Standard-Dialer, der direkte TCP-Verbindungen (Stream) und direkte UDP-Verbindungen (Packets) verwendet.

Unterstützte Interface-Typen für Stream-Dialer und Packet-Dialer:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

## Packet-Listener

Ein Packet-Listener erstellt eine nicht gebundene Paketverbindung, die verwendet werden kann, um Pakete an verschiedene Ziele zu senden.

### PacketListenerConfig

**Format:** *null* | [Interface](#interface)

*null* (absent) entspricht dem standardmäßigen Packet-Listener. Dies ist ein UDP-Packet-Listener.

Unterstützte Schnittstellentypen:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksPacketListenerConfig](#shadowsocksconfig)

## Strategien

### Shadowsocks

#### LegacyShadowsocksConfig

LegacyShadowsocksConfig repräsentiert einen Tunnel, der Shadowsocks als Transportmethode verwendet. Er implementiert dieses alte Format, um die Abwärtskompatibilität sicherzustellen.

**Format:** *struct*

**Felder:**

- `server` (*string*): der Host, mit dem eine Verbindung hergestellt werden soll.

- `server_port` (*number*): die Portnummer für die Verbindung.

- `method` (*string*): die zu verwendende [AEAD-Chiffre](https://shadowsocks.org/doc/aead.html#aead-ciphers).

- `password` (*string*): wird verwendet, um den Verschlüsselungsschlüssel zu generieren.

- `prefix` (*string*): die zu verwendende [Vorwahltarnung](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/).
Unterstützt auf Stream- und Packet-Verbindungen.

Beispiel:

```yaml
server: example.com
server_port: 4321
method: chacha20-ietf-poly1305
password: SECRET
prefix: "POST "
```

#### LegacyShadowsocksURI

LegacyShadowsocksURI repräsentiert einen Tunnel, der Shadowsocks als Transportmethode verwendet.
Er implementiert das alte URL-Format, um die Abwärtskompatibilität sicherzustellen.

**Format:** *string*

Siehe [Legacy Shadowsocks URI-Format](https://shadowsocks.org/doc/configs.html#uri-and-qr-code) und [SIP002 URI-Schema](https://shadowsocks.org/doc/sip002.html). Wir unterstützen keine Plug-ins.

Beispiel:

```yaml
ss://chacha20-ietf-poly1305:SECRET@example.com:443?prefix=POST%20
```

#### ShadowsocksConfig

ShadowsocksConfig kann einen Stream-Dialer oder einen Packet-Dialer sowie einen Packet-Listener repräsentieren, die Shadowsocks verwenden.

**Format:** *struct*

**Felder:**

- `endpoint` ([EndpointConfig](#endpointconfig)): der Shadowsocks-Endpunkt, mit dem die Verbindung hergestellt werden soll.

- `cipher` (*string*): die zu verwendende [AEAD-Chiffre](https://shadowsocks.org/doc/aead.html#aead-ciphers).

- `secret` (*string*): wird verwendet, um den Verschlüsselungsschlüssel zu generieren.

- `prefix` (*string*, optional): die zu verwendende [Vorwahltarnung](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/).
Unterstützt auf Stream- und Packet-Verbindungen.

Beispiel:

```yaml
endpoint: example.com:80
cipher: chacha20-ietf-poly1305
secret: SECRET
prefix: "POST "
```

## Meta-Definitionen

### FirstSupportedConfig

Nutzt die erste Konfiguration, die von der Anwendung unterstützt wird. Dies ist eine Möglichkeit, neue Konfigurationen zu unterstützen und gleichzeitig die Abwärtskompatibilität mit alten Konfigurationen beizubehalten.

**Format:** *struct*

**Felder:**

- `options` ([EndpointConfig[]](#endpointconfig) | [DialerConfig[]](#dialerconfig) | [PacketListenerConfig[]](#packetlistenerconfig)): Liste der zu berücksichtigenden Optionen

Beispiel:

```yaml
options:
  - $type: websocket
    url: wss://example.com/SECRET_PATH
  - ss.example.com:4321
```

### Interface

Interfaces bieten die Möglichkeit, eine von mehreren Implementierungen auszuwählen. Mit dem Feld `$type` wird der Typ angegeben, den die Konfiguration repräsentiert.

Beispiel:

```yaml
$type: shadowsocks
endpoint: example.com:4321
cipher: chacha20-ietf-poly1305
secret: SECRET
```
