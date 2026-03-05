---
title: "Disguise Connections as Web Traffic with Shadowsocks-over-WebSockets"
sidebar_label: "WebSockets"
---

*Klient Outline – wersja 1.15.0+*

W tym przewodniku znajdziesz szczegółowe instrukcje, które pomogą Ci wdrożyć Shadowsocks-over-WebSockets, silną metodę omijania cenzury w środowiskach, w których blokowane są standardowe połączenia Shadowsocks. Hermetyzując ruch Shadowsocks wewnątrz WebSockets, możesz upozorować, że jest to standardowy ruch internetowy, zwiększając dzięki temu odporność i dostępność.

## Krok 1. Skonfiguruj i uruchom serwer Outline

Utwórz nowy plik `config.yaml` o następującej konfiguracji:

```yaml
web:
  servers:
    - id: server1
        listen: 127.0.0.1:<WEB_SERVER_PORT>

services:
  - listeners:
      - type: websocket-stream
        web_server: server1
        path: /<TCP_PATH>
      - type: websocket-packet
        web_server: server1
        path: /<UDP_PATH>
    keys:
      - id: 1
        cipher: chacha20-ietf-poly1305
        secret: <SHADOWSOCKS_SECRET>
```

Pobierz najnowszy [`outline-ss-server`](https://github.com/Jigsaw-Code/outline-ss-server/releases) i uruchom go za pomocą utworzonej konfiguracji.

```sh
outline-ss-server -config=config.yaml
```

## Krok 2. Udostępnij serwer WWW

Aby Twój serwer WWW WebSocket stał się dostępny publicznie, musisz udostępnić go w internecie i skonfigurować [protokół TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security).
Możesz to zrobić na kilka sposobów. Możesz wykorzystać lokalny serwer WWW, taki jak [Caddy](https://caddyserver.com/), [nginx](https://nginx.org/) lub [Apache](https://httpd.apache.org/), pod warunkiem, że ma odpowiedni certyfikat TLS, lub skorzystać z usługi tunelowania, takiej jak [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) lub [ngrok](https://ngrok.com/).

### Przykład z wykorzystaniem TryCloudflare

W tym przykładzie pokażemy, jak za pomocą [TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/) utworzyć szybki tunel. To wygodny i bezpieczny sposób na udostępnienie lokalnego serwera WWW bez konieczności otwierania portów przychodzących.

1. Pobierz i zainstaluj [`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).

2. Utwórz tunel skierowany na port Twojego lokalnego serwera WWW:

```sh
cloudflared tunnel --url http://127.0.0.1:<WEB_SERVER_PORT>
```

Cloudflare stworzy subdomenę (np.
`acids-iceland-davidson-lb.trycloudflare.com`) zapewniającą dostęp do punktu końcowego WebSocket i automatycznie zajmie się protokołem TLS. Pamiętaj o tej subdomenie, ponieważ będzie Ci ona potrzebna później.

## Krok 3. Utwórz dynamiczny klucz dostępu

Wygeneruj plik YAML z kluczem dostępu klienta dla użytkowników korzystających z formatu [konfiguracji klucza dostępu](../management/config) i uwzględnij punkty końcowe WebSocket skonfigurowane wcześniej po stronie serwera:

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN>/<TCP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>

  udp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN>/<UDP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>
```

Po wygenerowaniu pliku YAML z dynamicznym kluczem dostępu musisz dostarczyć go swoim użytkownikom. Możesz hostować plik na statycznym hostingu WWW lub generować go dynamicznie. Dowiedz się więcej o [dynamicznych kluczach dostępu](../management/dynamic-access-keys).

## Krok 4. Połącz się z klientem Outline

Skorzystaj z jednej z oficjalnych aplikacji [klienta Outline](../../download-links) (wersja 1.15.0 i nowsze) i dodaj swój nowo utworzony klucz dostępu jako wpis serwera. Kliknij **Połącz**, aby rozpocząć tunelowanie do swojego serwera za pomocą konfiguracji Shadowsocks-over-Websocket.

Skorzystaj z narzędzia, takiego jak [IPInfo](https://ipinfo.io), aby potwierdzić, że przeglądasz internet za pomocą swojego serwera Outline.
