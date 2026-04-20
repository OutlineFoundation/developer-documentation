---
title: "Shadowsocks-over-WebSockets"
sidebar_label: "Shadowsocks-over-WebSockets"
---

*Outline 클라이언트 v1.15.0+*

이 튜토리얼에서는 일반 Shadowsocks 연결이 차단되는 환경에서 검열을 우회하는 강력한 기법인 Shadowsocks-over-WebSockets를 구현하는 방법을 자세히 안내합니다. WebSockets 내에 Shadowsocks 트래픽을 캡슐화하여 이를 표준 웹 트래픽으로 위장할 수 있으므로 복원력과 접근성이 향상됩니다.


:::note
Shadowsocks-over-WebSockets는 Outline 클라이언트 v1.15.0+에서만 지원됩니다. 이전 클라이언트 버전을 지원하려면 기존 구성을 유지해야 합니다.
:::

## 1단계: Outline 서버 구성 및 실행 {#step_1_configure_and_run_an_outline_server}

다음 구성을 사용하여 새 `config.yaml` 파일을 만듭니다.

```yaml
web:
  servers:
    - id: server1
      listen:
        - "127.0.0.1:<WEB_SERVER_PORT>"

services:
  - listeners:
      - type: websocket-stream
        web_server: server1
        path: /<TCP_PATH>
      - type: websocket-packet
        web_server: server1
        path: /<UDP_PATH>
    keys:
      - id: 1
        cipher: chacha20-ietf-poly1305
        secret: <SHADOWSOCKS_SECRET>
```

:::tip
프로브를 방지하려면 `path`를 계속 비밀로 유지하세요. 비밀 엔드포인트 역할을 합니다. 경로는 길고 무작위로 생성하는 것이 좋습니다.
:::


최신 [`outline-ss-server`](https://github.com/OutlineFoundation/outline-ss-server/releases)를 다운로드하고 생성된 구성을 사용하여 실행합니다.

```sh
outline-ss-server -config=config.yaml
```

## 2단계: 웹 서버 노출 {#step_2_expose_the_web_server}

WebSocket 웹 서버를 공개적으로 액세스할 수 있도록 하려면 인터넷에 공개하고 [TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security)를 구성해야 합니다.
여러 방법으로 이 작업을 할 수 있습니다. [Caddy](https://caddyserver.com/), [nginx](https://nginx.org/) 또는 [Apache](https://httpd.apache.org/)와 같은 로컬 웹 서버를 사용하여 유효한 TLS 인증서가 있는지 확인하거나 [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) 또는 [ngrok](https://ngrok.com/)와 같은 터널링 서비스를 사용할 수 있습니다.

### TryCloudflare 사용 예 {#example_using_trycloudflare}


:::caution
TryCloudflare는 데모 및 테스트용입니다.
:::

이 예에서는 [TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/)를 사용하여 빠른 터널을 만드는 방법을 보여줍니다. 이를 통해 인바운드 포트를 열지 않고도 로컬 웹 서버를 편리하고 안전하게 노출할 수 있습니다.

1. [`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)를 다운로드하고 설치합니다.

2. 로컬 웹 서버 포트를 가리키는 터널을 만듭니다.

```sh
cloudflared tunnel --url http://127.0.0.1:<WEB_SERVER_PORT>
```

Cloudflare는 WebSocket 엔드포인트에 액세스하고
TLS를 자동으로 처리할 하위 도메인(예:`acids-iceland-davidson-lb.trycloudflare.com`)을 제공합니다. 이 하위 도메인은 나중에 필요하므로 적어 두세요.

## 3단계: 동적 액세스 키 만들기 {#step_3_create_a_dynamic_access_key}

[액세스 키 구성](../management/config) 형식을 사용하여 사용자의 클라이언트 액세스 키 YAML 파일을 생성하고 이전에 서버 측에서 구성한 WebSocket 엔드포인트를 포함합니다.

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN>/<TCP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>

  udp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN>/<UDP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>
```

동적 액세스 키 YAML 파일을 생성한 후에는 사용자에게 제공해야 합니다. 정적 웹 호스팅 서비스에서 파일을 호스팅하거나 동적으로 생성할 수 있습니다. [동적 액세스 키](../management/dynamic-access-keys) 사용 방법을 자세히 알아보세요.

## 4단계: Outline 클라이언트에 연결 {#step_4_connect_with_the_outline_client}

공식 [Outline 클라이언트](../../download-links) 애플리케이션(버전 1.15.0+) 중 하나를 사용하고 새로 생성된 동적 액세스 키를 서버 항목으로 추가합니다. Shadowsocks-over-Websocket 구성을 사용하여 서버로의 터널링을 시작하려면 **연결**을 클릭합니다.

[IPInfo](https://ipinfo.io)와 같은 도구를 사용하여 현재 Outline 서버를 통해 인터넷을 탐색하고 있는지 확인합니다.
