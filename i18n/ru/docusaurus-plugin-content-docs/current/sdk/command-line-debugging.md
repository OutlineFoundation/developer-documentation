---
title: "Удаленная характеристика и обход сетевых помех с помощью Outline SDK"
sidebar_label: "Удаленная характеристика и обход сетевых помех с помощью Outline SDK"
---

В этом руководстве показано, как использовать инструменты командной строки Outline SDK для понимания и обхода сетевых помех с удаленной точки зрения. Вы узнаете, как использовать инструменты SDK для измерения сетевых помех, тестирования стратегий обхода и анализа результатов. В этом руководстве основное внимание будет уделено инструментам `resolve` , `fetch` и `http2transport` .

##  Начало работы с инструментами Outline SDK

 Вы можете начать использовать инструменты Outline SDK прямо из командной строки.

###  Решить DNS

 Инструмент `resolve` позволяет выполнять DNS-поиск с помощью указанного преобразователя.

 Чтобы разрешить запись A домена:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type A 1.2.3.4.nip.io
```

 Чтобы разрешить запись CNAME:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type CNAME www.google.com
```

###  Получить веб-страницу

 Инструмент `fetch` можно использовать для извлечения содержимого веб-страницы.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest https://example.com
```

 Он также может принудительно перевести соединение на использование QUIC.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -proto=h3 https://www.youtube.com
```

###  Используйте локальный прокси-сервер

 Инструмент `http2transport` создает локальный прокси для маршрутизации вашего трафика. Чтобы запустить локальный прокси с транспортом Shadowsocks:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/http2transport@latest -localAddr 127.0.0.1:8080 -transport "ss://{your_shadowsocks_credentials}"
```

 Затем вы можете использовать этот прокси с другими инструментами, такими как curl:

```sh
curl -p -x http://127.0.0.1:8080 https://ipinfo.io
```

##  Укажите стратегии обхода

 Outline SDK позволяет специфицировать различные стратегии обхода, которые можно комбинировать для обхода различных форм сетевых помех. Спецификация этих стратегий находится в [документации go](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl) .

###  Компонуемые стратегии

 Эти стратегии можно комбинировать для создания более надежных методов обхода.
*  **DNS-over-HTTPS с фрагментацией TLS** : `doh:name=cloudflare-dns.com&address=cloudflare.net:443 | tlsfrag:1`
*  **SOCKS5-over-TLS с доменным фронтингом** : `tls:sni=decoy.example.com&certname=[HOST] | socks5:[HOST]:[PORT]`
*  **Многоадресная маршрутизация с помощью Shadowsocks** : `ss://[USERINFO1]@[HOST1]:[PORT1] | ss://[USERINFO2]@[HOST2]:[PORT2] | ss://[USERINFO3]@[HOST3]:[PORT3]`

##  Удаленный доступ и измерение
 Для измерения помех в сети, которые испытываются в разных регионах, вы можете использовать удаленные прокси-серверы. Вы можете найти или создать удаленные прокси-серверы для подключения.

###  Параметры удаленного доступа

 Используя инструмент `fetch` , вы можете удаленно тестировать соединения различными способами.

####  Сервер Outline

 Удаленное подключение к стандартному серверу Outline с помощью транспорта Shadowsocks.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "ss://{remote_shadowsocks_credentials}" https://ipinfo.io | jq
```

####  SOCKS5 через SSH

 Создайте прокси SOCKS5 с использованием туннеля SSH.

```sh
ssh -D 127.0.0.1:1080 -C -N $USER@$HOST:$PORT
```

 Подключитесь к этому туннелю с помощью fetch

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "socks5://localhost:1080" https://ipinfo.io | jq
```

##  Пример из практики: обход блокировки YouTube в Иране

 Вот практический пример обнаружения и обхода сетевых помех.

###  Определить блок

 При попытке загрузить домашнюю страницу YouTube через иранский прокси-сервер время ожидания запроса истекает, что указывает на блокировку. 

```sh
export TRANSPORT="ss://{remote_shadowsocks_credentials}"
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)" https://www.youtube.com
```

Эта команда завершается сбоем из-за тайм-аута.

###  Обход с фрагментацией TLS

 Добавив фрагментацию TLS к транспорту, мы можем обойти эту блокировку. 

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)|tlsfrag:1" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Эта команда успешно извлекает заголовок домашней страницы YouTube: `<title>YouTube</title>` . 

###  Обход с помощью фрагментации TLS и DNS-over-HTTPS 

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|tlsfrag:1|doh:name=cloudflare-dns.com&address=www.cloudflare.net" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Это также успешно возвращает `<title>YouTube</title>` .

###  Обход с помощью сервера Outline 

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|ss://<your_shadowsocks_credentials>" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Это также возвращает `<title>YouTube</title>` .

##  Дополнительный анализ и ресурсы

 Для обсуждений и вопросов посетите [группу обсуждения Outline SDK](https://github.com/OutlineFoundation/outline-sdk/discussions) .
