---
title: "Disguise Connections with Prefixes"
sidebar_label: "Connection Prefixes"
---

Outline 클라이언트 버전 1.9.0부터 액세스 키에서 'prefix' 옵션을 지원합니다. 'prefix'는 Shadowsocks TCP 연결 [솔트](https://shadowsocks.org/guide/aead.html)의 첫 번째 바이트로 사용된 바이트 목록입니다.
이를 통해 연결이 네트워크에서 허용되는 프로토콜처럼 보여, 인식하지 못하는 프로토콜을 거부하는 방화벽을 우회할 수 있게 됩니다.

## 언제 사용하면 되나요? {#when_should_i_try_this}

Outline 배포의 사용자가 여전히 차단되고 있다고 생각되면 몇 가지 다른 접두사를 사용해 보는 것이 좋습니다.

## 안내 {#instructions}

접두사는 16바이트 이하여야 합니다. 접두사가 길면 솔트 충돌이 발생할 수 있고 이로 인해 암호화 안전성이 손상되어 연결이 감지될 수 있습니다. 가능한 짧은 접두사를 사용하여 직면하고 있는 차단을 우회하세요.

사용하는 포트는 접두사가 가장하고 있는 프로토콜과 일치해야 합니다.
IANA는 프로토콜과 포트 번호를 매핑하는 [전송 프로토콜 포트 번호 등록처](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)를 유지합니다.

효과적인 접두사의 예는 일반적인 프로토콜과 비슷합니다.

권장 포트
JSON 인코딩
URL 인코딩

HTTP 요청
80(http)
`"POST "`
`POST%20`

HTTP 응답
80(http)
`"HTTP/1.1 "`
`HTTP%2F1.1%20`

DNS-over-TCP 요청
53(dns)
`"\u0005\u00DC\u005F\u00E0\u0001\u0020"`
`%05%C3%9C_%C3%A0%01%20`

TLS ClientHello
443(https), 463(smtps), 563(nntps), 636(ldaps), 989(ftps-data), 990(ftps), 993(imaps), 995(pop3s), 5223(Apple APN), 5228(Play 스토어), 5349(turns)
`"\u0016\u0003\u0001\u0000\u00a8\u0001\u0001"`
`%16%03%01%00%C2%A8%01%01`

TLS 애플리케이션 데이터
443(https), 463(smtps), 563(nntps), 636(ldaps), 989(ftps-data), 990(ftps), 993(imaps), 995(pop3s), 5223(Apple APN), 5228(Play 스토어), 5349(turns)
`"\u0013\u0003\u0003\u003F"`
`%13%03%03%3F`

TLS ServerHello
443(https), 463(smtps), 563(nntps), 636(ldaps), 989(ftps-data), 990(ftps), 993(imaps), 995(pop3s), 5223(Apple APN), 5228(Play 스토어), 5349(turns)
`"\u0016\u0003\u0003\u0040\u0000\u0002"`
`%16%03%03%40%00%02`

SSH
22(ssh), 830(netconf-ssh), 4334(netconf-ch-ssh), 5162(snmpssh-trap)
`"SSH-2.0\r\n"`
`SSH-2.0%0D%0A`

### 동적 액세스 키 {#dynamic_access_keys}

[동적 액세스 키](../management/dynamic-access-keys)(`ssconf://`)와 함께 접두사 기능을 사용하려면 원하는 접두사를 나타내는 **JSON 인코딩** 값(위 표의 예 참고)을 사용하여 'prefix' 키를 JSON 객체에 추가합니다. 이스케이프 코드(예: \u00FF)를 사용하여 `U+0`~`U+FF` 범위에서 인쇄할 수 없는 유니코드 코드 포인트를 나타낼 수 있습니다. 예를 들면 다음과 같습니다.

```json
{
    "server": "example.com",
    "server_port": 8388,
    "password": "example",
    "method": "chacha20-ietf-poly1305",
    "prefix": "\u0005\u00DC\u005F\u00E0\u0001\u0020"
}
```

### 정적 액세스 키 {#static_access_keys}

**정적 액세스 키**(ss://)와 함께 접두사를 사용하려면 기존 키를 수정한 후 배포해야 합니다. Outline Manager에서 생성한 정적 액세스 키가 있다면 **URL 인코딩** 버전의 접두사(위 표의 예 참고)를 가져와 다음과 같이 액세스 키 끝에 추가하세요.

`ss://Z34nthataITHiTNIHTohithITHbVBqQ1o3bkk@127.0.0.1:33142/?outline=1&prefix=<your url-encoded prefix goes here>`

고급 사용자의 경우 브라우저의 `encodeURIComponent()` 함수를 사용하여 **JSON 인코딩** 접두사를 **URL 인코딩** 접두사로 변환할 수 있습니다. 웹 검사기 콘솔을 열고(*개발자 > *Chrome의 JavaScript 웹 콘솔) 다음과 같이 입력하면 됩니다.

```js
encodeURIComponent("<your json-encoded prefix goes here>")
```

Enter 키를 누릅니다. 생성된 값은 *URL 인코딩 *버전입니다. 예를 들면 다음과 같습니다.

```js
encodeURIComponent("\u0016\u0003\u0001\u0000\u00a8\u0001\u0001")
'%16%03%01%00%C2%A8%01%01'
```
