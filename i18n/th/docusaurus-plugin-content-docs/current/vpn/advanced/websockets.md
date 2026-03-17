---
title: "Shadowsocks-over-WebSockets"
sidebar_label: "Shadowsocks-over-WebSockets"
---

*ไคลเอ็นต์ Outline เวอร์ชัน 1.15.0 ขึ้นไป*

บทแนะนำนี้จะอธิบายคำแนะนำแบบละเอียดทีละขั้นเพื่อช่วยคุณติดตั้งใช้งาน Shadowsocks-over-WebSockets ซึ่งเป็นเทคนิคที่มีประสิทธิภาพในการหลบเลี่ยงการเซ็นเซอร์ในสภาพแวดล้อมที่มีการบล็อกการเชื่อมต่อ Shadowsocks แบบปกติ การห่อหุ้มข้อมูลการเข้าชม Shadowsocks ภายใน WebSocket จะทำให้คุณปลอมแปลงการเข้าชมดังกล่าวเป็นการเข้าชมเว็บมาตรฐานได้ ซึ่งจะช่วยเพิ่มความยืดหยุ่นและการเข้าถึง


:::note
เฉพาะไคลเอ็นต์ Outline เวอร์ชัน 1.15.0 ขึ้นไปเท่านั้นที่รองรับ Shadowsocks-over-WebSockets โดยคุณต้องคงการกำหนดค่าที่มีอยู่ไว้เพื่อรองรับไคลเอ็นต์เวอร์ชันเก่า
:::

## ขั้นตอนที่ 1: กำหนดค่าและเรียกใช้เซิร์ฟเวอร์ Outline {#step_1_configure_and_run_an_outline_server}

สร้างไฟล์ `config.yaml` ใหม่ที่มีการกำหนดค่าต่อไปนี้

```yaml
web:
  servers:
    - id: server1
        listen: 127.0.0.1:<WEB_SERVER_PORT>

services:
  - listeners:
      - type: websocket-stream
        web_server: server1
        path: /<TCP_PATH>
      - type: websocket-packet
        web_server: server1
        path: /<UDP_PATH>
    keys:
      - id: 1
        cipher: chacha20-ietf-poly1305
        secret: <SHADOWSOCKS_SECRET>
```

:::tip
เก็บ `path` ไว้เป็นความลับเพื่อหลีกเลี่ยงการตรวจสอบ ซึ่งเส้นทางนี้จะเป็นปลายทางลับ เราจึงแนะนำให้ใช้เส้นทางที่สร้างแบบสุ่มและมีความยาว
:::


ดาวน์โหลด [`outline-ss-server`](https://github.com/OutlineFoundation/outline-ss-server/releases) เวอร์ชันล่าสุดและเรียกใช้โดยใช้การกำหนดค่าที่สร้างไว้ดังต่อไปนี้

```sh
outline-ss-server -config=config.yaml
```

## ขั้นตอนที่ 2: เปิดใช้งานเว็บเซิร์ฟเวอร์ {#step_2_expose_the_web_server}

หากต้องการให้เว็บเซิร์ฟเวอร์ WebSocket เข้าถึงได้แบบสาธารณะ คุณจะต้องเปิดใช้งานเว็บดังกล่าวบนอินเทอร์เน็ตและกำหนดค่า [TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security)
โดยมีตัวเลือกหลายวิธีในการดำเนินการดังกล่าว คุณสามารถใช้เว็บเซิร์ฟเวอร์ในเครื่อง เช่น
[Caddy](https://caddyserver.com/), [nginx](https://nginx.org/) หรือ [Apache](https://httpd.apache.org/) โดยตรวจสอบว่าเว็บเซิร์ฟเวอร์มีใบรับรอง TLS ที่ถูกต้อง หรือใช้บริการการสร้างอุโมงค์เสมือน เช่น [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) หรือ [ngrok](https://ngrok.com/)

### ตัวอย่างการใช้ TryCloudflare {#example_using_trycloudflare}


:::caution
TryCloudflare มีไว้สำหรับเดโมและการทดสอบเท่านั้น
:::

ในตัวอย่างนี้ เราจะสาธิตการใช้ [TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/) เพื่อสร้างอุโมงค์ข้อมูลอย่างรวดเร็ว ซึ่งเป็นวิธีที่สะดวกและปลอดภัยในการเปิดใช้งานเว็บเซิร์ฟเวอร์ในเครื่องโดยไม่ต้องเปิดพอร์ตขาเข้า

1. ดาวน์โหลดและติดตั้ง [`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)

2. สร้างอุโมงค์ข้อมูลที่ชี้ไปยังพอร์ตเว็บเซิร์ฟเวอร์ในเครื่อง โดยทำดังนี้

```sh
cloudflared tunnel --url http://127.0.0.1:<WEB_SERVER_PORT>
```

Cloudflare จะจัดหาโดเมนย่อย (เช่น
`acids-iceland-davidson-lb.trycloudflare.com`) เพื่อเข้าถึงปลายทาง WebSocket และจัดการ TLS โดยอัตโนมัติ โปรดจดโดเมนย่อยนี้ไว้เนื่องจากคุณจะต้องใช้ในภายหลัง

## ขั้นตอนที่ 3: สร้างคีย์การเข้าถึงแบบไดนามิก {#step_3_create_a_dynamic_access_key}

สร้างไฟล์ YAML ของคีย์การเข้าถึงไคลเอ็นต์สำหรับผู้ใช้โดยใช้รูปแบบ[การกำหนดค่าคีย์การเข้าถึง](../management/config) และระบุปลายทาง WebSocket ที่กําหนดค่าไว้ก่อนหน้านี้ในฝั่งเซิร์ฟเวอร์

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN>/<TCP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>

  udp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN>/<UDP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>
```

หลังจากสร้างไฟล์ YAML ของคีย์การเข้าถึงแบบไดนามิกแล้ว คุณต้องส่งไฟล์ดังกล่าวให้ผู้ใช้ โดยสามารถฝากไฟล์ไว้ในบริการเว็บโฮสติ้งแบบคงที่หรือจะสร้างไฟล์แบบไดนามิกก็ได้ โปรดดูข้อมูลเพิ่มเติมเกี่ยวกับวิธีใช้[คีย์การเข้าถึงแบบไดนามิก](../management/dynamic-access-keys)

## ขั้นตอนที่ 4: เชื่อมต่อกับไคลเอ็นต์ Outline {#step_4_connect_with_the_outline_client}

ใช้แอปพลิเคชัน[ไคลเอ็นต์ Outline](../../download-links) แบบทางการ (เวอร์ชัน 1.15.0 ขึ้นไป) และเพิ่มคีย์การเข้าถึงแบบไดนามิกที่สร้างขึ้นใหม่เป็นรายการเซิร์ฟเวอร์ คลิก**เชื่อมต่อ**เพื่อเริ่มการสร้างอุโมงค์เสมือนไปยังเซิร์ฟเวอร์โดยใช้การกำหนดค่า Shadowsocks ผ่าน WebSocket

ใช้เครื่องมืออย่าง [IPInfo](https://ipinfo.io) เพื่อยืนยันว่าคุณกำลังท่องอินเทอร์เน็ตผ่านเซิร์ฟเวอร์ Outline
