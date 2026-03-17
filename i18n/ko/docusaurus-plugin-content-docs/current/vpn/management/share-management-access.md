---
title: "다른 사용자와 관리 액세스 권한 공유하기"
sidebar_label: "다른 사용자와 관리 액세스 권한 공유하기"
---

Outline 서비스가 확장됨에 따라 신뢰할 수 있는 다른 사용자에게 관리 책임을 위임해야 수도 있습니다. 이 문서에서는 다른 관리자와 관리 액세스 권한을 공유하는 데 사용할 수 있는 다양한 방법을 설명합니다.

관리 액세스 권한 공유 방법은 Outline 서버가 처음 배포된 방식에 따라 달라집니다.

## 클라우드 제공업체 배포 {#cloud_provider_deployments}

DigitalOcean, AWS, Google Cloud와 같은 클라우드 플랫폼에 배포된 Outline 서버의 경우, 관리 액세스 권한은 일반적으로 제공업체의 통합 ID 및 액세스 관리(IAM) 기능을 통해 처리됩니다. 이러한 방식은 수동으로 구성 정보를 공유하는 것보다 더 안전하고 체계적인 접근 방식을 제공합니다.

### DigitalOcean {#digitalocean}

DigitalOcean은 다른 DigitalOcean 사용자를 초대하여 프로젝트에서 협업할 수 있는 강력한 **Teams(팀)** 기능을 제공합니다. 이는 해당 플랫폼에 호스팅된 Outline 서버에 대한 관리 액세스 권한을 부여하는 데 권장되는 방법입니다.

#### 1. 팀 액세스 권한 부여하기 {#1_grant_team_access}

DigitalOcean에 호스팅된 Outline 서버 관리를 공유하는 가장 효과적인 방법은 DigitalOcean의 **Teams(팀)** 기능을 활용하는 것입니다.

- DigitalOcean 계정에 로그인합니다.

- **Teams(팀)** 섹션으로 이동합니다.

- 아직 팀을 만들지 않았다면 새 팀을 만들거나 기존 DigitalOcean 사용자를 팀에 초대합니다.

- 팀원을 초대할 때 해당 팀원에게 특정 역할을 할당하고 Outline을 실행하는 Droplet을 비롯한 특정 리소스에 대한 액세스 권한을 부여할 수 있습니다.

#### 2. 권한 관리하기 {#2_control_permissions}

팀원에게 부여하는 권한은 신중하게 검토해야 합니다. Outline 서버를 관리하기 위해 특정 Droplet에 대한 '읽기' 및 '쓰기' 액세스 권한을 부여할 수 있습니다. 이러한 권한을 받은 사용자는 다음과 같은 작업을 할 수 있습니다.

- Droplet의 세부정보(예: IP 주소, 상태 등) 보기

- 문제 해결이 필요한 경우 Droplet 콘솔에 액세스

- 부여된 권한 수준에 따라 Droplet 다시 시작하기와 같은 작업 수행 가능

Outline Manager를 자신의 DigitalOcean 계정에 연결한 사용자는 이제 해당 계정에 연결된 모든 Outline 서버를 보고 관리할 수 있습니다.


:::tip
새 관리자가 보안 강화를 위해 클라우드 제공업체 계정에서 다중 인증(MFA)을 사용 설정하도록 권장하세요.
:::

## 수동 설치 {#manual_installations}


:::caution
수동 설치에 대한 관리 액세스 권한을 공유하면 액세스 권한을 취소하는 것이 어려워집니다. 가장 직접적인 방법은 서버를 완전히 재설치하는 것이지만, 이 경우 구성이 새로 생성되는 동시에 모든 사용자 액세스 키도 재설정됩니다.
:::

[설치 스크립트](../getting-started/server-setup-advanced)를 사용하여 자체 서버에 Outline을 수동으로 설치한 사용자의 경우, 관리 액세스 권한을 부여하는 기본 방법은 **액세스 구성**을 공유하는 것입니다.

Outline Manager 애플리케이션이 Outline 서버에 연결하고 이를 관리하려면 특정 구성 문자열이 필요합니다. 이 구성 문자열에는 서버 주소, 포트, 인증을 위한 보안 비밀 키 등 필요한 모든 정보가 포함되어 있습니다.

### 1. `access.txt` 파일 찾기 {#1_locate_the_accesstxt_file}

Outline이 설치된 서버에서 Outline 디렉터리로 이동합니다. 정확한 위치는 설치 방법에 따라 약간씩 다를 수 있지만 일반적인 위치는 다음과 같습니다.

- `/opt/outline/access.txt`

- `/etc/outline/access.txt`

- Outline 서버 컨테이너에서 사용하는 Docker 볼륨 내부

### 2. 액세스 구성 가져오기 {#2_retrieve_the_access_config}

`access.txt` 파일을 찾은 후에는 다음 단계에서 Outline Manager가 필요로 하는 포맷인 JSON으로 파일을 변환합니다.

```sh
sed -n '2s/^apiUrl://p; 1s/^certSha256://p' /opt/outline/access.txt | paste -d'\n' -s | sed 'H;1h;$!d;x;s/\n/", \"apiUrl\": \"/g; s/^/{"certSha256": \"/; s/$/\"}/'
```

이 출력 결과에는 자체 서명된 인증서 지문(`certSha256`)과 서버의 Management API 엔드포인트(`apiUrl`)가 포함됩니다.

```json
{"certSha256": "1DCC18CC9F6C34EBBB639255F4D1BC6984C2F6A47B15F7A49AA8AFB69B7E4DDE", "apiUrl": "https://1.1.1.1:12345/Fw-CkWFNSN7Ml8LLM8Pduw"}
```


:::warning[Important]
이 줄에는 민감한 정보가 포함되어 있습니다. 관리자 액세스 권한이 필요한 신뢰할 수 있는 사용자와만 공유하세요.
:::

### 3. 액세스 권한 구성 안전하게 공유하기 {#3_share_the_access_config_securely}

출력 결과를 복사하여 신규 Outline Manager와 안전하게 공유합니다. 일반 이메일이나 채팅과 같은 암호화되지 않은 채널을 통해 전송하지 마세요.
비밀번호 관리자의 보안 공유 기능이나 다른 암호화된 통신 방법을 사용해 보세요.

제공된 **액세스 구성**을 Outline Manager에 붙여넣으면 새 관리자가 애플리케이션 인터페이스를 통해 Outline 서버를 추가하고 관리할 수 있습니다. Outline Manager 사용에 관한 추가 지원은 [Outline 고객센터](https://support.google.com/outline)를 참고하세요.
