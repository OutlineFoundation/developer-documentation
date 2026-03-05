---
title: "Deploy with Automatic HTTPS Using Caddy"
sidebar_label: "HTTPS with Caddy"
---

이 가이드에서는 강력하고 사용자 친화적인 웹 서버인 [Caddy](https://caddyserver.com/)를 사용하여 Outline 서버 설정을 개선하는 방법을 설명합니다. Caddy는 [자동 HTTPS](https://caddyserver.com/docs/automatic-https) 기능과 유연한 구성을 보유하고 있어 특히 WebSocket 전송을 사용할 때 Outline 서버를 제공하는 데 적합합니다.

## Caddy란 무엇인가요?

Caddy는 사용 용이성과 자동 HTTPS, 다양한 프로토콜 지원으로 알려진 오픈소스 웹 서버입니다. 웹 서버 구성을 간소화하고 다음과 같은 기능을 제공합니다.

- **자동 HTTPS:** Caddy는 TLS 인증서를 자동으로 획득하고 갱신하므로 보안 연결이 보장됩니다.

- **HTTP/3 지원:** Caddy는 더 빠르고 효율적인 웹 트래픽을 위해 최신 HTTP/3 프로토콜을 지원합니다.

- **플러그인으로 확장 가능:** Caddy는 리버스 프록시, 부하 분산 등 다양한 기능을 지원하기 위해 플러그인으로 확장할 수 있습니다.

## 1단계: 기본 요건

- [`xcaddy`](https://github.com/caddyserver/xcaddy)를 다운로드하고 설치합니다.

## 2단계: 도메인 구성

Caddy를 시작하기 전에 도메인 이름이 서버의 IP 주소를 가리키도록 올바르게 구성되었는지 확인합니다.

- **A/AAAA 레코드 설정:** DNS 제공업체에 로그인하고 도메인의 A 및 AAAA 레코드가 각각 서버의 IPv4 및 IPv6 주소를 가리키도록 설정합니다.

- 

**DNS 레코드 확인:** 신뢰할 수 있는 조회를 통해 DNS 레코드가 올바르게 설정되었는지 확인합니다.

## 3단계: 맞춤 Caddy 빌드 구축 및 실행

`xcaddy`를 사용하면 Outline 핵심 서버 모듈과 필요한 기타 서버 확장 모듈이 포함된 맞춤 `caddy` 바이너리를 빌드할 수 있습니다.

## 4단계: Outline을 사용하여 Caddy 서버 구성 및 실행

다음 구성을 사용하여 새 `config.yaml` 파일을 만듭니다.

이 구성은 웹 서버가 포트 `443`에서 수신 대기하는 Shadowsocks-over-WebSockets 전략을 나타내며 `TCP_PATH` 및 `UDP_PATH` 경로에서 각각 TCP 및 UDP Shadowsocks 래핑 트래픽을 허용합니다.

생성된 구성을 사용하여 Outline으로 확장된 Caddy 서버를 실행합니다.

더 많은 구성 예는 [outline-ss-server/outlinecaddy GitHub 저장소](https://github.com/Jigsaw-Code/outline-ss-server/tree/master/outlinecaddy/examples)에서 확인할 수 있습니다.

## 5단계: 동적 액세스 키 만들기

[고급 구성](../management/config) 형식을 사용하여 사용자의 클라이언트 액세스 키 YAML 파일을 생성하고 이전에 서버 측에서 구성한 WebSocket 엔드포인트를 포함합니다.

동적 액세스 키 YAML 파일을 생성한 후에는 사용자에게 제공해야 합니다. 정적 웹 호스팅 서비스에서 파일을 호스팅하거나 동적으로 생성할 수 있습니다. [동적 액세스 키](../management/dynamic-access-keys) 사용 방법을 자세히 알아보세요.

## 6단계: Outline 클라이언트에 연결

공식 [Outline 클라이언트](../../download-links) 애플리케이션(버전 1.15.0+) 중 하나를 사용하고 새로 생성된 동적 액세스 키를 서버 항목으로 추가합니다. Shadowsocks-over-Websocket 구성을 사용하여 서버로의 터널링을 시작하려면 **연결**을 클릭합니다.

[IPInfo](https://ipinfo.io)와 같은 도구를 사용하여 현재 Outline 서버를 통해 인터넷을 탐색하고 있는지 확인합니다.
