---
title: "Dynamic Access Keys"
sidebar_label: "Dynamic Access Keys"
---

Outline에서는 두 가지 유형의 액세스 키, 즉 정적 액세스 키와 동적 액세스 키를 제공합니다. 정적 키는 키 자체 내에서 모든 연결 정보를 인코딩하지만, 동적 키는 연결 정보의 위치를 인코딩하므로 정보를 원격으로 저장하고 필요에 따라 변경할 수 있습니다. 즉, 새 키를 생성하여 사용자에게 배포할 필요 없이 서버 구성을 업데이트할 수 있습니다. 이 문서에서는 동적 액세스 키를 사용하여 Outline 서버를 더 유연하고 효율적으로 관리하는 방법을 설명합니다.

동적 액세스 키에서 사용할 액세스 정보는 세 가지 형식으로 지정할 수 있습니다.

### `ss://` 링크 사용

*Outline 클라이언트 v1.8.1+*

기존 `ss://` 링크를 직접 사용할 수 있습니다. 이 방법은 서버나 포트, 암호화 방법을 자주 바꾸지 않아도 되지만 유연하게 서버 주소를 업데이트하려는 경우에 적합합니다.

**예:**

### JSON 객체 사용

*Outline 클라이언트 v1.8.0+*

이 방법을 사용하면 사용자의 Outline 연결의 모든 측면을 더 유연하게 관리할 수 있습니다. 이 방법으로 서버와 포트, 비밀번호, 암호화 방법을 업데이트할 수 있습니다.

**예:**

- **server:** VPN 서버의 도메인이나 IP 주소입니다.

- **server_port:** VPN 서버가 실행되는 포트 번호입니다.

- **password:** VPN에 연결하는 데 필요한 비밀번호입니다.

- **method:** VPN에서 사용하는 암호화 방법입니다. Shadowsocks 지원 [AEAD 암호화](https://shadowsocks.org/doc/aead.html)를 참고하세요.

### YAML 객체 사용

*Outline 클라이언트 v1.15.0+*

이 방법은 앞서 언급한 JSON을 사용하는 방법과 비슷하지만, Outline의 고급 구성 형식을 활용하므로 더욱 유연합니다. 서버와 포트, 비밀번호, 암호화 방법 등을 업데이트할 수 있습니다.

**예:**

- **transport:** 사용할 전송 프로토콜을 정의합니다(여기서는 TCP, UDP).

- **tcp/udp:** 각 프로토콜의 구성을 지정합니다.

    - **$type:** 구성 유형을 나타냅니다. 여기서는 shadowsocks입니다.

    - **endpoint:** VPN 서버의 도메인이나 IP 주소 및 포트입니다.

    - **secret:** VPN에 연결하는 데 필요한 비밀번호입니다.

    - **cipher:** VPN에서 사용하는 암호화 방법입니다. Shadowsocks 지원 [AEAD 암호화](https://shadowsocks.org/doc/aead.html)를 참고하세요.

전송, 엔드포인트, 다이얼러, 패킷 리스너 등 Outline 서버에 대한 액세스를 구성할 수 있는 모든 방법에 관한 자세한 내용은 [액세스 키 구성](config)을 참고하세요.

## 정적 키에서 액세스 정보 추출

기존의 정적 액세스 키가 있다면 정보를 추출하여 JSON 또는 YAML 기반 동적 액세스 키를 만들 수 있습니다. 정적 액세스 키는 다음 패턴을 따릅니다.

예:

- **서버:** `outline-server.example.com`

- **서버 포트:** `8388`

- 

**사용자 정보:** `Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl` [Google 관리 콘솔 도구 상자 인코딩/디코딩](https://toolbox.googleapps.com/apps/encode_decode/)과 같은 도구를 사용하여 [base64](https://en.wikipedia.org/wiki/Base64)로 디코딩됨

    - **방법**: `chacha20-ietf-poly1305`

    - **비밀번호**: `example`

## 호스팅 플랫폼 선택

이제 동적 액세스 키를 만드는 방법을 알아봤으므로 액세스 키 구성에 적합한 호스팅 플랫폼을 선택하는 것이 중요합니다. 선택할 때는 플랫폼의 안정성, 보안, 사용 용이성, 검열 방지와 같은 요소를 고려하세요. 플랫폼에서 다운타임 없이 액세스 키 정보를 지속적으로 제공하는지, 구성을 보호하기 위해 적절한 보안 조치를 제공하는지, 플랫폼에서 액세스 키 정보를 얼마나 쉽게 관리할 수 있는지, 인터넷 검열이 있는 지역에서 플랫폼에 액세스할 수 있는지 고려해야 합니다.

정보에 대한 액세스가 제한될 수도 있는 상황에서는 [Google Drive](https://drive.google.com), [pad.riseup.net](https://pad.riseup.net/), [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html)(path-style 액세스 포함), [Netlify](https://dev.to/alexmercedcoder/delivering-json-data-with-netlify-1j96) 또는 [GitHub secret gists](https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists/creating-gists)와 같은 검열 방지 플랫폼에서 호스팅하는 것이 좋습니다.
배포의 특정 요구사항을 평가하고 접근성 및 보안 요구사항에 맞는 플랫폼을 선택하세요.
