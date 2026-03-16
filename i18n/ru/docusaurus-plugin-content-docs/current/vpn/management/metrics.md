---
title: "Access Performance Metrics"
sidebar_label: "Performance Metrics"
---

Outline позволяет получить подробную статистику использования сервера, предоставляя показатели эффективности через сервис [Prometheus](https://prometheus.io/). Из этого руководства вы узнаете, как получать и просматривать эти данные.

**Важно!** Для использования этого руководства необходимы базовые знания о Prometheus и PromQL. Если ранее вы не работали с сервисом Prometheus, сначала изучите его документацию и справочные материалы.

## Требования {#prerequisites}

- **Включенные показатели Prometheus:** убедитесь, что показатели Prometheus включены на вашем сервере Outline. Это конфигурация по умолчанию.

- **SSH-доступ к серверу:** это необходимо для перенаправления порта Prometheus.

## Инструкции {#instructions}

1. **Перенаправление порта Prometheus**

Подключитесь к серверу с помощью SSH и перенаправьте порт 9090:

```sh
ssh root@your_server_ip -L 9090:localhost:9090
```

2. **Доступ к веб-интерфейсу Prometheus**

Откройте в браузере страницу <http://localhost:9090/graph>
Запрос показателей

3. **Используйте запросы PromQL, чтобы получить нужные вам показатели.**

### Пример запросов PromQL {#example_promql_queries}

#### Использование {#usage}

- **Байты данных (по ключу доступа, протоколу и маршруту):**

`increase(shadowsocks_data_bytes[1d])`

- **Байты данных (агрегированные по ключу доступа):**

`sum(increase(shadowsocks_data_bytes[1d])) by (access_key)`

- **Байты данных (для вычисления лимитов трафика):**

`sum(increase(shadowsocks_data_bytes{dir=~"c<p|p>t"}[30d])) by (access_key)`

- **Байты данных (по местоположению, протоколу и маршруту):**

`increase(shadowsocks_data_bytes_per_location[1d])`

#### Активные ключи доступа {#active_access_keys}

`sum(max(max_over_time(shadowsocks_data_bytes{access_key!=""} [1h])) by (access_key) > bool 0)`

#### TCP-подключения {#tcp_connections}

- **TCP-подключения (по ключу доступа, местоположению и статусу):**

`increase(shadowsocks_tcp_connections_closed[1d])`

- **TCP-подключения (по местоположению):**

`increase(shadowsocks_tcp_connections_opened[1d])`

#### UDP {#udp}

- **UDP-пакеты (по местоположению и статусу):**

`increase(shadowsocks_udp_packets_from_client_per_location[1d])`

- **UDP-связи (без разбивки):**

`increase(shadowsocks_udp_nat_entries_added[1d])`

#### Производительность {#performance}

- **Использование ЦП (по процессу):**

`rate(process_cpu_seconds_total[10m])`

- **Память (по процессу):**

`process_virtual_memory_bytes`

#### Сведения о сборке {#build_information}

- **Prometheus:**

`prometheus_build_info`

- **outline-ss-server:**

`shadowsocks_build_info`

- **Node.js:**

`nodejs_version_info`

Полный список доступных показателей можно найти в [исходном коде](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/metrics.go) `outline-ss-server`.
