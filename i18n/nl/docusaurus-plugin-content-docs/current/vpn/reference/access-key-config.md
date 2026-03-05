---
title: "Access Key Configuration Reference"
sidebar_label: "Access Key Config"
---

## Tunnels

### TunnelConfig

Tunnel is het object op het hoogste niveau in een Outline-configuratie. Hiermee bepaal je hoe de VPN wordt ingesteld.

**Indeling:** [ExplicitTunnelConfig](#explicittunnelconfig) |
[LegacyShadowsocksConfig](#legacyshadowsocksconfig) |
[LegacyShadowsocksURI](#legacyshadowsocksuri)

### ExplicitTunnelConfig

**Indeling:** *struct*

**Velden:**

- `transport` ([TransportConfig](#transportconfig)): Het transport waarmee pakketten moeten worden uitgewisseld met de doelbestemming.

- `error` (*struct*): Informatie om te communiceren met de gebruiker als er een servicefout is (bijv. verlopen sleutel, quotum bereikt).

    - `message` (*string*): Gebruiksvriendelijk bericht om te tonen aan de gebruiker.

    - `details` (*string*): Bericht om te tonen als de gebruiker de details van de fout opent. Nuttig voor probleemoplossing.

De velden `error` en `transport` sluiten elkaar uit.

Correct voorbeeld:

```yaml
transport:
  $type: tcpudp
  tcp:
    ...  # Stream Dialer for TCP
  udp:
    ...  # Packet Listener for UDP
```

Foutief voorbeeld:

```yaml
error:
  message: Quota exceeded
  details: Used 100GB out of 100GB
```

## Transporten

### TransportConfig

Hiermee bepaal je hoe pakketten moeten worden uitgewisseld met de doelbestemming.

**Indeling:** [Interface](#interface)

Ondersteunde Interface-typen:

- `tcpudp`: [TCPUDPConfig](#tcpudpconfig)

### TCPUDPConfig

Met TCPUDPConfig kun je aparte TCP- en UDP-strategieën instellen.

**Indeling:** *struct*

**Velden:**

- `tcp` ([DialerConfig](#dialerconfig)): De Stream Dialer om te gebruiken voor TCP-verbindingen.

- `udp` ([PacketListenerConfig](#packetlistenerconfig)): De Packet Listener om te gebruiken voor UDP-pakketten.

Voorbeeld voor het sturen van TCP en UDP naar verschillende eindpunten:

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

## Endpoints

Met Endpoints maak je verbinding met een vast eindpunt. Dit heeft de voorkeur over Dialers omdat je hiermee eindpuntspecifieke optimalisaties kunt doorvoeren. Er zijn Stream en Packet Endpoints.

### EndpointConfig

**Indeling:** *string* | [Interface](#interface)

De Endpoint *string* is het host:poort-adres van het geselecteerde eindpunt. De verbinding wordt gemaakt met de standaard Dialer.

Ondersteunde Interface-typen voor Stream en Packet Endpoints:

- `dial`: [DialEndpointConfig](#dialendpointconfig)

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `websocket`: [WebsocketEndpointConfig](#websocketendpointconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

### DialEndpointConfig

Hiermee maak je verbinding door een vast adres aan te roepen. Je kunt hier een dialer aan toevoegen, zodat je verschillende strategieën samen kunt gebruiken.

**Indeling:** *struct*

**Velden:**

- `address` (*string*): Het adres van het eindpunt om aan te roepen.

- `dialer` ([DialerConfig](#dialerconfig)): De dialer om het adres mee aan te roepen.

### WebsocketEndpointConfig

Hiermee worden stream- en pakketverbindingen getunneld naar een eindpunt via WebSockets.

Voor streamverbindingen wordt elke write veranderd in een WebSocket-bericht. Voor pakketverbindingen wordt elk pakket veranderd in een WebSocket-bericht.

**Indeling:** *struct*

**Velden:**

- `url` (*string*): De URL van het WebSocket-eindpunt. Het schema moet `https` of `wss` zijn voor WebSocket over TLS, en `http` of `ws` zijn voor WebSocket in niet-versleutelde tekst.

- `endpoint` ([EndpointConfig](#endpointconfig)): Het eindpunt van de webserver waarmee verbinding moet worden gemaakt. Als je hier niets invoert, wordt er verbinding gemaakt met het adres dat je opgeeft in de URL.

## Dialers

Dialers maken verbinding met een eindpuntadres. Er zijn Stream en Packet Dialers.

### DialerConfig

**Indeling:** *null* | [Interface](#interface)

De Dialer *null* (afwezig) is de standaard Dialer, die directe TCP-verbindingen gebruikt voor streams en directe UDP-verbindingen gebruikt voor pakketten.

Ondersteunde Interface-typen voor Stream en Packet Dialers:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

## Packet Listeners

Een Packet Listener maakt een ongebonden pakketverbinding waarmee je pakketten kunt sturen naar meerdere bestemmingen.

### PacketListenerConfig

**Indeling:** *null* | [Interface](#interface)

De Packet Listener *null* (afwezig) is de standaard Packet Listener. Dit is een UDP Packet Listener.

Ondersteunde Interface-typen:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksPacketListenerConfig](#shadowsocksconfig)

## Strategieën

### Shadowsocks

#### LegacyShadowsocksConfig

LegacyShadowsocksConfig vertegenwoordigt een tunnel die Shadowsocks gebruikt voor het transport. Hiermee implementeer je de verouderde indeling voor compatibiliteit met eerdere versies.

**Indeling:** *struct*

**Velden:**

- `server` (*string*): De host om verbinding mee te maken.

- `server_port` (*number*): Het poortnummer om verbinding mee te maken.

- `method` (*string*): De [AEAD-codering](https://shadowsocks.org/doc/aead.html#aead-ciphers) om te gebruiken.

- `password` (*string*): Gebruikt om de versleutelingssleutel mee te maken.

- `prefix` (*string*): De [voorvoegselvermomming](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/) om te gebruiken.
Wordt ondersteund voor stream- en pakketverbindingen.

Voorbeeld:

```yaml
server: example.com
server_port: 4321
method: chacha20-ietf-poly1305
password: SECRET
prefix: "POST "
```

#### LegacyShadowsocksURI

LegacyShadowsocksURI vertegenwoordigt een tunnel die Shadowsocks gebruikt voor het transport.
Hiermee implementeer je de verouderde URL-indeling voor compatibiliteit met eerdere versies.

**Indeling:** *string*

Ga naar [Verouderde URI-indeling voor Shadowsocks](https://shadowsocks.org/doc/configs.html#uri-and-qr-code) en [SIP002 URI-schema](https://shadowsocks.org/doc/sip002.html). Plug-ins worden niet ondersteund.

Voorbeeld:

```yaml
ss://chacha20-ietf-poly1305:SECRET@example.com:443?prefix=POST%20
```

#### ShadowsocksConfig

ShadowsocksConfig kan een Stream en Packet Dialer vertegenwoordigen, of een Packet Listener die Shadowsocks gebruikt.

**Indeling:** *struct*

**Velden:**

- `endpoint` ([EndpointConfig](#endpointconfig)): Het Shadowsocks-eindpunt waarmee verbinding moet worden gemaakt.

- `cipher` (*string*): De [AEAD-codering](https://shadowsocks.org/doc/aead.html#aead-ciphers) om te gebruiken.

- `secret` (*string*): Gebruikt om de versleutelingssleutel mee te maken.

- `prefix` (*string*, optioneel): De [voorvoegselvermomming](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/) om te gebruiken.
Wordt ondersteund voor stream- en pakketverbindingen.

Voorbeeld:

```yaml
endpoint: example.com:80
cipher: chacha20-ietf-poly1305
secret: SECRET
prefix: "POST "
```

## Metadefinities

### FirstSupportedConfig

Gebruikt de eerste configuratie die wordt ondersteund door de app. Dit is een manier om nieuwe configuraties te gebruiken en compatibiliteit te behouden met eerdere configuraties.

**Indeling:** *struct*

**Velden:**

- `options` ([EndpointConfig[]](#endpointconfig) |
[DialerConfig[]](#dialerconfig) |
[PacketListenerConfig[]](#packetlistenerconfig)): Lijst met opties om te overwegen.

Voorbeeld:

```yaml
options:
  - $type: websocket
    url: wss://example.com/SECRET_PATH
  - ss.example.com:4321
```

### Interface

Met Interfaces kun je een van meerdere implementaties kiezen. In het veld `$type` voer je het type in dat die configuratie vertegenwoordigt.

Voorbeeld:

```yaml
$type: shadowsocks
endpoint: example.com:4321
cipher: chacha20-ietf-poly1305
secret: SECRET
```
