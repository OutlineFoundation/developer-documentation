---
title: "Access Key Configuration Reference"
sidebar_label: "Access Key Config"
---

## Tunnel {#tunnels}

### TunnelConfig {#tunnelconfig}

Tunnel è l'oggetto di livello superiore in una configurazione Outline. Specifica come deve essere configurata la VPN.

**Formato:** [ExplicitTunnelConfig](#explicittunnelconfig) |
[LegacyShadowsocksConfig](#legacyshadowsocksconfig) |
[LegacyShadowsocksURI](#legacyshadowsocksuri)

### ExplicitTunnelConfig {#explicittunnelconfig}

**Formato:** *struct*

**Campi:**

- `transport` ([TransportConfig](#transportconfig)): il Transport da utilizzare per scambiare i pacchetti con la destinazione target.

- `error` (*struct*): informazioni da comunicare all'utente in caso di errore del servizio (ad es. chiave scaduta, quota esaurita).

    - `message` (*string*): messaggio semplice da mostrare all'utente.

    - `details` (*string*): messaggio da mostrare quando l'utente apre i dettagli dell'errore.
 Utile per la risoluzione dei problemi.

I campi `error` e `transport` si escludono a vicenda.

Esempio riuscito:

```yaml
transport:
  $type: tcpudp
  tcp:
    ...  # Stream Dialer for TCP
  udp:
    ...  # Packet Listener for UDP
```

Esempio di errore:

```yaml
error:
  message: Quota exceeded
  details: Used 100GB out of 100GB
```

## Transport {#transports}

### TransportConfig {#transportconfig}

Specifica come i pacchetti devono essere scambiati con la destinazione target.

**Formato:** [Interface](#interface)

Tipi di Interface supportati:

- `tcpudp`: [TCPUDPConfig](#tcpudpconfig)

### TCPUDPConfig {#tcpudpconfig}

TCPUDPConfig consente di impostare strategie TCP e UDP separate.

**Formato:** *struct*

**Campi:**

- `tcp` ([DialerConfig](#dialerconfig)): lo Stream Dialer da utilizzare per le connessioni TCP.

- `udp` ([PacketListenerConfig](#packetlistenerconfig)): il Packet Listener da utilizzare per i pacchetti UDP.

Esempio di invio di TCP e UDP a endpoint diversi:

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

## Endpoint {#endpoints}

Gli endpoint stabiliscono connessioni con un endpoint fisso. Sono preferibili ai dialer poiché consentono ottimizzazioni specifiche per gli endpoint. Esistono Stream Endpoint e Packet Endpoint.

### EndpointConfig {#endpointconfig}

**Formato:** *string* | [Interface](#interface)

L'endpoint *string* è l'indirizzo host:porta dell'endpoint selezionato. La connessione viene stabilita tramite il dialer predefinito.

Tipi di Interface supportati per Stream Endpoint e Packet Endpoint:

- `dial`: [DialEndpointConfig](#dialendpointconfig)

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `websocket`: [WebsocketEndpointConfig](#websocketendpointconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

### DialEndpointConfig {#dialendpointconfig}

Stabilisce connessioni componendo un indirizzo fisso. Può essere dotato di un dialer, che consente la composizione delle strategie.

**Formato:** *struct*

**Campi:**

- `address` (*string*): l'indirizzo dell'endpoint da comporre.

- `dialer` ([DialerConfig](#dialerconfig)): il dialer da utilizzare per comporre l'indirizzo.

### WebsocketEndpointConfig {#websocketendpointconfig}

Connessioni Stream e Packet dei Tunnel verso un endpoint tramite Websocket.

Per le connessioni Stream, ogni scrittura viene trasformata in un messaggio Websocket. Per le connessioni Packet, ogni pacchetto viene convertito in un messaggio Websocket.

**Formato:** *struct*

**Campi:**

- `url` (*string*): l'URL per l'endpoint Websocket. Lo schema deve essere `https` o `wss` per Websocket su TLS e `http` o `ws` per Websocket con testo non crittografato.

- `endpoint` ([EndpointConfig](#endpointconfig)): l'endpoint del server web a cui connettersi. Se assente, si connette all'indirizzo specificato nell'URL.

## Dialer {#dialers}

I dialer stabiliscono connessioni in base all'indirizzo di un endpoint. Esistono Stream Dialer e Packet Dialer.

### DialerConfig {#dialerconfig}

**Formato:** *null* | [Interface](#interface)

Il dialer *null* (assente) indica il dialer predefinito, che utilizza connessioni TCP dirette per Stream e connessioni UDP dirette per Packet.

Tipi di Interface supportati per Stream Dialer e Packet Dialer:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

## Packet Listener {#packet_listeners}

Un Packet Listener stabilisce una connessione Packet illimitata che può essere utilizzata per inviare pacchetti a più destinazioni.

### PacketListenerConfig {#packetlistenerconfig}

**Formato:** *null* | [Interface](#interface)

Il Packet Listener *null* (assente) indica il Packet Listener predefinito, che è un Packet Listener UDP.

Tipi di Interface supportati:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksPacketListenerConfig](#shadowsocksconfig)

## Strategie {#strategies}

### Shadowsocks {#shadowsocks}

#### LegacyShadowsocksConfig {#legacyshadowsocksconfig}

LegacyShadowsocksConfig rappresenta un Tunnel che utilizza Shadowsocks come Transport. Implementa il formato legacy per la compatibilità con le versioni precedenti.

**Formato:** *struct*

**Campi:**

- `server` (*string*): l'host a cui connettersi.

- `server_port` (*number*): il numero di porta a cui connettersi.

- `method` (*string*): il [cifrario di crittografia autenticata con dati associati](https://shadowsocks.org/doc/aead.html#aead-ciphers) da utilizzare.

- `password` (*string*): utilizzato per generare la chiave di crittografia.

- `prefix` (*string*): il [mascheramento del prefisso](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/) da utilizzare.
Supportato sulle connessioni Stream e Packet.

Esempio:

```yaml
server: example.com
server_port: 4321
method: chacha20-ietf-poly1305
password: SECRET
prefix: "POST "
```

#### LegacyShadowsocksURI {#legacyshadowsocksuri}

LegacyShadowsocksURI rappresenta un Tunnel che utilizza Shadowsocks come Transport.
Implementa il formato URL legacy per la compatibilità con le versioni precedenti.

**Formato:** *string*

Consulta [Formato LegacyShadowsocksURI](https://shadowsocks.org/doc/configs.html#uri-and-qr-code) e [Schema URI SIP002](https://shadowsocks.org/doc/sip002.html). Non supportiamo i plug-in.

Esempio:

```yaml
ss://chacha20-ietf-poly1305:SECRET@example.com:443?prefix=POST%20
```

#### ShadowsocksConfig {#shadowsocksconfig}

ShadowsocksConfig può rappresentare uno Stream Dialer o un Packet Dialer, così come un Packet Listener che utilizza Shadowsocks.

**Formato:** *struct*

**Campi:**

- `endpoint` ([EndpointConfig](#endpointconfig)): l'endpoint Shadowsocks a cui connettersi.

- `cipher` (*string*): il [cifrario di crittografia autenticata con dati associati](https://shadowsocks.org/doc/aead.html#aead-ciphers) da utilizzare.

- `secret` (*string*): utilizzato per generare la chiave di crittografia.

- `prefix` (*string*, facoltativo): il [mascheramento del prefisso](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/) da utilizzare.
Supportato sulle connessioni Stream e Packet.

Esempio:

```yaml
endpoint: example.com:80
cipher: chacha20-ietf-poly1305
secret: SECRET
prefix: "POST "
```

## Meta definizioni {#meta_definitions}

### FirstSupportedConfig {#firstsupportedconfig}

Utilizza la prima configurazione supportata dall'applicazione. Questo è un modo per incorporare le nuove configurazioni mantenendo la compatibilità con quelle precedenti.

**Formato:** *struct*

**Campi:**

- `options` ([EndpointConfig[]](#endpointconfig) |
[DialerConfig[]](#dialerconfig) |
[PacketListenerConfig[]](#packetlistenerconfig)): elenco delle opzioni di cui tenere conto.

Esempio:

```yaml
options:
  - $type: websocket
    url: wss://example.com/SECRET_PATH
  - ss.example.com:4321
```

### Interface {#interface}

Interface consente di scegliere una tra più implementazioni. Utilizza il campo `$type` per specificare il tipo rappresentato da Config.

Esempio:

```yaml
$type: shadowsocks
endpoint: example.com:4321
cipher: chacha20-ietf-poly1305
secret: SECRET
```
