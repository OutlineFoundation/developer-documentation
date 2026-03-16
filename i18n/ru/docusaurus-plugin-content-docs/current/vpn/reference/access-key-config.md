---
title: "Конфигурация"
sidebar_label: "Конфигурация"
---

## Туннели {#tunnels}

### TunnelConfig {#tunnelconfig}

Tunnel – это основной объект в конфигурации Outline. Он определяет, как должен быть настроен VPN.

**Формат:** [ExplicitTunnelConfig](#explicittunnelconfig) | [LegacyShadowsocksConfig](#legacyshadowsocksconfig) | [LegacyShadowsocksURI](#legacyshadowsocksuri)

### ExplicitTunnelConfig {#explicittunnelconfig}

**Формат:** *struct*

**Поля**

- `transport` ([TransportConfig](#transportconfig)): протокол для передачи пакетов к целевому узлу.

- `error` (*struct*): информация об ошибке сервиса (например, истечение срока действия ключа или превышение квоты).

    - `message` (*string*): текстовое сообщение для пользователя.

    - `details` (*string*): дополнительная информация об ошибке, доступная по запросу. Может быть полезной при устранении неполадок.

Поля `error` и `transport` являются взаимоисключающими.

Пример эффективной конфигурации:

```yaml
transport:
  $type: tcpudp
  tcp:
    ...  # Stream Dialer for TCP
  udp:
    ...  # Packet Listener for UDP
```

Пример ошибки:

```yaml
error:
  message: Quota exceeded
  details: Used 100GB out of 100GB
```

## Протоколы {#transports}

### TransportConfig {#transportconfig}

Определяет, каким образом пакеты передаются к целевому узлу.

**Формат:** [Interface](#interface)

Поддерживаемые типы Interface:

- `tcpudp`: [TCPUDPConfig](#tcpudpconfig)

### TCPUDPConfig {#tcpudpconfig}

TCPUDPConfig позволяет задавать отдельные стратегии для протоколов TCP и UDP.

**Формат:** *struct*

**Поля**

- `tcp` ([DialerConfig](#dialerconfig)): конфигурация Stream Dialer для TCP-соединений.

- `udp` ([PacketListenerConfig](#packetlistenerconfig)): конфигурация Packet Listener для обработки UDP-трафика.

Пример отправки TCP и UDP на разные конечные точки:

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

## Конечные точки {#endpoints}

Объект Endpoint устанавливает соединение с фиксированной конечной точкой. В отличие от Dialer, этот объект позволяет применять оптимизированные настройки для определенного узла. Существует два типа объектов Endpoint: Stream и Packet.

### EndpointConfig {#endpointconfig}

**Формат:** *string* | [Interface](#interface)

Endpoint формата *string* – это адрес выбранной конечной точки в формате host:port. Подключение устанавливается через объект Dialer по умолчанию.

Поддерживаемые типы Interface для Stream и Packet:

- `dial`: [DialEndpointConfig](#dialendpointconfig)

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `websocket`: [WebsocketEndpointConfig](#websocketendpointconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

### DialEndpointConfig {#dialendpointconfig}

Отвечает за установку подключений с фиксированным адресом. Может использовать Dialer, что позволяет комбинировать стратегии подключения.

**Формат:** *struct*

**Поля**

- `address` (*string*): адрес конечной точки, с которой устанавливается соединение.

- `dialer` ([DialerConfig](#dialerconfig)): Dialer, используемый для подключения к указанному адресу.

### WebsocketEndpointConfig {#websocketendpointconfig}

Туннелирует Stream- и Packet-подключения к конечной точке через WebSockets.

В Stream-подключениях каждая запись превращается в сообщение WebSocket. В Packet-подключениях каждый пакет передается как отдельное сообщение WebSocket.

**Формат:** *struct*

**Поля**

- `url` (*string*): URL конечной точки WebSocket. Для WebSocket через TLS требуется использовать схему `https` или `wss`, а для обычного WebSocket – `http` или `ws`.

- `endpoint` ([EndpointConfig](#endpointconfig)): конечная точка веб-сервера для подключения. Если параметр отсутствует, подключение устанавливается к адресу, указанному в URL.

## Dialer {#dialers}

Объект Dialer устанавливает подключение к конечной точке с заданным адресом. Существуют два типа объектов Dialer: Stream и Packet.

### DialerConfig {#dialerconfig}

**Формат:** *null*, [Interface](#interface)

Значение *null* означает, что используется объект Dialer по умолчанию, который устанавливает прямые TCP-подключения для Stream и прямые UDP-подключения для Packet.

Поддерживаемые типы Interface для Stream и Packer:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

## Packet Listener {#packet_listeners}

Объект Packet Listener устанавливает неограниченное пакетное подключение, которое можно использовать для отправки пакетов на разные конечные точки.

### PacketListenerConfig {#packetlistenerconfig}

**Формат:** *null*, [Interface](#interface)

Значение *null* означает, что используется объект Packet Listener по умолчанию, который используется для прослушивания UDP-пакетов.

Поддерживаемые типы Interface:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksPacketListenerConfig](#shadowsocksconfig)

## Стратегии {#strategies}

### Shadowsocks {#shadowsocks}

#### LegacyShadowsocksConfig {#legacyshadowsocksconfig}

LegacyShadowsocksConfig представляет объект Tunnel, использующий Shadowsocks в качестве протокола. Он реализует устаревший формат для обратной совместимости.

**Формат:** *struct*

**Поля**

- `server` (*string*): хост, к которому устанавливается подключение.

- `server_port` (*number*): номер порта для подключения.

- `method` (*string*): [AEAD-шифр](https://shadowsocks.org/doc/aead.html#aead-ciphers), используемый для шифрования.

- `password` (*string*): пароль, используемый для генерации ключа шифрования.

- `prefix` (*string*): [префикс для маскировки](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/).
Поддерживается при Stream- и Packet-подключениях.

Пример:

```yaml
server: example.com
server_port: 4321
method: chacha20-ietf-poly1305
password: SECRET
prefix: "POST "
```

#### LegacyShadowsocksURI {#legacyshadowsocksuri}

LegacyShadowsocksURI представляет объект Tunnel, использующий Shadowsocks в качестве протокола.
Реализует устаревший формат URL для обратной совместимости.

**Формат:** *string*

Ознакомьтесь с [устаревшим форматом Shadowsocks URI](https://shadowsocks.org/doc/configs.html#uri-and-qr-code) и [схемой SIP002 URI](https://shadowsocks.org/doc/sip002.html). Плагины не поддерживаются.

Пример:

```yaml
ss://chacha20-ietf-poly1305:SECRET@example.com:443?prefix=POST%20
```

#### ShadowsocksConfig {#shadowsocksconfig}

ShadowsocksConfig может представлять Stream Dialer, Packet Dialer или Packet Listener, использующие Shadowsocks.

**Формат:** *struct*

**Поля**

- `endpoint` ([EndpointConfig](#endpointconfig)): конечная точка Shadowsocks для подключения.

- `cipher` (*string*): [AEAD-шифр](https://shadowsocks.org/doc/aead.html#aead-ciphers), используемый для шифрования.

- `secret` (*string*): пароль, используемый для генерации ключа шифрования.

- `prefix` (*string*): [префикс для маскировки](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/).
Поддерживается при Stream- и Packet-подключениях.

Пример:

```yaml
endpoint: example.com:80
cipher: chacha20-ietf-poly1305
secret: SECRET
prefix: "POST "
```

## Метаопределения {#meta_definitions}

### FirstSupportedConfig {#firstsupportedconfig}

Использует первую конфигурацию, поддерживаемую приложением. Это позволяет добавлять новые конфигурации, сохраняя обратную совместимость со старыми.

**Формат:** *struct*

**Поля**

- `options` ([EndpointConfig[]](#endpointconfig) | [DialerConfig[]](#dialerconfig) | [PacketListenerConfig[]](#packetlistenerconfig)): список возможных конфигураций.

Пример:

```yaml
options:
  - $type: websocket
    url: wss://example.com/SECRET_PATH
  - ss.example.com:4321
```

### Interface {#interface}

Interface позволяет выбирать одну из нескольких реализаций. Для указания типа конфигурации используется поле `$type`.

Пример:

```yaml
$type: shadowsocks
endpoint: example.com:4321
cipher: chacha20-ietf-poly1305
secret: SECRET
```
