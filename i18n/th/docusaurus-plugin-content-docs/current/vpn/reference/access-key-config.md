---
title: "Access Key Configuration Reference"
sidebar_label: "Access Key Config"
---

## Tunnel

### TunnelConfig

Tunnel เป็นออบเจ็กต์ระดับบนสุดในการกำหนดค่า Outline ซึ่งจะระบุว่าควรกำหนดค่า VPN อย่างไร

**รูปแบบ:** [ExplicitTunnelConfig](#explicittunnelconfig) |
[LegacyShadowsocksConfig](#legacyshadowsocksconfig) |
[LegacyShadowsocksURI](#legacyshadowsocksuri)

### ExplicitTunnelConfig

**รูปแบบ:** *struct*

**ฟิลด์:**

- `transport` ([TransportConfig](#transportconfig)): การรับส่งที่จะใช้เพื่อแลกเปลี่ยนแพ็กเกจกับปลายทางเป้าหมาย

- `error` (*struct*): ข้อมูลสำหรับแจ้งให้ผู้ใช้ทราบในกรณีที่เกิดข้อผิดพลาดในการให้บริการ (เช่น คีย์หมดอายุ โควต้าหมด)

    - `message` (*string*): ข้อความที่ใช้ง่ายซึ่งจะแสดงต่อผู้ใช้

    - `details` (*string*): ข้อความที่จะแสดงเมื่อผู้ใช้เปิดรายละเอียดข้อผิดพลาด ซึ่งมีประโยชน์สำหรับการแก้ปัญหา

ฟิลด์ `error` และ `transport` จะเป็นข้อมูลแยกกัน

ตัวอย่างที่สําเร็จ

ตัวอย่างข้อผิดพลาด

## Transport

### TransportConfig

ระบุวิธีแลกเปลี่ยนแพ็กเก็ตกับปลายทางเป้าหมาย

**รูปแบบ:** [Interface](#interface)

ประเภท Interface ที่รองรับ

- `tcpudp`: [TCPUDPConfig](#tcpudpconfig)

### TCPUDPConfig

TCPUDPConfig ช่วยให้ตั้งค่ากลยุทธ์ TCP และ UDP แยกกันได้

**รูปแบบ:** *struct*

**ฟิลด์:**

- `tcp` ([DialerConfig](#dialerconfig)): Stream Dialer ที่จะใช้สําหรับการเชื่อมต่อ TCP

- `udp` ([PacketListenerConfig](#packetlistenerconfig)): Packet Listener ที่จะใช้กับแพ็กเก็ต UDP

ตัวอย่างการส่ง TCP และ UDP ไปยังปลายทางที่แตกต่างกัน

## Endpoint

Endpoint จะสร้างการเชื่อมต่อกับปลายทางที่คงที่ ซึ่งดีกว่าใช้ Dialer เนื่องจากช่วยให้เพิ่มประสิทธิภาพเฉพาะปลายทางได้ โดยจะมีทั้ง Stream Endpoint และ Packet Endpoint

### EndpointConfig

**รูปแบบ:** *string* | [Interface](#interface)

ปลายทาง *string* คือที่อยู่ host:port ของปลายทางที่เลือก ระบบจะสร้างการเชื่อมต่อโดยใช้ Dialer ตามค่าเริ่มต้น

ประเภท Interface ที่รองรับสําหรับ Stream Endpoint และ Packet Endpoint มีดังนี้

- `dial`: [DialEndpointConfig](#dialendpointconfig)

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `websocket`: [WebsocketEndpointConfig](#websocketendpointconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

### DialEndpointConfig

สร้างการเชื่อมต่อโดยการเชื่อมสายไปยังที่อยู่คงที่ โดยอาจใช้โปรแกรมเชื่อมสาย ซึ่งช่วยให้สามารถกำหนดกลยุทธ์ได้

**รูปแบบ:** *struct*

**ฟิลด์:**

- `address` (*string*): ที่อยู่ปลายทางที่จะเชื่อมสาย

- `dialer` ([DialerConfig](#dialerconfig)): โปรแกรมเชื่อมสายที่จะใช้เพื่อเชื่อมสายไปยังที่อยู่

### WebsocketEndpointConfig

ส่งการเชื่อมต่อสตรีมและแพ็กเก็ตไปยังปลายทางผ่าน Websocket

สำหรับการเชื่อมต่อสตรีม ระบบจะเปลี่ยนการเขียนแต่ละครั้งเป็นข้อความ Websocket และสำหรับการเชื่อมต่อแพ็กเก็ต ระบบจะเปลี่ยนแต่ละแพ็กเก็ตเป็นข้อความ Websocket

**รูปแบบ:** *struct*

**ฟิลด์:**

- `url` (*string*): URL สำหรับปลายทาง Websocket สคีมาต้องเป็น `https` หรือ `wss` สำหรับ Websocket ผ่าน TLS และ `http` หรือ `ws` สำหรับ Websocket แบบข้อความธรรมดา

- `endpoint` ([EndpointConfig](#endpointconfig)): ปลายทางของเว็บเซิร์ฟเวอร์ที่จะเชื่อมต่อ หากไม่มี ระบบจะเชื่อมต่อกับที่อยู่ซึ่งระบุไว้ใน URL

## Dialer

Dialer จะสร้างการเชื่อมต่อโดยอิงตามที่อยู่ปลายทาง โดยจะมีทั้ง Stream Dialer และ Packet Dialer

### DialerConfig

**รูปแบบ:** *null* | [Interface](#interface)

Dialer ที่เป็น *null* (ค่าว่าง) หมายถึง Dialer เริ่มต้น ซึ่งใช้การเชื่อมต่อ TCP โดยตรงสำหรับ Stream และการเชื่อมต่อ UDP โดยตรงสำหรับ Packet

ประเภทอินเทอร์เฟซที่รองรับสำหรับ Stream Dialer และ Packet Dialer

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

## Packet Listener

Packet Listener จะสร้างการเชื่อมต่อแพ็กเก็ตแบบไม่จำกัดซึ่งสามารถใช้เพื่อส่งแพ็กเก็ตไปยังปลายทางหลายแห่ง

### PacketListenerConfig

**รูปแบบ:** *null* | [Interface](#interface)

Packet Listener ที่เป็น *null* (ค่าว่าง) หมายถึง Packet Listener เริ่มต้น ซึ่งก็คือ UDP Packet Listener

ประเภท Interface ที่รองรับ

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksPacketListenerConfig](#shadowsocksconfig)

## กลยุทธ์

### Shadowsocks

#### LegacyShadowsocksConfig

LegacyShadowsocksConfig แสดงถึง Tunnel ที่ใช้ Shadowsocks เป็นช่องทางการรับส่ง โดยใช้รูปแบบเดิมเพื่อให้เข้ากันได้แบบย้อนหลัง

**รูปแบบ:** *struct*

**ฟิลด์:**

- `server` (*string*): โฮสต์ที่จะเชื่อมต่อ

- `server_port` (*number*): หมายเลขพอร์ตที่จะเชื่อมต่อ

- `method` (*string*): [การเข้ารหัส AEAD](https://shadowsocks.org/doc/aead.html#aead-ciphers) ที่จะใช้

- `password` (*string*): ใช้ในการสร้างคีย์การเข้ารหัส

- `prefix` (*string*): [การซ่อนคำนำหน้า](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/)ที่จะใช้
รองรับการเชื่อมต่อสตรีมและแพ็กเก็ต

ตัวอย่าง

#### LegacyShadowsocksURI

LegacyShadowsocksURI แสดงถึง Tunnel ที่ใช้ Shadowsocks เป็นช่องทางการรับส่ง
โดยใช้ URL รูปแบบเดิมเพื่อให้เข้ากันได้แบบย้อนหลัง

**รูปแบบ:** *string*

ดู[รูปแบบ URI ของ Shadowsocks รุ่นเดิม](https://shadowsocks.org/doc/configs.html#uri-and-qr-code)และ[รูปแบบ URI ของ SIP002](https://shadowsocks.org/doc/sip002.html) ทั้งนี้เราไม่รองรับปลั๊กอิน

ตัวอย่าง:

#### ShadowsocksConfig

ShadowsocksConfig สามารถแสดงถึง Stream Dialer หรือ Packet Dialer รวมถึง Packet Listener ที่ใช้ Shadowsocks ได้เช่นกัน

**รูปแบบ:** *struct*

**ฟิลด์:**

- `endpoint` ([EndpointConfig](#endpointconfig)): ปลายทาง Shadowsocks ที่จะเชื่อมต่อ

- `cipher` (*string*): [การเข้ารหัส AEAD](https://shadowsocks.org/doc/aead.html#aead-ciphers) ที่จะใช้

- `secret` (*string*): ใช้ในการสร้างคีย์การเข้ารหัส

- `prefix` (*string* (ไม่บังคับ)): [การซ่อนคำนำหน้า](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/)ที่จะใช้
รองรับการเชื่อมต่อสตรีมและแพ็กเก็ต

ตัวอย่าง

## คำอธิบายเมตา

### FirstSupportedConfig

ใช้การกําหนดค่าแรกที่แอปพลิเคชันรองรับ วิธีนี้ช่วยให้รวมการกําหนดค่าใหม่ได้ในขณะที่เข้ากันได้แบบย้อนหลังกับการกำหนดค่าเก่า

**รูปแบบ:** *struct*

**ฟิลด์:**

- `options` ([EndpointConfig[]](#endpointconfig) | [DialerConfig[]](#dialerconfig) | [PacketListenerConfig[]](#packetlistenerconfig)): รายการตัวเลือกที่ควรพิจารณา

ตัวอย่าง:

### Interface

Interface ช่วยให้คุณเลือกการใช้งานได้หลายวิธี โดยใช้ฟิลด์ `$type` เพื่อระบุประเภทที่ Config แสดง

ตัวอย่าง:
