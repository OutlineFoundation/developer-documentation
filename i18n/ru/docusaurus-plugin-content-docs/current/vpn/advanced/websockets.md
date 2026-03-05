---
title: "Disguise Connections as Web Traffic with Shadowsocks-over-WebSockets"
sidebar_label: "WebSockets"
---

*Для клиента Outline 1.15.0 или более поздних версий*

Это руководство содержит подробные инструкции по реализации Shadowsocks-over-WebSockets – мощного метода обхода цензуры в ситуациях, когда стандартные подключения Shadowsocks блокируются. Инкапсулируя трафик Shadowsocks в WebSockets, вы можете замаскировать его под обычный веб-трафик, повысив устойчивость и доступность соединения.

## Шаг 1. Настройте и запустите сервер Outline

Создайте новый файл `config.yaml` со следующей конфигурацией:

Скачайте последнюю версию [`outline-ss-server`](https://github.com/Jigsaw-Code/outline-ss-server/releases) и запустите ее с созданной конфигурацией.

## Шаг 2. Настройте доступ к веб-серверу

Чтобы сделать веб-сервер WebSocket общедоступным, необходимо настроить на нем внешний доступ и включить [TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security).
Вы можете использовать для этого указанные ниже способы. Можно настроить локальный веб-сервер (например, [Caddy](https://caddyserver.com/), [nginx](https://nginx.org/) или [Apache](https://httpd.apache.org/)) с действующим TLS-сертификатом или использовать сервис туннелирования (например, [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) или [ngrok](https://ngrok.com/)).

### Пример использования TryCloudflare

В этом примере мы покажем, как быстро создать туннель с помощью [TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/). Это удобный и безопасный способ настроить внешний доступ на локальном веб-сервере без необходимости открывать входящие порты.

1. 

Скачайте и установите [`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).

2. 

Создайте туннель, указав порт вашего локального веб-сервера:

Cloudflare предоставит субдомен
(например, `acids-iceland-davidson-lb.trycloudflare.com`), который позволит подключиться к конечной точке WebSocket и автоматически настроить TLS. Сохраните этот субдомен, так как он понадобится вам позже.

## Шаг 3. Создайте динамический ключ доступа

Сгенерируйте YAML-файл с ключами доступа для пользователей, используя [указанный в этой статье формат](../management/config). Включите в файл конечные точки WebSocket, настроенные на сервере.

После создания YAML-файла с динамическим ключом доступа его нужно передать пользователям. Вы можете разместить файл на статическом веб-хостинге или настроить динамическую генерацию. Подробнее о том, [как использовать динамические ключи доступа](../management/dynamic-access-keys)…

## Шаг 4. Подключитесь к клиенту Outline

Используйте официальное приложение [клиента Outline](../../download-links) 1.15.0 или более поздних версий и добавьте созданный динамический ключ доступа в список серверов. Нажмите **Подключить**, чтобы начать туннелирование трафика через сервер с конфигурацией Shadowsocks-over-Websocket.

Чтобы убедиться, что трафик проходит через ваш сервер Outline, воспользуйтесь инструментом [IPInfo](https://ipinfo.io).
