---
title: "Конфигурация Smart Dialer"
sidebar_label: "Конфигурация Smart Dialer"
---

**Smart Dialer** подбирает стратегию, которая позволяет обойти блокировки DNS и TLS для заданного списка тестовых доменов. Резолвер использует конфигурацию, описывающую несколько доступных стратегий.

## Конфигурация YAML для Smart Dialer {#yaml_config_for_the_smart_dialer}

Конфигурация, которую использует Smart Dialer, задается в формате YAML. Пример:

```yaml
dns:
  - system: {}
  - https:
      name: 8.8.8.8
  - https:
      name: 9.9.9.9
tls:
  - ""
  - split:2
  - tlsfrag:1

fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

### Конфигурация DNS {#dns_configuration}

- Поле `dns` указывает список DNS-резолверов, которые необходимо протестировать.

- Каждый DNS-резолвер может относиться к одному из следующих типов:

    - `system`: используется системный резолвер. Указывается как пустой объект.

    - `https`: используется зашифрованный резолвер DNS-over-HTTPS (DoH).

    - `tls`: используется зашифрованный резолвер DNS over TLS (DoT).

    - `udp`: используется UDP-резолвер.

    - `tcp`: используется TCP-резолвер.

#### Резолвер DNS-over-HTTPS (DoH) {#dns-over-https_resolver_doh}

```yaml
https:
  name: dns.google
  address: 8.8.8.8
```

- `name`: доменное имя сервера DoH.

- `address`: адрес сервера в формате host:port. Значение по умолчанию – `name`:443.

#### Резолвер DNS-over-TLS (DoT) {#dns-over-tls_resolver_dot}

```yaml
tls:
  name: dns.google
  address: 8.8.8.8
```

- `name`: доменное имя сервера DoT.

- `address`: адрес сервера в формате host:port. Значение по умолчанию – `name`:853.

#### UDP-резолвер {#udp_resolver}

```yaml
udp:
  address: 8.8.8.8
```

- `address`: адрес резолвера в формате host:port.

#### TCP-резолвер {#tcp_resolver}

```yaml
tcp:
  address: 8.8.8.8
```

- `address`: адрес резолвера в формате host:port.

### Конфигурация TLS {#tls_configuration}

- Поле `tls` указывает список протоколов TLS, которые необходимо протестировать.

- Каждый протокол задается строкой, определяющей используемую технологию.

- Например, `override:host=cloudflare.net|tlsfrag:1` обозначает протокол, использующий доменное прикрытие с Cloudflare и фрагментацию TLS. Подробная информация приведена в [документации по конфигурации](https://pkg.go.dev/github.com/OutlineFoundation/outline-sdk/x/configurl#hdr-Config_Format).

### Резервная конфигурация {#fallback_configuration}

Резервная конфигурация используется, если ни одна из стратегий без прокси-сервера не сработала. Например, можно указать резервный прокси-сервер, через который будет предпринята попытка подключения. Использование резервной конфигурации приведет к более медленному запуску, поскольку сначала должны завершиться неудачей или по таймауту все попытки по DNS- и TLS-стратегиям.

Допустимые строки для резервной конфигурации:

- Допустимая строка конфигурации `StreamDialer`, как определено в [`configurl`](https://pkg.go.dev/github.com/OutlineFoundation/outline-sdk/x/configurl#hdr-Proxy_Protocols).

- Допустимый объект конфигурации Psiphon, вложенный в поле `psiphon`.

#### Пример сервера Shadowsocks {#shadowsocks_server_example}

```yaml
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

#### Пример сервера SOCKS5 {#socks5_server_example}

```yaml
fallback:
  - socks5://[USERINFO]@[HOST]:[PORT]
```

#### Пример конфигурации Psiphon {#psiphon_config_example}

Чтобы использовать сеть [Psiphon](https://psiphon.ca/), необходимо:

1. Связаться с командой Psiphon, чтобы получить конфигурацию для доступа к их сети. Возможно, для этого потребуется заключить договор.

2. Добавить полученную конфигурацию Psiphon в раздел `fallback` конфигурации Smart Dialer. Поскольку JSON-файл совместим с YAML, вы можете вставить конфигурацию Psiphon напрямую в раздел `fallback`, например:

```yaml
fallback:
  - psiphon: {
      "PropagationChannelId": "FFFFFFFFFFFFFFFF",
      "SponsorId": "FFFFFFFFFFFFFFFF",
      "DisableLocalSocksProxy" : true,
      "DisableLocalHTTPProxy" : true,
      ...
    }
```


:::note
Кодовая база Psiphon распространяется под лицензией GPL, которая может ограничивать использование вашего кода. Рассмотрите возможность получения специальной лицензии у команды Psiphon.
:::

### Как использовать Smart Dialer {#how_to_use_the_smart_dialer}

Чтобы использовать Smart Dialer, создайте объект `StrategyFinder` и вызовите метод `NewDialer`, передав список тестовых доменов и YAML-конфигурацию.
Метод `NewDialer` вернет `transport.StreamDialer`, с помощью которого можно будет создавать подключения с использованием подобранной стратегии. Например:

```go
finder := &smart.StrategyFinder{
    TestTimeout:  5 * time.Second,
    LogWriter:   os.Stdout,
    StreamDialer: &transport.TCPDialer{},
    PacketDialer: &transport.UDPDialer{},
}

configBytes := []byte(`
dns:
  - system: {}
  - https:
      name: 8.8.8.8
  - https:
      name: 9.9.9.9
tls:
  - ""
  - split:2
  - tlsfrag:1
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
`)

dialer, err := finder.NewDialer(
  context.Background(),
  []string{"www.google.com"},
  configBytes
)
if err != nil {
    // Handle error.
}

// Use dialer to create connections.
```

Это базовый пример, который при необходимости можно адаптировать под ваш сценарий использования.
