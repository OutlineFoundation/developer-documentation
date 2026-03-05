---
title: "Access Performance Metrics"
sidebar_label: "Performance Metrics"
---

Outline, [Prometheus](https://prometheus.io/) aracılığıyla ayrıntılı performans metrikleri sunar. Bu sayede sunucunuzun kullanımı ve sağlık durumuyla ilgili daha ayrıntılı bilgiye erişebilirsiniz. Bu kılavuzda, söz konusu metrikleri toplayıp görüntüleme işlemi anlatılmaktadır.

**Önemli not:** Bu kılavuzdan yararlanmak için temel düzeyde Prometheus ve PromQL bilginiz olmalıdır. Prometheus hakkında çok tecrübeniz yoksa Outline'daki metriklerden önce Prometheus belgeleri ve eğitimlerini incelemeniz önerilir.

## Ön hazırlık

- **Prometheus'un etkinleştirildiği Outline sunucusu**: Outline sunucunuzda Prometheus metriklerinin etkinleştirildiğinden emin olun. (Genellikle varsayılan yapılandırma bu şekildedir.)

- **Sunucunuza SSH erişimi**: Prometheus bağlantı noktasını yönlendirmek için SSH erişimi gerekir.

## Talimatlar

1. **Prometheus bağlantı noktasını yönlendirme**

SSH aracılığıyla sunucunuza bağlanın ve 9090 bağlantı noktasını yönlendirin:

2. **Prometheus web arayüzüne erişme**

Web tarayıcınızı açıp şu adrese gidin: <http://localhost:9090/graph>
Prometheus metriklerini sorgulama

3. **İlgilendiğiniz metrikleri almak için PromQL sorgularını kullanın.**

### Örnek PromQL sorguları

#### Kullanım

- **Veri baytları (erişim anahtarı, protokol ve yöne göre):**

`increase(shadowsocks_data_bytes[1d])`

- **Veri baytları (Erişim anahtarına göre toplanır):**

`sum(increase(shadowsocks_data_bytes[1d])) by (access_key)`

- **Veri baytları (veri sınırı hesaplaması için):**

`sum(increase(shadowsocks_data_bytes{dir=~"c<p|p>t"}[30d])) by (access_key)`

- **Veri baytları (konum, protokol ve yöne göre):**

`increase(shadowsocks_data_bytes_per_location[1d])`

#### Etkin erişim anahtarları

`sum(max(max_over_time(shadowsocks_data_bytes{access_key!=""} [1h])) by (access_key) > bool 0)`

#### TCP bağlantıları

- **TCP bağlantıları (erişim anahtarı, konum ve duruma göre):**

`increase(shadowsocks_tcp_connections_closed[1d])`

- **TCP bağlantıları (konuma göre):**

`increase(shadowsocks_tcp_connections_opened[1d])`

#### UDP

- **UDP paketleri (konum ve duruma göre):**

`increase(shadowsocks_udp_packets_from_client_per_location[1d])`

- **UDP ilişkilendirmeleri (Kategoriye göre ayırma yok):**

`increase(shadowsocks_udp_nat_entries_added[1d])`

#### Performans

- **CPU kullanımı (işleme göre):**

`rate(process_cpu_seconds_total[10m])`

- **Hafıza (işleme göre):**

`process_virtual_memory_bytes`

#### Derleme bilgileri

- **Prometheus:**

`prometheus_build_info`

- **outline-ss-server:**

`shadowsocks_build_info`

- **Node.js:**

`nodejs_version_info`

Mevcut tüm metriklerin listesi `outline-ss-server` [kaynak kodunda](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/metrics.go) bulunabilir.
