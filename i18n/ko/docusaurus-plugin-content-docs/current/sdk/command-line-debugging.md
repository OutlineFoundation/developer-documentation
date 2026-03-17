---
title: "Outline SDK를 사용하여 원격으로 네트워크 간섭 특성화 및 우회"
sidebar_label: "Outline SDK를 사용하여 원격으로 네트워크 간섭 특성화 및 우회"
---

이 가이드에서는 Outline SDK의 명령줄 도구를 사용하여 원격 관점에서 네트워크 간섭을 이해하고 우회하는 방법을 보여줍니다. SDK의 도구를 사용하여 네트워크 간섭을 측정하고, 우회 전략을 테스트하고, 결과를 분석하는 방법을 알아봅니다. 이 가이드에서는 `resolve`, `fetch`, `http2transport` 도구에 중점을 둡니다.

## Outline SDK 도구 시작하기

명령줄에서 직접 Outline SDK 도구를 사용할 수 있습니다.

### DNS 해결

`resolve` 도구를 사용하면 지정된 리졸버로 DNS 조회를 실행할 수 있습니다.

도메인의 A 레코드를 확인하려면 다음 단계를 따르세요.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type A 1.2.3.4.nip.io
```

CNAME 레코드를 확인하려면 다음 단계를 따르세요.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type CNAME www.google.com
```

### 웹페이지 가져오기

`fetch` 도구를 사용하여 웹페이지의 콘텐츠를 가져올 수 있습니다.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest https://example.com
```

또한 연결에서 QUIC를 사용하도록 강제할 수 있습니다.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -proto=h3 https://www.youtube.com
```

### 로컬 프록시 사용

`http2transport` 도구는 트래픽을 라우팅할 로컬 프록시를 만듭니다.
Shadowsocks 전송으로 로컬 프록시를 시작하려면 다음을 실행하세요.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/http2transport@latest -localAddr 127.0.0.1:8080 -transport "ss://{your_shadowsocks_credentials}"
```

그런 다음 curl과 같은 다른 도구와 함께 이 프록시를 사용할 수 있습니다.

```sh
curl -p -x http://127.0.0.1:8080 https://ipinfo.io
```

## 우회 전략 지정

Outline SDK를 사용하면 다양한 우회 전략을 지정할 수 있으며, 이러한 전략을 결합하여 다양한 형태의 네트워크 간섭을 우회할 수 있습니다. 이러한 전략의 사양은 [Go 문서](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl)에 있습니다.

### 구성 가능한 전략

이러한 전략을 결합하여 더 강력한 우회 기법을 만들 수 있습니다.

* **TLS 프래그먼트가 있는 DNS-over-HTTPS**: `doh:name=cloudflare-dns.com&address=cloudflare.net:443 | tlsfrag:1`

* **도메인 프론팅을 사용하는 SOCKS5-over-TLS**: `tls:sni=decoy.example.com&certname=[HOST] | socks5:[HOST]:[PORT]`

* **Shadowsocks를 사용한 멀티 홉 라우팅**: `ss://[USERINFO1]@[HOST1]:[PORT1] | ss://[USERINFO2]@[HOST2]:[PORT2] | ss://[USERINFO3]@[HOST3]:[PORT3]`

## 원격 액세스 및 측정

여러 지역에서 발생하는 네트워크 간섭을 측정하려면 원격 프록시를 사용하면 됩니다. 연결할 원격 프록시를 찾거나 만들 수 있습니다.

### 원격 액세스 옵션

`fetch` 도구를 사용하면 다양한 방법으로 원격 연결을 테스트할 수 있습니다.

#### Outline 서버

Shadowsocks 전송을 사용하여 표준 Outline 서버에 원격으로 연결합니다.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "ss://{remote_shadowsocks_credentials}" https://ipinfo.io | jq
```

#### SSH를 통한 SOCKS5

SSH 터널을 사용하여 SOCKS5 프록시를 만듭니다.

```sh
ssh -D 127.0.0.1:1080 -C -N $USER@$HOST:$PORT
```

fetch를 사용하여 해당 터널에 연결

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "socks5://localhost:1080" https://ipinfo.io | jq
```

## 우수사례: 이란에서 YouTube 차단 우회하기

다음은 네트워크 간섭을 감지하고 우회하는 실제 예입니다.

### 블록 감지

이란 프록시를 통해 YouTube 홈페이지를 가져오려고 하면 요청이 시간 초과되어 차단되었음을 나타냅니다.

```sh
export TRANSPORT="ss://{remote_shadowsocks_credentials}"
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)" https://www.youtube.com
```

이 명령어는 시간 초과로 실패합니다.

### TLS 조각화로 우회

전송에 TLS 조각화를 추가하면 이 차단을 우회할 수 있습니다.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)|tlsfrag:1" https://www.youtube.com | grep -oe '<title>.*</title>'
```

이 명령어는 YouTube 홈페이지의 제목(`<title>YouTube</title>`)을 성공적으로 가져옵니다.

### TLS 조각화 및 DNS-over-HTTPS로 우회

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|tlsfrag:1|doh:name=cloudflare-dns.com&address=www.cloudflare.net" https://www.youtube.com | grep -oe '<title>.*</title>'
```

이 경우에도 `<title>YouTube</title>`가 반환됩니다.

### Outline 서버로 우회하기

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|ss://<your_shadowsocks_credentials>" https://www.youtube.com | grep -oe '<title>.*</title>'
```

이 경우에도 `<title>YouTube</title>`이 반환됩니다.

## 추가 분석 및 리소스

토론 및 질문은 [Outline SDK 토론 그룹](https://github.com/OutlineFoundation/outline-sdk/discussions)을 참고하세요.
