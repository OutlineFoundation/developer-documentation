---
title: "Smart Dialer Configuration"
sidebar_label: "Smart Dialer Config"
---

**스마트 다이얼러**는 주어진 테스트 도메인 목록에 대해 DNS 및 TLS 차단을 해제할 전략을 검색하며, 여러 전략을 기술하는 구성에서 전략을 선택합니다.

## 스마트 다이얼러를 위한 YAML 구성 {#yaml_config_for_the_smart_dialer}

스마트 다이얼러에서 사용하는 구성은 YAML 형식입니다. 예를 들면 다음과 같습니다.

```yaml
dns:
  - system: {}
  - https:
      name: 8.8.8.8
  - https:
      name: 9.9.9.9
tls:
  - ""
  - split:2
  - tlsfrag:1

fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

### DNS 구성 {#dns_configuration}

- `dns` 필드는 테스트하려는 DNS 리졸버 목록을 지정합니다.

- 각 DNS 리졸버는 다음 유형 중 하나일 수 있습니다.

    - `system`: 시스템 리졸버를 사용합니다. 빈 객체로 지정하세요.

    - `https`: 암호화된 DNS-over-HTTPS(DoH) 리졸버를 사용합니다.

    - `tls`: 암호화된 DNS over TLS(DoT) 리졸버를 사용합니다.

    - `udp`: UDP 리졸버를 사용합니다.

    - `tcp`: TCP 리졸버를 사용합니다.

#### DNS-over-HTTPS 리졸버(DoH) {#dns-over-https_resolver_doh}

```yaml
https:
  name: dns.google
  address: 8.8.8.8
```

- `name`: DoH 서버의 도메인 이름입니다.

- `address`: DoH 서버의 호스트:포트입니다. 기본값은 `name`:443입니다.

#### DNS-over-TLS 리졸버(DoT) {#dns-over-tls_resolver_dot}

```yaml
tls:
  name: dns.google
  address: 8.8.8.8
```

- `name`: DoH 서버의 도메인 이름입니다.

- `address`: DoT 서버의 호스트:포트입니다. 기본값은 `name`:853입니다.

#### UDP 리졸버 {#udp_resolver}

```yaml
udp:
  address: 8.8.8.8
```

- `address`: UDP 리졸버의 호스트:포트입니다.

#### TCP 리졸버 {#tcp_resolver}

```yaml
tcp:
  address: 8.8.8.8
```

- `address`: TCP 리졸버의 호스트:포트입니다.

### TLS 구성 {#tls_configuration}

- `tls` 필드는 테스트하려는 TLS 전송 목록을 지정합니다.

- 각 TLS 전송은 사용하려는 전송을 지정하는 문자열입니다.

- 예를 들어, `override:host=cloudflare.net|tlsfrag:1`은 Cloudflare 및 TLS 단편화를 통해 도메인 프론팅을 사용하는 전송을 지정합니다. 자세한 내용은 [구성 문서](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x/configurl#hdr-Config_Format)를 참고하세요.

### 대체 구성 {#fallback_configuration}

대체 구성은 프록시리스 전략이 모두 연결에 실패할 경우 사용됩니다. 예를 들어 사용자의 연결을 시도할 백업 프록시 서버를 지정할 수 있습니다. 대체 구성을 사용할 경우, 다른 DNS/TLS 전략이 먼저 실패하거나 시간이 초과된 후에야 실행되므로 시작이 지연될 수 있습니다.

대체 문자열은 다음 중 하나여야 합니다.

- [`configurl`](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x/configurl#hdr-Proxy_Protocols)에 정의된 형식에 따른 유효한 `StreamDialer` 구성 문자열

- `psiphon` 필드의 하위 요소로서 유효한 Psiphon 구성 객체

#### Shadowsocks 서버 예 {#shadowsocks_server_example}

```yaml
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

#### SOCKS5 서버 예 {#socks5_server_example}

```yaml
fallback:
  - socks5://[USERINFO]@[HOST]:[PORT]
```

#### Psiphon 구성 예 {#psiphon_config_example}

[Psiphon](https://psiphon.ca/) 네트워크를 사용하려면 다음을 수행해야 합니다.

1. Psiphon 팀에 문의하여 해당 네트워크에 액세스할 수 있는 구성 정보를 받습니다. 계약이 필요할 수도 있습니다.

2. 수신한 Psiphon 구성 정보를 스마트 다이얼러 구성의 `fallback` 섹션에 추가합니다. JSON은 YAML과 호환되므로 다음과 같이 Psiphon 구성을 `fallback` 섹션에 직접 복사하여 붙여넣을 수 있습니다.

```yaml
fallback:
  - psiphon: {
      "PropagationChannelId": "FFFFFFFFFFFFFFFF",
      "SponsorId": "FFFFFFFFFFFFFFFF",
      "DisableLocalSocksProxy" : true,
      "DisableLocalHTTPProxy" : true,
      ...
    }
```

### 스마트 다이얼러 사용 방법 {#how_to_use_the_smart_dialer}

스마트 다이얼러를 사용하려면 `StrategyFinder` 객체를 만들고 `NewDialer` 메서드를 호출하여 테스트 도메인 목록과 YAML 구성을 전달합니다.
`NewDialer` 메서드는 찾은 전략을 사용하여 연결을 생성할 수 있는 `transport.StreamDialer` 객체를 반환합니다. 예를 들면 다음과 같습니다.

```go
finder := &smart.StrategyFinder{
    TestTimeout:  5 * time.Second,
    LogWriter:   os.Stdout,
    StreamDialer: &transport.TCPDialer{},
    PacketDialer: &transport.UDPDialer{},
}

configBytes := []byte(`
dns:
  - system: {}
  - https:
      name: 8.8.8.8
  - https:
      name: 9.9.9.9
tls:
  - ""
  - split:2
  - tlsfrag:1
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
`)

dialer, err := finder.NewDialer(
  context.Background(),
  []string{"www.google.com"},
  configBytes
)
if err != nil {
    // Handle error.
}

// Use dialer to create connections.
```

이 예시는 기본적인 사용 방법일 뿐이며 특정 사용 사례에 따라 조정이 필요할 수 있습니다.
