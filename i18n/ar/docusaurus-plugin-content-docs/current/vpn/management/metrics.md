---
title: "Access Performance Metrics"
sidebar_label: "Performance Metrics"
---

يوفّر Outline مقاييس أداء مفصّلة من خلال
[Prometheus](https://prometheus.io/)، ما يتيح لك الحصول على إحصاءات متعمّقة
حول استخدام الخادم وصحته. وستتعرّف في هذا الدليل على خطوات
الحصول على هذه المقاييس والاطّلاع عليها.

**ملاحظة مُهمّة:** من المفترض أن يكون لديك فهم مبدئي لـ
Prometheus وPromQL من أجل استيعاب معلومات هذا الدليل. وإذا لم تكن على دراية بـ Prometheus، ننصحك بالاطّلاع على
المستندات والأدلّة التوجيهية قبل التعمّق في فهم مقاييس Outline.

## المتطلّبات الأساسية {#prerequisites}

- **تفعيل مقاييس Prometheus على خادم Outline**: تأكَّد من تفعيل مقاييس Prometheus على خادم Outline
الخاص بك. (يكون هذا هو الإعداد التلقائي عادةً).

- **إذن وصول بروتوكول النقل الآمن (SSH) إلى الخادم**: ستحتاج إلى إذن وصول بروتوكول SSH لإعادة توجيه
منفذ Prometheus.

## التعليمات {#instructions}

1. **إعادة توجيه منفذ Prometheus**

اتّصِل بالخادم باستخدام بروتوكول SSH ثم أعِد توجيه المنفذ 9090:

```sh
ssh root@your_server_ip -L 9090:localhost:9090
```

2. **الوصول إلى واجهة ويب Prometheus**

افتح متصفح الويب ثمّ انتقِل إلى الرابط <http://localhost:9090/graph>
للاطّلاع على "مقاييس طلب Prometheus" ‏(Query Prometheus Metrics)

3. **استخدام طلبات PromQL لإيجاد المقاييس المطلوبة**

### مثال على طلبات PromQL {#example_promql_queries}

#### الاستخدام {#usage}

- **وحدات البايت للبيانات (حسب مفتاح الوصول والبروتوكول والاتجاه):**

`increase(shadowsocks_data_bytes[1d])`

- **وحدات البايت للبيانات (مُجمعة حسب مفتاح الوصول):**

`sum(increase(shadowsocks_data_bytes[1d])) by (access_key)`

- **وحدات البايت للبيانات (لحساب الحد الأقصى للبيانات):**

`sum(increase(shadowsocks_data_bytes{dir=~"c<p|p>t"}[30d])) by (access_key)`

- **وحدات البايت للبيانات (حسب الموقع والبروتوكول والاتجاه):**

`increase(shadowsocks_data_bytes_per_location[1d])`

#### مفاتيح الوصول النشطة {#active_access_keys}

`sum(max(max_over_time(shadowsocks_data_bytes{access_key!=""} [1h])) by (access_key) > bool 0)`

#### اتصالات TCP {#tcp_connections}

- **اتصالات TCP (حسب مفتاح الوصول والموقع والحالة):**

`increase(shadowsocks_tcp_connections_closed[1d])`

- **اتصالات TCP (حسب الموقع):**

`increase(shadowsocks_tcp_connections_opened[1d])`

#### UDP {#udp}

- **حزم UDP (حسب الموقع والحالة):**

`increase(shadowsocks_udp_packets_from_client_per_location[1d])`

- **روابط UDP (بدون تقسيم):**

`increase(shadowsocks_udp_nat_entries_added[1d])`

#### الأداء {#performance}

- **استخدام وحدة المعالجة المركزية (CPU) (حسب العملية):**

`rate(process_cpu_seconds_total[10m])`

- **الذاكرة (حسب العملية):**

`process_virtual_memory_bytes`

#### معلومات الإصدار {#build_information}

- **Prometheus:**

`prometheus_build_info`

- **outline-ss-server:**

`shadowsocks_build_info`

- **Node.js:**

`nodejs_version_info`

تتوفّر قائمة كاملة بالمقاييس المتاحة في [رمز مصدر](https://github.com/OutlineFoundation/outline-ss-server/blob/master/cmd/outline-ss-server/metrics.go)
`outline-ss-server`.
