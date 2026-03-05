---
title: "Configure Access Keys"
sidebar_label: "Configure Access Keys"
---

Outline은 YAML 기반 구성을 사용하여 VPN 매개변수를 정의하고 TCP/UDP 트래픽을 처리합니다. 구성은 여러 수준에서 구성 가능성을 지원하므로 유연하고 확장 가능한 설정이 가능해집니다.

최상위 구성은 [TunnelConfig](../reference/access-key-config#tunnelconfig)를 지정합니다.

## 예

일반적인 Shadowsocks 구성은 다음과 같습니다.

이제 TCP와 UDP가 다른 포트나 엔드포인트에서 다른 접두사를 사용하여 실행될 수 있다는 점에 유의하세요.

YAML 앵커와 `<<` 병합 키를 사용하여 중복을 방지할 수 있습니다.

이제 전략을 구성하고 멀티 홉을 실행할 수 있습니다.

Shadowsocks와 같은 '아무것도 아닌 것처럼 보이는' 프로토콜을 차단하는 경우 Shadowsocks-over-Websockets를 사용하면 됩니다. 배포 방법은 [서버 구성 예](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml)를 참고하세요. 클라이언트 구성은 다음과 같습니다.

Websocket 엔드포인트는 결과적으로 엔드포인트를 가져올 수 있고 DNS 기반 차단을 우회하는 데 이를 활용할 수 있습니다.

다양한 Outline 클라이언트 버전에서 호환성을 보장하려면 구성에서 `first-supported` 옵션을 사용하세요. 이는 새 전략과 기능이 Outline에 추가될 때 특히 중요합니다. 일부 사용자는 최신 클라이언트 소프트웨어로 업데이트하지 않았을 수 있기 때문입니다. `first-supported`를 사용하면 다양한 플랫폼과 클라이언트 버전에서 원활하게 작동하는 단일 구성을 제공할 수 있어 하위 호환성과 일관된 사용자 환경이 보장됩니다.
