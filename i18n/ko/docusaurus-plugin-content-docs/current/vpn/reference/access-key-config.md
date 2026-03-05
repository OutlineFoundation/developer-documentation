---
title: "Access Key Configuration Reference"
sidebar_label: "Access Key Config"
---

## 터널

### TunnelConfig

터널은 Outline 구성에서 최상위 객체입니다. VPN을 구성하는 방법을 지정합니다.

**형식:** [ExplicitTunnelConfig](#explicittunnelconfig) |
[LegacyShadowsocksConfig](#legacyshadowsocksconfig) |
[LegacyShadowsocksURI](#legacyshadowsocksuri)

### ExplicitTunnelConfig

**형식:** *구조체*

**필드:**

- `transport`([TransportConfig](#transportconfig)): 대상 목적지와 패키지를 교환하는 데 사용할 전송입니다.

- `error`(*구조체*): 서비스 오류가 발생하는 경우 사용자에게 전달할 정보(예: 키 만료, 할당량 소진)입니다.

    - `message`(*문자열*): 사용자에게 표시할 사용자 친화적 메시지입니다.

    - `details`(*문자열*): 사용자가 오류 세부정보를 열 때 표시할 메시지입니다. 문제 해결에 도움이 됩니다.

`error` 및 `transport` 필드는 상호 배타적입니다.

성공적인 예:

```yaml
transport:
  $type: tcpudp
  tcp:
    ...  # Stream Dialer for TCP
  udp:
    ...  # Packet Listener for UDP
```

오류 예:

```yaml
error:
  message: Quota exceeded
  details: Used 100GB out of 100GB
```

## 전송

### TransportConfig

대상 목적지와 패킷을 교환하는 방법을 지정합니다.

**형식:** [인터페이스](#interface)

지원되는 인터페이스 유형:

- `tcpudp`: [TCPUDPConfig](#tcpudpconfig)

### TCPUDPConfig

TCPUDPConfig를 사용하면 별도의 TCP 전략과 UDP 전략을 설정할 수 있습니다.

**형식:** *구조체*

**필드:**

- `tcp`([DialerConfig](#dialerconfig)): TCP 연결에 사용할 스트림 다이얼러입니다.

- `udp`([PacketListenerConfig](#packetlistenerconfig)): UDP 패킷에 사용할 패킷 리스너입니다.

TCP와 UDP를 다른 엔드포인트로 전송하는 예:

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

## 엔드포인트

엔드포인트는 고정된 엔드포인트에 대한 연결을 설정합니다. 엔드포인트별로 최적화할 수 있어 다이얼러보다 선호됩니다. 스트림 엔드포인트와 패킷 엔드포인트가 있습니다.

### EndpointConfig

**형식:** *문자열* | [인터페이스](#interface)

*문자열* 엔드포인트는 선택된 엔드포인트의 호스트:포트 주소입니다. 연결은 기본 다이얼러를 사용하여 설정됩니다.

지원되는 스트림 및 패킷 엔드포인트 인터페이스 유형

- `dial`: [DialEndpointConfig](#dialendpointconfig)

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `websocket`: [WebsocketEndpointConfig](#websocketendpointconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

### DialEndpointConfig

고정 주소로 전화를 걸어 연결을 설정합니다. 전략 구성을 허용하는 다이얼러를 사용할 수 있습니다.

**형식:** *구조체*

**필드:**

- `address`(*문자열*): 전화를 걸 엔드포인트 주소입니다.

- `dialer`([DialerConfig](#dialerconfig)): 주소로 전화를 걸 때 사용할 다이얼러입니다.

### WebsocketEndpointConfig

Websockets를 통해 엔드포인트에 대한 스트림 및 패킷 연결을 터널링합니다.

스트림 연결의 경우 각 쓰기가 Websocket 메시지로 변환됩니다. 패킷 연결의 경우 각 패킷이 Websocket 메시지로 변환됩니다.

**형식:** *구조체*

**필드:**

- `url`(*문자열*): Websocket 엔드포인트의 URL입니다. 스키마는 TLS를 통한 Websocket의 경우 `https` 또는 `wss`여야 하고 일반 텍스트 Websocket의 경우 `http` 또는 `ws`여야 합니다.

- `endpoint`([EndpointConfig](#endpointconfig)): 연결할 웹 서버 엔드포인트입니다. 없는 경우 URL에 지정된 주소에 연결합니다.

## 다이얼러

다이얼러는 엔드포인트 주소가 주어지면 연결을 설정합니다. 스트림 다이얼러와 패킷 다이얼러가 있습니다.

### DialerConfig

**형식:** *null* | [인터페이스](#interface)

*null*(부재하는) 다이얼러는 기본 다이얼러를 의미하며 스트림에는 직접 TCP 연결을 사용하고 패킷에는 직접 UDP 연결을 사용합니다.

지원되는 스트림 및 패킷 다이얼러 인터페이스 유형

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

## 패킷 리스너

패킷 리스너는 여러 목적지로 패킷을 전송하는 데 사용할 수 있는 무제한 패킷 연결을 설정합니다.

### PacketListenerConfig

**형식:** *null* | [인터페이스](#interface)

*null*(부재하는) 패킷 리스너는 기본 패킷 리스너를 의미하며 이는 UDP 패킷 리스너입니다.

지원되는 인터페이스 유형:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksPacketListenerConfig](#shadowsocksconfig)

## 전략

### Shadowsocks

#### LegacyShadowsocksConfig

LegacyShadowsocksConfig는 Shadowsocks를 전송으로 사용하는 터널을 나타냅니다. 하위 호환성을 위해 기존 형식을 구현합니다.

**형식:** *구조체*

**필드:**

- `server`(*문자열*): 연결할 호스트입니다.

- `server_port`(*숫자*): 연결할 포트 번호입니다.

- `method`(*문자열*): 사용할 [AEAD 암호화](https://shadowsocks.org/doc/aead.html#aead-ciphers)입니다.

- `password`(*문자열*): 암호화 키를 생성하는 데 사용됩니다.

- `prefix`(*문자열*): 사용할 [접두사 위장](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/)입니다.
스트림 및 패킷 연결에서 지원됩니다.

예:

```yaml
server: example.com
server_port: 4321
method: chacha20-ietf-poly1305
password: SECRET
prefix: "POST "
```

#### LegacyShadowsocksURI

LegacyShadowsocksURI는 Shadowsocks를 전송으로 사용하는 터널을 나타냅니다.
하위 호환성을 위해 기존 URL 형식을 구현합니다.

**형식:** *문자열*

[기존 Shadowsocks URI 형식](https://shadowsocks.org/doc/configs.html#uri-and-qr-code) 및 [SIP002 URI 스킴](https://shadowsocks.org/doc/sip002.html)을 참고하세요. 플러그인은 지원되지 않습니다.

예:

```yaml
ss://chacha20-ietf-poly1305:SECRET@example.com:443?prefix=POST%20
```

#### ShadowsocksConfig

ShadowsocksConfig는 스트림 또는 패킷 다이얼러와 Shadowsocks를 사용하는 패킷 리스너를 나타낼 수 있습니다.

**형식:** *구조체*

**필드:**

- `endpoint`([EndpointConfig](#endpointconfig)): 연결할 Shadowsocks 엔드포인트입니다.

- `cipher`(*문자열*): 사용할 [AEAD 암호화](https://shadowsocks.org/doc/aead.html#aead-ciphers)입니다.

- `secret`(*문자열*): 암호화 키를 생성하는 데 사용됩니다.

- `prefix`(*문자열*, 선택사항): 사용할 [접두사 위장](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/)입니다.
스트림 및 패킷 연결에서 지원됩니다.

예:

```yaml
endpoint: example.com:80
cipher: chacha20-ietf-poly1305
secret: SECRET
prefix: "POST "
```

## 메타 정의

### FirstSupportedConfig

애플리케이션에서 지원하는 첫 번째 구성을 사용합니다. 이는 이전 구성과 하위 호환되면서 새 구성을 통합하는 방법입니다.

**형식:** *구조체*

**필드:**

- `options`([EndpointConfig[]](#endpointconfig) |
[DialerConfig[]](#dialerconfig) |
[PacketListenerConfig[]](#packetlistenerconfig)): 고려할 옵션 목록입니다.

예:

```yaml
options:
  - $type: websocket
    url: wss://example.com/SECRET_PATH
  - ss.example.com:4321
```

### 인터페이스

인터페이스를 통해 여러 구현 중 하나를 선택할 수 있습니다. `$type` 필드를 사용하여 구성이 나타내는 유형을 지정합니다.

예:

```yaml
$type: shadowsocks
endpoint: example.com:4321
cipher: chacha20-ietf-poly1305
secret: SECRET
```
