---
title: "Deploy with Automatic HTTPS Using Caddy"
sidebar_label: "HTTPS with Caddy"
---

W tym przewodniku znajdziesz informacje o tym, jak korzystać z [Caddy](https://caddyserver.com/), zaawansowanego i przyjaznego dla użytkownika serwera WWW, aby udoskonalić konfigurację serwera Outline. Funkcje serwera Caddy dotyczące [automatycznego protokołu HTTPS](https://caddyserver.com/docs/automatic-https) oraz jego elastyczna konfiguracja sprawiają, że jest to doskonały wybór do obsługi serwera Outline, zwłaszcza w przypadku korzystania z transportu webSocket.

## Czym jest serwer Caddy? {#what_is_caddy}

Caddy to serwer WWW na licencji open source znany z łatwości użytkowania, automatycznego protokołu HTTPS i obsługi wielu różnych protokołów. Upraszcza konfigurację serwera WWW i zapewnia funkcje takie jak:

- **Automatyczny protokół HTTPS:** Caddy automatycznie uzyskuje i odnawia certyfikaty TLS, zapewniając tym samym bezpieczne połączenia.

- **Obsługa HTTP/3:** Caddy obsługuje najnowszy protokół HTTP/3, co przekłada się na szybszy i wydajniejszy ruch w sieci.

- **Rozszerzalność za pomocą wtyczek:** Caddy można rozszerzyć za pomocą wtyczek o różne funkcje, w tym odwrotne serwery proxy i równoważenie obciążenia.

## Krok 1. Wymagania wstępne {#step_1_prerequisites}

- Pobierz i zainstaluj [`xcaddy`](https://github.com/caddyserver/xcaddy).

## Krok 2. Skonfiguruj domenę {#step_2_configure_your_domain}

Przed uruchomieniem serwera Caddy upewnij się, że nazwa Twojej domeny jest poprawnie skonfigurowana, tak aby wskazywała na adres IP Twojego serwera.

- **Ustaw rekordy A/AAAA:** zaloguj się do swojego dostawcy DNS i skonfiguruj rekordy A i AAAA dla swojej domeny, tak aby wskazywały odpowiednio na adresy IPv4 i IPv6 Twojego serwera.

- **Sprawdź rekordy DNS:** sprawdź, czy Twoje rekordy DNS są ustawione poprawnie, za pomocą wyszukiwania autorytatywnego:

```sh
curl "https://cloudflare-dns.com/dns-query?name=<DOMAIN_NAME>&type=A" \
  -H "accept: application/dns-json"
```

## Krok 3. Utwórz i uruchom odpowiedni serwer Caddy {#build-and-run}

Korzystając z `xcaddy`, możesz skompilować spersonalizowany plik binarny `caddy` zawierający główny moduł serwera Outline i inne moduły rozszerzenia serwera, które są potrzebne.

```sh
xcaddy build \
  # The example uses a YAML config, so include a YAML config adapter module.
  --with github.com/iamd3vil/caddy_yaml_adapter \
  # The Outline core server module.
  --with github.com/OutlineFoundation/outline-ss-server/outlinecaddy
```

## Krok 4. Skonfiguruj i uruchom serwer Caddy z Outline {#step_4_configure_and_run_the_caddy_server_with_outline}

Utwórz nowy plik `config.yaml` o następującej konfiguracji:

```yaml
apps:
  http:
    servers:
      server1:
        listen:
          - ":443"
        routes:
          - match:
            - host:
              - <DOMAIN_NAME>
            - path:
              - /<TCP_PATH>
            handle:
            - handler: websocket2layer4
              type: stream
              connection_handler: ss1
          - match:
            - host:
              - <DOMAIN_NAME>
            - path:
              - /<UDP_PATH>
            handle:
              - handler: websocket2layer4
                type: packet
                connection_handler: ss1
  outline:
    shadowsocks:
      replay_history: 10000
    connection_handlers:
      - name: ss1
        handle:
          handler: shadowsocks
          keys:
            - id: user-1
              cipher: chacha20-ietf-poly1305
              secret: <SHADOWSOCKS_SECRET>
```

Ta konfiguracja reprezentuje strategię Shadowsocks-over-WebSockets z serwerem WWW nasłuchującym na porcie `443`, przyjmującym spakowany ruch protokołów Shadowsocks TCP i UDP odpowiednio przy ścieżkach `TCP_PATH` i `UDP_PATH`.

Uruchom serwer Caddy rozszerzony za pomocą Outline, korzystając z utworzonej konfiguracji:

```sh
caddy run --config config.yaml --adapter yaml --watch
```

Więcej przykładów konfiguracji znajdziesz w naszym [repozytorium GitHub outline-ss-server/outlinecaddy](https://github.com/OutlineFoundation/outline-ss-server/tree/master/outlinecaddy/examples).

## Krok 5. Utwórz dynamiczny klucz dostępu {#step_5_create_a_dynamic_access_key}

Wygeneruj plik YAML z kluczem dostępu klienta dla użytkowników korzystających z formatu [zaawansowanej konfiguracji](../management/config) i uwzględnij punkty końcowe WebSocket skonfigurowane po stronie serwera:

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN_NAME>/<TCP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>

  udp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN_NAME>/<UDP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>
```

Po wygenerowaniu pliku YAML z dynamicznym kluczem dostępu musisz dostarczyć go swoim użytkownikom. Możesz hostować plik na statycznym hostingu WWW lub generować go dynamicznie. Dowiedz się więcej o [dynamicznych kluczach dostępu](../management/dynamic-access-keys).

## Krok 6. Połącz się z klientem Outline {#step_6_connect_with_the_outline_client}

Skorzystaj z jednej z oficjalnych aplikacji [klienta Outline](../../download-links) (wersja 1.15.0 i nowsze) i dodaj swój nowo utworzony dynamiczny klucz dostępu jako wpis serwera. Kliknij **Połącz**, aby rozpocząć tunelowanie do swojego serwera za pomocą konfiguracji Shadowsocks-over-Websocket.

Skorzystaj z narzędzia takiego jak [IPInfo](https://ipinfo.io), aby potwierdzić, że przeglądasz internet za pomocą swojego serwera Outline.
