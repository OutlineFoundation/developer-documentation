---
title: "Access Performance Metrics"
sidebar_label: "Performance Metrics"
---

Outline zapewnia dostęp do szczegółowych danych dotyczących wydajności, używając pakietu narzędzi [Prometheus](https://prometheus.io/), dzięki czemu możesz dokładnie zapoznać się ze stanem i wykorzystaniem serwera. Ten przewodnik przeprowadzi Cię przez proces pobierania i wyświetlania tych danych.

**Ważna informacja:** przewodnik jest przeznaczony dla osób, które znają podstawy pakietu Prometheus oraz PromQL. Jeśli dopiero zaczynasz pracę z pakietem Prometheus, warto zapoznać się z jego dokumentacją oraz samouczkami na jego temat, zanim zagłębisz się w dane dotyczące Outline.

## Wymagania wstępne

- 

**Serwer Outline z włączonym pakietem Prometheus:** sprawdź, czy na serwerze Outline włączone są dane pakietu Prometheus (zazwyczaj są włączone domyślnie).

- 

**Dostęp SSH do serwera:** będziesz potrzebować dostępu SSH, żeby przekierować port pakietu Prometheus.

## Instrukcje

1. 

**Przekierowanie portu pakietu Prometheus**

Połącz się z serwerem przy użyciu SSH i przekieruj port 9090:

2. 

**Uzyskiwanie dostępu do interfejsu internetowego pakietu Prometheus**

Otwórz przeglądarkę i adres <http://localhost:9090/graph>. Wysyłanie zapytania dotyczącego danych z pakietu Prometheus

3. 

**Użyj zapytań PromQL, żeby uzyskać interesujące Cię dane.**

### Przykładowe zapytania PromQL

#### Wykorzystanie

- 

**Bajty danych (według klucza dostępu, protokołu i kierunku):**

`increase(shadowsocks_data_bytes[1d])`

- 

**Bajty danych (zagregowane według klucza dostępu):**

`sum(increase(shadowsocks_data_bytes[1d])) by (access_key)`

- 

**Bajty danych (na potrzeby obliczania limitów danych):**

`sum(increase(shadowsocks_data_bytes{dir=~"c<p|p>t"}[30d])) by (access_key)`

- 

**Bajty danych (według lokalizacji, protokołu i kierunku):**

`increase(shadowsocks_data_bytes_per_location[1d])`

#### Aktywne klucze dostępu

`sum(max(max_over_time(shadowsocks_data_bytes{access_key!=""} [1h])) by (access_key) > bool 0)`

#### Połączenia TCP

- 

**Połączenia TCP (według klucza dostępu, lokalizacji i stanu):**

`increase(shadowsocks_tcp_connections_closed[1d])`

- 

**Połączenia TCP (według lokalizacji):**

`increase(shadowsocks_tcp_connections_opened[1d])`

#### UDP

- 

**Pakiety UDP (według lokalizacji i stanu):**

`increase(shadowsocks_udp_packets_from_client_per_location[1d])`

- 

**Powiązania UDP (bez podziału):**

`increase(shadowsocks_udp_nat_entries_added[1d])`

#### Działanie aplikacji

- 

**Wykorzystanie procesora (według procesu):**

`rate(process_cpu_seconds_total[10m])`

- 

**Pamięć (według procesu):**

`process_virtual_memory_bytes`

#### Informacje o kompilacji

- 

**Prometheus:**

`prometheus_build_info`

- 

**outline-ss-server:**

`shadowsocks_build_info`

- 

**Node.js:**

`nodejs_version_info`

Pełną listę dostępnych danych znajdziesz w [kodzie źródłowym](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/metrics.go) `outline-ss-server`.
