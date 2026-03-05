---
title: "Use a Domain Name with Floating IPs"
sidebar_label: "Domain with Floating IPs"
---

## 소개

Outline 서버는 때때로 고도로 검열된 네트워크에서 검색되어 차단되는 문제가 발생할 수 있습니다. 올바로 설정된 경우 차단된 서버를 복구할 수 있으며 어렵지도 않습니다. 도메인 이름(예: `getoutline.org`)을 실제 IP 주소(예: `216.239.36.21`)로 변환하는 인터넷 기술인 DNS와 Outline 서버에 IP 주소를 두 개 이상 할당할 수 있는 클라우드 기능인 Floating IP를 사용하면 됩니다.

## 요구사항

이 가이드를 따르는 데는 높은 수준의 기술 지식이 필요하지 않습니다. DNS를 기본적으로 알고 있으면 도움이 되나 필수는 아닙니다. 소개를 보려면 도메인 이름에 관한 [MDN](https://developer.mozilla.org/docs/Learn/Common_questions/What_is_a_domain_name) 가이드를 참고하세요.

구체적인 예를 제공하기 위해 여기서는 DigitalOcean과 Google Domains를 사용하지만 IP 주소 할당을 허용하는 클라우드 제공업체(예: Google Cloud 또는 [AWS Lightsail](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/lightsail-create-static-ip))와 도메인 등록기관(예: [AWS Route 53](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-using-route-53-to-point-a-domain-to-an-instance))을 사용해도 됩니다.

## 안내

1. 

다음 목록에서는 서버의 IP 주소를 순환하는 단계를 요약합니다.

2. 

도메인 이름을 구매합니다.

3. 

도메인 이름이 서버의 IP 주소를 가리키도록 합니다.

4. 

도메인 이름을 사용하여 액세스 키를 발급합니다.

5. 

서버의 Droplet에 Floating IP를 할당합니다.

6. 

새 IP 주소를 가리키도록 도메인 이름을 변경합니다.

## DigitalOcean에서 Outline 서버 만들기

실행 중인 DigitalOcean 서버가 있는 경우 다음 단계로 건너뜁니다.

1. 

Outline Manager를 열고 왼쪽 하단에서 '+' 기호를 클릭하면 서버 생성 화면이 열립니다.

2. 

'DigitalOcean' 버튼에서 'Create Server'(서버 만들기)를 클릭하고 앱의 지시를 따릅니다.

![서버 만들기](/images/create-DO-server.png)

## 서버의 호스트 이름 만들기

1. 

[Google Domains](https://domains.google.com/m/registrar/)로 이동하여 '완벽한 도메인 찾기'를 클릭합니다.

2. 

검색창에 도메인 이름을 입력하고 이름을 선택합니다. 여기서는 `outlinedemo.info`를 예시로 사용했습니다.

3. 

Google Domains의 DNS 탭으로 이동합니다. '맞춤 리소스 레코드'에서 'IPV4 주소'라고 표시된 필드에 서버의 IP 주소를 입력합니다.

4. 

Outline Manager에서 서버의 'Settings'(설정) 탭으로 이동합니다. 'Hostname'(호스트 이름)에서 구매한 호스트 이름을 입력하고 'SAVE'(저장)를 클릭합니다. 이렇게 하면 향후 모든 액세스 키에서 서버의 IP 주소 대신 이 호스트 이름을 사용하게 됩니다.

![호스트 이름을 설정합니다.](/images/set-hostname.png)

## 서버의 IP 주소 변경

1. 

DigitalOcean의 'Droplets' 페이지에서 서버로 이동합니다.

2. 

창 오른쪽 상단에서 'Floating IP' 옆에 있는 'Enable Now'(지금 사용 설정)를 클릭합니다.

![Floating IP 사용 설정](/images/floating-ip-DO.png)

1. Droplets 목록에서 서버를 찾아 'Assign Floating IP'(Floating IP 할당)를 클릭합니다.

![Floating IP 할당](/images/assign-floating-ip-DO.png)

1. 

Google Domains의 DNS 탭으로 다시 이동합니다.

2. 

이전과 같이 IP 주소를 변경하지만 이번에는 새로운 Floating IP 주소를 사용합니다. 이 작업에는 최대 48시간이 걸릴 수 있지만 대개는 몇 분밖에 걸리지 않습니다.

3. 

[Google의 온라인 DNS 도구](https://toolbox.googleapps.com/apps/dig/#A/)로 이동하여 도메인 이름을 입력하면 마지막 단계에서 변경이 발생한 시점을 확인할 수 있습니다.

![Google DNS 도구에서 도메인 검색](/images/google-dns.png)

이 변경사항이 전파되면 이제 클라이언트가 새 IP 주소에 연결됩니다. 새 키를 사용하여 서버에 연결하고 <https://ipinfo.io>를 열어 서버의 새 IP 주소가 표시되는지 확인할 수 있습니다.

결론. Outline 서버의 IP 주소를 순환하는 방법을 통해 빠르게 서버 차단을 해제하고 클라이언트에 대한 서비스를 복원할 수 있습니다. 궁금한 점이 있다면 [공지사항 게시물](https://redd.it/hrbhz4)에 댓글을 쓰거나 [Outline의 지원 페이지](https://support.getoutline.org/)를 방문하거나 [Google에 직접 문의](https://support.getoutline.org/s/contactsupport)해 주세요.
