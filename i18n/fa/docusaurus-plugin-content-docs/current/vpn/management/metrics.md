---
title: "Access Performance Metrics"
sidebar_label: "Performance Metrics"
---

‫Outline سنجه‌های عملکرد مشروحی را ازطریق
[Prometheus](https://prometheus.io/) ارائه می‌کند که به شما اجازه می‌دهد اطلاعات آماری عمیق‌تری را درباره
کاربرد و سلامت سرور خود به‌دست آورید. این راهنما شما را در فرایند
بازیابی و مشاهده این سنجه‌ها همراهی می‌کند.

**نکته مهم:** این راهنما فرض می‌کند شما آشنایی پایه‌ای از
Prometheus و PromQL دارید. اگر Prometheus برایتان مقوله جدیدی است،
مستندات و آموزش‌های گام‌به‌گام آن را پیش‌از ورود به موضوع سنجه‌های Outline بخوانید.

## پیش‌نیازها

- **سرور Outline فعال‌شده با Prometheus**: مطمئن شوید که سرور Outline شما دارای
سنجه‌های Prometheus فعال‌شده باشد. (این حالت معمولاً در پیکربندی پیش‌فرض است).

- **دسترسی «پوسته امن» (SSH) به سرور شما**: برای بازارسال کردن درگاه Prometheus،
به دسترسی «پوسته امن» نیاز خواهید داشت.

## دستورالعمل‌ها

1. **بازارسال کردن درگاه Prometheus**

اتصال به سرور شما بااستفاده از «پوسته امن» و بازارسال درگاه ۹۰۹۰:

```sh
ssh root@your_server_ip -L 9090:localhost:9090
```

2. **دسترسی به میانای وب Prometheus**

مرورگر وب خود را باز کنید و به نشانی زیر پیمایش کنید: <http://localhost:9090/graph>
پُرسمان سنجه‌های Prometheus

3. **از پُرسمان‌های PromQL استفاده کنید تا سنجه‌های خاصی را که می‌خواهید بازیابی کنید.**

### نمونه پُرسمان‌های PromQL

#### کاربرد

- **بایت‌های داده (براساس کلید دسترسی، پروتکل، و مسیر):**

`increase(shadowsocks_data_bytes[1d])`

- **بایت‌های داده (تجمیع‌شده با کلید دسترسی):**

`sum(increase(shadowsocks_data_bytes[1d])) by (access_key)`

- **بایت‌های داده (برای محاسبه محدودیت‌های داده):**

`sum(increase(shadowsocks_data_bytes{dir=~"c<p|p>t"}[30d])) by (access_key)`

- **بایت‌های داده (براساس مکان، پروتکل، و مسیر):**

`increase(shadowsocks_data_bytes_per_location[1d])`

#### کلیدهای دسترسی فعال

`sum(max(max_over_time(shadowsocks_data_bytes{access_key!=""} [1h])) by (access_key) > bool 0)`

#### اتصال‌های TCP

- **اتصال‌های TCP (براساس کلید دسترسی، مکان، و وضعیت):**

`increase(shadowsocks_tcp_connections_closed[1d])`

- **اتصال‌های TCP (براساس مکان):**

`increase(shadowsocks_tcp_connections_opened[1d])`

#### UDP

- **بسته‌های UDP (براساس مکان و وضعیت):**

`increase(shadowsocks_udp_packets_from_client_per_location[1d])`

- **انجمن‌های UDP (بدون تفکیک):**

`increase(shadowsocks_udp_nat_entries_added[1d])`

#### عملکرد

- **کاربرد CPU (براساس پردازش):**

`rate(process_cpu_seconds_total[10m])`

- **حافظه (براساس پردازش):**

`process_virtual_memory_bytes`

#### ساختن اطلاعات

- **Prometheus:**

`prometheus_build_info`

- **outline-ss-server:**

`shadowsocks_build_info`

- **Node.js:**

`nodejs_version_info`

فهرست کامل سنجه‌های دردسترس را در`outline-ss-server`
[کد منبع](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/metrics.go) ببینید.
