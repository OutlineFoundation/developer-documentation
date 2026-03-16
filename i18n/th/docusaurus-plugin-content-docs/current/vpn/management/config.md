---
title: "Configure Access Keys"
sidebar_label: "Configure Access Keys"
---

Outline ใช้การกำหนดค่าแบบอิงตาม YAML ในการกำหนดพารามิเตอร์ VPN และการบริหารการรับส่งข้อมูล TCP/UDP การกำหนดค่าดังกล่าวรองรับความสามารถในการประกอบในหลายๆ ระดับ จึงช่วยให้การตั้งค่ามีความยืดหยุ่นและเพิ่มส่วนขยายได้

โดยการกำหนดค่าระดับสูงจะระบุ
[TunnelConfig](../reference/access-key-config#tunnelconfig)

## ตัวอย่าง {#examples}

การกำหนดค่า Shadowsocks แบบทั่วไปจะมีลักษณะดังนี้

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks
    endpoint: ss.example.com:80
    cipher: chacha20-ietf-poly1305
    secret: SECRET
    prefix: "POST "  # HTTP request

  udp:
    $type: shadowsocks
    endpoint: ss.example.com:53
    cipher: chacha20-ietf-poly1305
    secret: SECRET
    prefix: "\u0097\u00a7\u0001\u0000\u0000\u0001\u0000\u0000\u0000\u0000\u0000\u0000"  # DNS query
```

จะเห็นได้ว่าในตอนนี้เราสามารถใช้งาน TCP และ UDP ในคนละพอร์ตหรือในอุปกรณ์ปลายทางคนละเครื่อง และใช้คำนำหน้าต่างกัน

คุณสามารถใช้แท็ก Anchor ของ YAML และคีย์การผสานรวม `<<` เพื่อหลีกเลี่ยงการซ้ำ

```yaml
transport:
  $type: tcpudp

  tcp:
    <<: &shared
      $type: shadowsocks
      endpoint: ss.example.com:4321
      cipher: chacha20-ietf-poly1305
      secret: SECRET
    prefix: "POST "

  udp: *shared
```

ในตอนนี้คุณสามารถเขียนกลยุทธ์ต่างๆ และใช้การ Hop หลายรายการได้แล้ว

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: dial
      address: exit.example.com:4321
      dialer:
        $type: shadowsocks
        address: entry.example.com:4321
        cipher: chacha20-ietf-poly1305
        secret: ENTRY_SECRET

    cipher: chacha20-ietf-poly1305
    secret: EXIT_SECRET

  udp: *shared
```

ในกรณีที่มีการบล็อกโปรโตคอลที่ยากต่อการตรวจจับอย่าง Shadowsocks คุณสามารถใช้ Shadowsocks-over-Websockets ได้ ดูวิธีการติดตั้งใช้งานได้ในหัวข้อ[การกำหนดค่าตัวอย่างเซิร์ฟเวอร์](https://github.com/OutlineFoundation/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml) การกำหนดค่าไคลเอ็นต์จะมีลักษณะดังนี้

```yaml
transport:
  $type: tcpudp
  tcp:
    $type: shadowsocks
    endpoint:
        $type: websocket
        url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/tcp
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET

  udp:
    $type: shadowsocks
    endpoint:
        $type: websocket
        url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/udp
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET
```

โปรดทราบว่าอุปกรณ์ปลายทาง Websocket สามารถเข้าควบคุมอุปกรณ์ปลายทางได้ทีละเครื่อง ซึ่งสามารถใช้ประโยชน์จากส่วนนี้ในการข้ามการบล็อกตาม DNS

```yaml
transport:
  $type: tcpudp
  tcp:
    $type: shadowsocks
    endpoint:
        $type: websocket
        url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/tcp
        endpoint: cloudflare.net:443
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET

  udp:
    $type: shadowsocks
    endpoint:
        $type: websocket
        url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/udp
        endpoint: cloudflare.net:443
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET
```

โปรดใช้ตัวเลือก `first-supported` ในการกำหนดค่าเพื่อรักษาความสามารถในการใช้งานร่วมกันในไคลเอ็นต์ Outline เวอร์ชันต่างๆ การดำเนินการเช่นนี้เป็นสิ่งสำคัญอย่างยิ่งเมื่อมีการเพิ่มกลยุทธ์และฟีเจอร์ใหม่ๆ ใน Outline เนื่องจากผู้ใช้บางรายอาจยังไม่ได้อัปเดตซอฟต์แวร์ไคลเอ็นต์เป็นเวอร์ชันล่าสุด เมื่อใช้ `first-supported` คุณสามารถสร้างการกำหนดค่าในรูปแบบหนึ่งเดียวที่สามารถทำงานได้อย่างราบรื่นในแพลตฟอร์มและไคลเอ็นต์เวอร์ชันต่างๆ ได้ เพื่อรักษาความเข้ากันได้แบบย้อนหลังและประสบการณ์ของผู้ใช้ให้มีความสม่ำเสมอ

```yaml
transport:
  $type: tcpudp
  tcp:
    $type: shadowsocks
    endpoint:
      $type: first-supported
      options:
        - $type: websocket
          url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/tcp
        - ss.example.com:4321
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET

  udp:
    $type: shadowsocks
    endpoint:
      $type: first-supported
      options:
        - $type: websocket
          url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/udp
        - ss.example.com:4321
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET
```
