---
title: "Access Key Configuration Reference"
sidebar_label: "Access Key Config"
---

## Tunele

### TunnelConfig

Tunel to obiekt najwyższego poziomu w konfiguracji Outline. Określa, w jaki sposób należy skonfigurować usługę VPN.

**Format:** [ExplicitTunnelConfig](#explicittunnelconfig) | [LegacyShadowsocksConfig](#legacyshadowsocksconfig) | [LegacyShadowsocksURI](#legacyshadowsocksuri)

### ExplicitTunnelConfig

**Format:** *struct*

**Pola:**

- `transport` ([TransportConfig](#transportconfig)): transport obsługujący wymianę pakietów z punktem docelowym

- `error` (*struct*): informacja mająca zostać przekazana użytkownikowi w przypadku błędu usługi (np. wygaśnięcie klucza, przekroczenie limitu)

    - `message` (*ciąg znaków*): wiadomość przyjazna dla użytkownika

    - `details` (*ciąg znaków*): wiadomość wyświetlana, gdy użytkownik otwiera szczegóły błędu. Jest przydatna podczas rozwiązywania problemów.

Pola `error` i `transport` wykluczają się nawzajem.

Przykład udanego działania:

```yaml
transport:
  $type: tcpudp
  tcp:
    ...  # Stream Dialer for TCP
  udp:
    ...  # Packet Listener for UDP
```

Przykład błędu:

```yaml
error:
  message: Quota exceeded
  details: Used 100GB out of 100GB
```

## Transporty

### TransportConfig

Określa, w jaki sposób pakiet powinien zostać wymieniony z punktem docelowym.

**Format:** [interfejs](#interface)

Obsługiwane rodzaje interfejsów:

- `tcpudp`: [TCPUDPConfig](#tcpudpconfig)

### TCPUDPConfig

TCPUDPConfig umożliwia stosowanie oddzielnych strategii TCP i UDP.

**Format:** *struct*

**Pola:**

- `tcp` ([DialerConfig](#dialerconfig)): dialer do obsługi połączeń TCP.

- `udp` ([PacketListenerConfig](#packetlistenerconfig)): detektor pakietów do obsługi pakietów UDP.

Przykład wysyłania danych przez TCP i UDP do różnych punktów końcowych:

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

## Punkty końcowe

Punkty końcowe nawiązują połączenia ze stałym punktem końcowym. Jest to lepsze rozwiązanie niż dialery, ponieważ umożliwia optymalizację pod kątem określonych punktów końcowych. Istnieją strumieniowe i pakietowe punkty końcowe.

### EndpointConfig

**Format:** *ciąg znaków* | [Interfejs](#interface)

Punkt końcowy będący *ciągiem znaków* to adres wybranego punktu końcowego podany w postaci host:port. Połączenie jest nawiązywane za pomocą domyślnego dialera.

Obsługiwane rodzaje interfejsów dla strumieniowych i pakietowych punktów końcowych.

- `dial`: [DialEndpointConfig](#dialendpointconfig)

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `websocket`: [WebsocketEndpointConfig](#websocketendpointconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

### DialEndpointConfig

Nawiązuje połączenia poprzez wybieranie stałego adresu. Może potrzebować dialera umożliwiającego tworzenie strategii.

**Format:** *struct*

**Pola:**

- `address` (*ciąg znaków*): adres punktu końcowego do wybrania

- `dialer` ([DialerConfig](#dialerconfig)): dialer obsługujący wybieranie adresu

### WebsocketEndpointConfig

Tunele obsługują strumieniowe i pakietowe połączenia do punktów końcowych przez protokoły Websocket.

W przypadku połączeń strumieniowych każdy zapis jest zamieniany w wiadomość Websocket. W przypadku połączeń pakietowych każdy pakiet jest zamieniany w wiadomość Websocket.

**Format:** *struct*

**Pola:**

- `url` (*ciąg znaków*): adres URL punktu końcowego Websocket. Schemat musi mieć format `https` lub `wss` dla Websocket przez TLS albo `http` lub `ws` dla tekstu jawnego Websocket.

- `endpoint` ([EndpointConfig](#endpointconfig)): punkt końcowy serwera WWW, z którym ma być nawiązane połączenie. Jeśli go nie ma, nawiązywane jest połączenie z adresem określonym w URL.

## Dialery

Dialery nawiązują połączenia z podanym adresem punktu końcowego. Istnieją dialery strumieniowe i pakietowe.

### DialerConfig

**Format:** *null* | [Interfejs](#interface)

Dialer *null* (brak wartości) oznacza domyślny dialer, który wykorzystuje bezpośrednie połączenia TCP do dialerów strumieniowych i bezpośrednie połączenia UDP do dialerów pakietowych.

Obsługiwane rodzaje interfejsów dla dialerów strumieniowych i pakietowych:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

## Detektory pakietów

Detektor pakietów nawiązuje nieograniczone połączenia pakietowe, które można wykorzystać do wysyłania pakietów do wielu punktów docelowych.

### PacketListenerConfig

**Format:** *null* | [Interfejs](#interface)

Detektor pakietów *null* (brak wartości) to domyślny detektor pakietów będący detektorem pakietów UDP.

Obsługiwane rodzaje interfejsów:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksPacketListenerConfig](#shadowsocksconfig)S

## Strategie

### Shadowsocks

#### LegacyShadowsocksConfig

LegacyShadowsocksConfig reprezentuje tunel, który wykorzystuje Shadowsocks jako transport. Używa starszego formatu, aby uzyskać zgodność wsteczną.

**Format:** *struct*

**Pola:**

- `server` (*ciąg znaków*): host z którym ma być nawiązane połączenie

- `server_port` (*numer*): numer portu, z którym ma być nawiązane połączenie

- `method` (*ciąg znaków*): [algorytm szyfrujący AEAD](https://shadowsocks.org/doc/aead.html#aead-ciphers), który zostanie użyty

- `password` (*ciąg znaków*): wykorzystywane do generowania klucza szyfrującego

- `prefix` (*ciąg znaków*): [maskowanie przy użyciu prefiksu](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/), które zostanie zastosowane.
Obsługiwane w przypadku połączeń strumieniowych i pakietowych.

Przykład:

```yaml
server: example.com
server_port: 4321
method: chacha20-ietf-poly1305
password: SECRET
prefix: "POST "
```

#### LegacyShadowsocksURI

LegacyShadowsocksURI reprezentuje tunel, który wykorzystuje Shadowsocks jako transport.
Używa starszego formatu URL, aby uzyskać zgodność wsteczną.

**Format:** *ciąg znaków*

Zobacz [starszy format URI Shadowsocks](https://shadowsocks.org/doc/configs.html#uri-and-qr-code) i [schemat URI SIP002](https://shadowsocks.org/doc/sip002.html). Nie obsługujemy wtyczek.

Przykład:

```yaml
ss://chacha20-ietf-poly1305:SECRET@example.com:443?prefix=POST%20
```

#### ShadowsocksConfig

ShadowsocksConfig może reprezentować dialery strumieniowe i pakietowe oraz detektor pakietów, który korzysta z Shadowsocks.

**Format:** *struct*

**Pola:**

- `endpoint` ([EndpointConfig](#endpointconfig)): punkt końcowy Shadowsocks, z którym ma być nawiązane połączenie

- `cipher` (*ciąg znaków*): [algorytm szyfrujący AEAD](https://shadowsocks.org/doc/aead.html#aead-ciphers), który zostanie użyty

- `secret` (*ciąg znaków*): wykorzystywany do generowania klucza szyfrującego

- `prefix` (*ciąg znaków*): [maskowanie przy użyciu prefiksu](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/), które zostanie zastosowane.
Obsługiwane w przypadku połączeń strumieniowych i pakietowych.

Przykład:

```yaml
endpoint: example.com:80
cipher: chacha20-ietf-poly1305
secret: SECRET
prefix: "POST "
```

## Metadefinicje

### FirstSupportedConfig

Korzysta z pierwszej konfiguracji obsługiwanej przez aplikację. To sposób na wdrażanie nowych konfiguracji przy zachowaniu zgodności wstecznej ze starymi.

**Format:** *struct*

**Pola:**

- `options` ([EndpointConfig[]](#endpointconfig) | [DialerConfig[]](#dialerconfig) | [PacketListenerConfig[]](#packetlistenerconfig)): lista opcji do rozważenia

Przykład:

```yaml
options:
  - $type: websocket
    url: wss://example.com/SECRET_PATH
  - ss.example.com:4321
```

### Interfejs

Interfejs umożliwia wybranie jednej z wielu implementacji. Wykorzystuje pole `$type` do określenia rodzaju, który reprezentuje konfiguracja.

Przykład:

```yaml
$type: shadowsocks
endpoint: example.com:4321
cipher: chacha20-ietf-poly1305
secret: SECRET
```
