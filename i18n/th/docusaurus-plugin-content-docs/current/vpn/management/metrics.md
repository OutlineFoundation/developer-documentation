---
title: "Access Performance Metrics"
sidebar_label: "Performance Metrics"
---

Outline ให้ข้อมูลเมตริกประสิทธิภาพโดยละเอียดผ่าน [Prometheus](https://prometheus.io/) ซึ่งช่วยให้คุณทำความเข้าใจการใช้งานและประสิทธิภาพของเซิร์ฟเวอร์ได้อย่างลึกซึ่งยิ่งขึ้น โดยคู่มือนี้จะแนะนำขั้นตอนการดึงข้อมูลและการดูเมตริกดังกล่าว

**หมายเหตุสำคัญ:** คุณควรมีความรู้พื้นฐานเกี่ยวกับ Prometheus และ PromQL มาก่อนใช้คู่มือนี้ ในกรณีที่คุณยังไม่คุ้นเคยกับ Prometheus โปรดดูเอกสารประกอบและบทแนะนำต่างๆ ก่อนจะมาเจาะลึกเรื่องเมตริกของ Outline

## สิ่งที่ต้องดำเนินการก่อน

- **เปิดใช้ Prometheus ในเซิร์ฟเวอร์ Outline**: ตรวจสอบว่าเซิร์ฟเวอร์ Outline ของคุณได้เปิดใช้เมตริกของ Prometheus แล้ว (ส่วนใหญ่จะเป็นการกำหนดค่าเริ่มต้นไว้แล้ว)

- **การเข้าถึง SSH ในเซิร์ฟเวอร์ของคุณ**: คุณต้องมีสิทธิ์เข้าถึง SSH เพื่อส่งต่อพอร์ต Prometheus

## วิธีการ

1. **ส่งต่อพอร์ต Prometheus**

เชื่อมต่อกับเซิร์ฟเวอร์ของคุณโดยใช้ SSH และส่งต่อพอร์ต 9090

```sh
ssh root@your_server_ip -L 9090:localhost:9090
```

2. **เข้าถึงอินเทอร์เฟซเว็บ Prometheus**

เปิดเว็บเบราว์เซอร์และไปที่ <http://localhost:9090/graph>
เมตริกการค้นหาของ Prometheus

3. **ใช้การค้นหา PromQL เพื่อดึงข้อมูลเมตริกที่คุณสนใจ**

### ตัวอย่างการค้นหา PromQL

#### การใช้งาน

- **ไบต์ (จำแนกตามคีย์การเข้าถึง โปรโตคอล และทิศทาง)**

`increase(shadowsocks_data_bytes[1d])`

- **ไบต์ (รวมโดยคีย์การเข้าถึง)**

`sum(increase(shadowsocks_data_bytes[1d])) by (access_key)`

- **ไบต์ (สำหรับการคำนวณขีดจำกัดของข้อมูล)**

`sum(increase(shadowsocks_data_bytes{dir=~"c<p|p>t"}[30d])) by (access_key)`

- **ไบต์ (จำแนกตามตำแหน่ง โปรโตคอล และทิศทาง)**

`increase(shadowsocks_data_bytes_per_location[1d])`

#### คีย์การเข้าถึงที่ใช้งานอยู่

`sum(max(max_over_time(shadowsocks_data_bytes{access_key!=""} [1h])) by (access_key) > bool 0)`

#### การเชื่อมต่อ TCP

- **การเชื่อมต่อ TCP (จำแนกตามคีย์การเข้าถึง ตำแหน่ง และสถานะ)**

`increase(shadowsocks_tcp_connections_closed[1d])`

- **การเชื่อมต่อ TCP (จำแนกตามตำแหน่ง)**

`increase(shadowsocks_tcp_connections_opened[1d])`

#### UDP

- **แพ็กเก็ต UDP (จำแนกตามตำแหน่งและสถานะ)**

`increase(shadowsocks_udp_packets_from_client_per_location[1d])`

- **การเชื่อมโยง UDP (ไม่มีรายละเอียด)**

`increase(shadowsocks_udp_nat_entries_added[1d])`

#### ประสิทธิภาพ

- **การใช้ CPU (จำแนกตามกระบวนการ)**

`rate(process_cpu_seconds_total[10m])`

- **หน่วยความจำ (จำแนกตามกระบวนการ)**

`process_virtual_memory_bytes`

#### ข้อมูลบิลด์

- **Prometheus**

`prometheus_build_info`

- **outline-ss-server**

`shadowsocks_build_info`

- **Node.js**

`nodejs_version_info`

โปรดดูรายการเมตริกที่มีทั้งหมดใน[ซอร์สโค้ด](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/metrics.go) `outline-ss-server`
