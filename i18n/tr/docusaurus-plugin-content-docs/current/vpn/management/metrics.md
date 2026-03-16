---
title: "Outline sunucusunun performans metriklerine erişme"
sidebar_label: "Outline sunucusunun performans metriklerine erişme"
---

Outline, [Prometheus](https://prometheus.io/) aracılığıyla ayrıntılı performans metrikleri sunar. Bu sayede sunucunuzun kullanımı ve sağlık durumuyla ilgili daha ayrıntılı bilgiye erişebilirsiniz. Bu kılavuzda, söz konusu metrikleri toplayıp görüntüleme işlemi anlatılmaktadır.

**Önemli not:** Bu kılavuzdan yararlanmak için temel düzeyde Prometheus ve PromQL bilginiz olmalıdır. Prometheus hakkında çok tecrübeniz yoksa Outline'daki metriklerden önce Prometheus belgeleri ve eğitimlerini incelemeniz önerilir.

## Ön hazırlık {#prerequisites}

- **Prometheus'un etkinleştirildiği Outline sunucusu**: Outline sunucunuzda Prometheus metriklerinin etkinleştirildiğinden emin olun. (Genellikle varsayılan yapılandırma bu şekildedir.)

- **Sunucunuza SSH erişimi**: Prometheus bağlantı noktasını yönlendirmek için SSH erişimi gerekir.

## Talimatlar {#instructions}

1. **Prometheus bağlantı noktasını yönlendirme**

SSH aracılığıyla sunucunuza bağlanın ve 9090 bağlantı noktasını yönlendirin:

```sh
ssh root@your_server_ip -L 9090:localhost:9090
```

2. **Prometheus web arayüzüne erişme**

Web tarayıcınızı açıp şu adrese gidin: <http://localhost:9090/graph>
Prometheus metriklerini sorgulama

3. **İlgilendiğiniz metrikleri almak için PromQL sorgularını kullanın.**

### Örnek PromQL sorguları {#example_promql_queries}

#### Kullanım {#usage}

- **Veri baytları (erişim anahtarı, protokol ve yöne göre):**

`increase(shadowsocks_data_bytes[1d])`

- **Veri baytları (Erişim anahtarına göre toplanır):**

`sum(increase(shadowsocks_data_bytes[1d])) by (access_key)`

- **Veri baytları (veri sınırı hesaplaması için):**

`sum(increase(shadowsocks_data_bytes{dir=~"c<p|p>t"}[30d])) by (access_key)`

- **Veri baytları (konum, protokol ve yöne göre):**

`increase(shadowsocks_data_bytes_per_location[1d])`

#### Etkin erişim anahtarları {#active_access_keys}

`sum(max(max_over_time(shadowsocks_data_bytes{access_key!=""} [1h])) by (access_key) > bool 0)`

#### TCP bağlantıları {#tcp_connections}

- **TCP bağlantıları (erişim anahtarı, konum ve duruma göre):**

`increase(shadowsocks_tcp_connections_closed[1d])`

- **TCP bağlantıları (konuma göre):**

`increase(shadowsocks_tcp_connections_opened[1d])`

#### UDP {#udp}

- **UDP paketleri (konum ve duruma göre):**

`increase(shadowsocks_udp_packets_from_client_per_location[1d])`

- **UDP ilişkilendirmeleri (Kategoriye göre ayırma yok):**

`increase(shadowsocks_udp_nat_entries_added[1d])`

#### Performans {#performance}

- **CPU kullanımı (işleme göre):**

`rate(process_cpu_seconds_total[10m])`

- **Hafıza (işleme göre):**

`process_virtual_memory_bytes`

#### Derleme bilgileri {#build_information}

- **Prometheus:**

`prometheus_build_info`

- **outline-ss-server:**

`shadowsocks_build_info`

- **Node.js:**

`nodejs_version_info`

Mevcut tüm metriklerin listesi `outline-ss-server` [kaynak kodunda](https://github.com/OutlineFoundation/outline-ss-server/blob/master/cmd/outline-ss-server/metrics.go) bulunabilir.
