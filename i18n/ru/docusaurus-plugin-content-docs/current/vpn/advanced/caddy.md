---
title: "Caddy с автоматическим HTTPS"
sidebar_label: "Caddy с автоматическим HTTPS"
---

В этом руководстве объясняется, как использовать [Caddy](https://caddyserver.com/) – мощный и удобный веб-сервер – для расширенной настройки сервера Outline. [Автоматическое использование HTTPS](https://caddyserver.com/docs/automatic-https) и возможности гибкой настройки делают Caddy отличным решением для обслуживания сервера Outline, особенно если он работает на базе протокола WebSocket.

## Что такое Caddy? {#what_is_caddy}

Caddy – это веб-сервер с открытым исходным кодом, который отличается простотой настройки, автоматическим использованием HTTPS и поддержкой различных протоколов. Он упрощает настройку веб-сервера и предлагает следующие функции:

- **Автоматическое использование HTTPS.** Caddy автоматически получает и обновляет сертификаты TLS, обеспечивая защищенное подключение.

- **Поддержка HTTP/3.** Caddy поддерживает последний протокол HTTP/3 для более быстрой и эффективной передачи веб-трафика.

- **Расширяемость с помощью плагинов.** Вы можете добавить в Caddy такие функции, как обратный прокси и балансировщик нагрузки.

## Шаг 1. Выполните подготовку {#step_1_prerequisites}

- Скачайте и установите [`xcaddy`](https://github.com/caddyserver/xcaddy).

## Шаг 2. Настройте свой домен {#step_2_configure_your_domain}

Перед запуском Caddy проверьте, что доменное имя настроено правильно и указывает на IP-адрес вашего сервера.

- **Настройте записи A и AAAA.** Войдите в аккаунт на сайте вашего поставщика услуг DNS и укажите IPv4-адрес  (запись A) и IPv6-адрес сервера (запись AAAA).

- **Проверьте записи DNS.** Чтобы убедиться, что записи настроены правильно, выполните следующий запрос:

```sh
curl "https://cloudflare-dns.com/dns-query?name=<DOMAIN_NAME>&type=A" \
  -H "accept: application/dns-json"
```

## Шаг 3. Создайте и запустите специальную сборку Caddy {#build-and-run}

С помощью `xcaddy` можно собрать специальный исполняемый файл `caddy`, содержащий модуль основного сервера Outline и другие необходимые модули расширений.

```sh
xcaddy build \
  # The example uses a YAML config, so include a YAML config adapter module.
  --with github.com/iamd3vil/caddy_yaml_adapter \
  # The Outline core server module.
  --with github.com/OutlineFoundation/outline-ss-server/outlinecaddy
```

## Шаг 4. Настройте и запустите сервер Caddy с Outline {#step_4_configure_and_run_the_caddy_server_with_outline}

Создайте файл `config.yaml` со следующей конфигурацией:

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

:::warning[Important]
Чтобы избежать автоматического сканирования и возможных атак, держите значение `path` в секрете. Оно выполняет роль секретной конечной точки. Рекомендуется использовать длинный, случайно сгенерированный путь.
:::


Эта конфигурация реализует модель Shadowsocks-over-WebSockets, где веб-сервер прослушивает порт `443` и принимает трафик TCP и UDP, упакованный в трафик Shadowsocks, по путям `TCP_PATH` и `UDP_PATH` соответственно.

Запустите Caddy с Outline, используя созданный ранее файл конфигурации:

```sh
caddy run --config config.yaml --adapter yaml --watch
```

:::note
В примере используется формат YAML, поскольку он удобнее для чтения и добавления комментариев. Однако вы также можете использовать формат JSON (основной формат конфигурации Caddy). Если вы используете этот формат, Caddy можно запускать без флага `--adapter yaml` и удалить адаптер YAML из зависимостей на этапе сборки и запуска.
:::


Дополнительные примеры конфигурации можно найти в нашем репозитории GitHub: [outline-ss-server/outlinecaddy](https://github.com/OutlineFoundation/outline-ss-server/tree/master/outlinecaddy/examples).

## Шаг 5. Создайте динамический ключ доступа {#step_5_create_a_dynamic_access_key}

Сгенерируйте файл YAML с ключами доступа, используя формат [расширенной конфигурации](../management/config), и добавьте конечные точки WebSocket, настроенные на сервере.

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

После создания файла YAML с динамическими ключами доступа его нужно передать пользователям. Вы можете разместить файл на статическом веб-хостинге или настроить динамическую генерацию. Подробнее о том, [как использовать динамические ключи доступа](../management/dynamic-access-keys)…

## Шаг 6. Подключитесь к клиенту Outline {#step_6_connect_with_the_outline_client}

Используйте официальное приложение [клиента Outline](../../download-links) 1.15.0 или более поздних версий и добавьте созданный динамический ключ доступа в список серверов. Нажмите **Подключить**, чтобы начать туннелирование трафика через сервер с конфигурацией Shadowsocks-over-Websocket.

Чтобы убедиться, что трафик проходит через ваш сервер Outline, воспользуйтесь инструментом [IPInfo](https://ipinfo.io).
