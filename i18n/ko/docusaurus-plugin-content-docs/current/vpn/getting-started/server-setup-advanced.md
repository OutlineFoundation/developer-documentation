---
title: "설치 스크립트를 사용하여 배포하기"
sidebar_label: "설치 스크립트를 사용하여 배포하기"
---

이 가이드에서는 안전하고 제한 없는 인터넷 액세스를 제공하기 위해 Outline 서버를 설정하는 과정을 안내합니다.

## 기본 요건 {#prerequisites}

- 지원되는 운영체제(Ubuntu 20.04 LTS 또는 Debian 10)를 실행하는 서버(실제 또는 가상)

- 서버에 대한 루트 또는 sudo 액세스

## 안내 {#instructions}

1. Outline 설치 스크립트를 다운로드하여 실행합니다.

```sh
sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/OutlineFoundation/outline-apps/master/server_manager/install_scripts/install_server.sh)"
```

2. 화면에 표시되는 안내를 따릅니다.
