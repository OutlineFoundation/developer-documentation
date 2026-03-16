---
title: "Concepts"
sidebar_label: "Concepts"
---

Outline SDK는 구성과 재사용이 가능하도록 상호 운용 가능한 인터페이스로 정의된 몇 가지 기본 개념을 기반으로 빌드되었습니다.

## 연결 {#connections}

연결은 추상화된 전송을 통해 두 엔드포인트 간 통신을 지원합니다. 연결에는 두 가지 유형이 있습니다.

- `transport.StreamConn`: TCP 및 `SOCK_STREAM` Posix 소켓 유형과 같은 스트림 기반 연결입니다.

- `transport.PacketConn`: UDP 및 `SOCK_DGRAM` Posix 소켓 유형과 같은 데이터그램 기반 연결입니다.
Go 표준 라이브러리의 규칙에 따라 'Datagram' 대신 'Packet'을 사용합니다.

연결을 래핑하여 새로운 전송을 통해 중첩된 연결을 만들 수 있습니다.
예를 들어 `StreamConn`은 TCP에, TCP상의 TLS에, TCP상의 TLS상의 HTTP에, 또는 QUIC에 구성될 수 있으며 그 외에도 다양한 옵션이 있습니다.

## 다이얼러 {#dialers}

다이얼러는 호스트:포트 주소를 기반으로 연결을 생성하며, 이 과정에서 기본 전송이나 프록시 프로토콜을 캡슐화합니다.
`StreamDialer` 및 `PacketDialer` 유형은 주소를 기반으로 각각 `StreamConn` 및 `PacketConn` 연결을 만듭니다. 다이얼러도 중첩될 수 있습니다.
예를 들어, TLS 스트림 다이얼러는 TCP 다이얼러를 사용하여 TCP 연결을 기반으로 하는 `StreamConn`을 만든 다음 해당 TCP `StreamConn`을 기반으로 TLS `StreamConn`을 만들 수 있습니다. SOCKS5-over-TLS 다이얼러는 TLS 다이얼러를 사용하여 프록시 서버와의 TLS `StreamConn`을 먼저 생성한 후 대상 주소로의 SOCKS5 연결을 수행할 수 있습니다.

## 리졸버 {#resolvers}

리졸버(`dns.Resolver`)는 DNS 관련 질문에 대답하며, 이 과정에서 기본 알고리즘 또는 프로토콜을 캡슐화합니다.
리졸버는 주로 도메인 이름을 IP 주소에 매핑하는 데 사용됩니다.
