---
title: "Smart Dialer Configuration"
sidebar_label: "Smart Dialer Config"
---

**Smart Dialer** จะค้นหากลยุทธ์ที่เลิกบล็อก DNS และ TLS สำหรับรายการโดเมนทดสอบที่ระบุ ซึ่งจะใช้การกำหนดค่าที่อธิบายรายละเอียดกลยุทธ์ต่างๆ เพื่อให้เลือกใช้งานได้

## การกำหนดค่า YAML สำหรับ Smart Dialer

การกำหนดค่าที่ Smart Dialer ใช้จะอยู่ในรูปแบบ YAML ดังตัวอย่างต่อไปนี้

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

### การกำหนดค่า DNS

- ฟิลด์ `dns` จะระบุรายการรีโซลเวอร์ DNS ที่จะทดสอบ

- รีโซลเวอร์ DNS แต่ละรายการอาจเป็นประเภทใดประเภทหนึ่งต่อไปนี้

    - `system`: ใช้รีโซลเวอร์ระบบ ระบุด้วยออบเจ็กต์ที่ว่างเปล่า

    - `https`: ใช้รีโซลเวอร์ DNS over HTTPS (DoH) ที่เข้ารหัส

    - `tls`: ใช้รีโซลเวอร์ DNS over TLS (DoT) ที่เข้ารหัส

    - `udp`: ใช้รีโซลเวอร์ UDP

    - `tcp`: ใช้รีโซลเวอร์ TCP

#### รีโซลเวอร์ DNS-over-HTTPS (DoH)

```yaml
https:
  name: dns.google
  address: 8.8.8.8
```

- `name`: ชื่อโดเมนของเซิร์ฟเวอร์ DoH

- `address`: host:port ของเซิร์ฟเวอร์ DoH ค่าเริ่มต้นคือ `name`:443

#### รีโซลเวอร์ DNS-over-TLS (DoT)

```yaml
tls:
  name: dns.google
  address: 8.8.8.8
```

- `name`: ชื่อโดเมนของเซิร์ฟเวอร์ DoT

- `address`: host:port ของเซิร์ฟเวอร์ DoT ค่าเริ่มต้นคือ `name`:853

#### รีโซลเวอร์ UDP

```yaml
udp:
  address: 8.8.8.8
```

- `address`: host:port ของรีโซลเวอร์ UDP

#### รีโซลเวอร์ TCP

```yaml
tcp:
  address: 8.8.8.8
```

- `address`: host:port ของรีโซลเวอร์ TCP

### การกำหนดค่า TLS

- ฟิลด์ `tls` จะระบุรายการการรับส่งข้อมูล TLS ที่จะทดสอบ

- การรับส่งข้อมูล TLS แต่ละรายการคือสตริงที่ระบุการรับส่งข้อมูลที่จะใช้

- เช่น `override:host=cloudflare.net|tlsfrag:1` จะระบุการรับส่งข้อมูลที่ใช้การทำ Domain Fronting ด้วย Cloudflare และการกระจาย Fragment ของ TLS ดูรายละเอียดได้จาก
[เอกสารประกอบการกำหนดค่า](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x/configurl#hdr-Config_Format)

### การกำหนดค่าสำรอง

การกำหนดค่าสำรองจะใช้ในกรณีที่ไม่มีกลยุทธ์ปลอดพร็อกซีที่สามารถเชื่อมต่อได้ เช่น การกำหนดค่านี้ระบุพร็อกซีเซิร์ฟเวอร์สำรองเพื่อพยายามทำการเชื่อมต่อของผู้ใช้ การใช้การกำหนดค่าสำรองจะเริ่มต้นได้ช้ากว่า เนื่องจากต้องให้กลยุทธ์ DNS/TLS อื่นๆ ต้องล้มเหลว/หมดเวลาก่อน

สตริงสำรองควรเป็นดังนี้

- สตริงการกำหนดค่า `StreamDialer` ที่ถูกต้องตามที่กำหนดไว้ใน [`configurl`](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x/configurl#hdr-Proxy_Protocols)

- ออบเจ็กต์การกำหนดค่า Psiphon ที่ถูกต้องเป็นรายการย่อยของฟิลด์ `psiphon`

#### ตัวอย่างเซิร์ฟเวอร์ Shadowsocks

```yaml
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

#### ตัวอย่างเซิร์ฟเวอร์ SOCKS5

```yaml
fallback:
  - socks5://[USERINFO]@[HOST]:[PORT]
```

#### ตัวอย่างการกำหนดค่า Psiphon

หากต้องการใช้เครือข่าย [Psiphon](https://psiphon.ca/) คุณจะต้องทำดังนี้

1. ติดต่อทีม Psiphon เพื่อรับการกำหนดค่าที่ให้สิทธิ์เข้าถึงเครือข่าย ซึ่งการดำเนินการนี้อาจต้องมีการทำสัญญา

2. เพิ่มการกำหนดค่า Psiphon ที่ได้รับมาในส่วน `fallback` ของการกำหนดค่า Smart Dialer เนื่องจาก JSON สามารถใช้งานร่วมกับ YAML คุณจึงคัดลอกและวางการกำหนดค่า Psiphon ลงในส่วน `fallback` ได้โดยตรงดังนี้

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

### วิธีใช้ Smart Dialer

หากต้องการใช้ Smart Dialer ให้สร้างออบเจ็กต์ `StrategyFinder` และเรียกใช้เมธอด
`NewDialer` ซึ่งส่งผ่านในรายการโดเมนทดสอบและการกำหนดค่า YAML
เมธอด `NewDialer` จะส่งกลับ `transport.StreamDialer` ที่สามารถใช้สร้างการเชื่อมต่อโดยใช้กลยุทธ์ที่พบ เช่น

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

นี่เป็นเพียงตัวอย่างพื้นฐานและอาจต้องมีการปรับเปลี่ยนให้เข้ากับ Use Case ของคุณโดยเฉพาะ
