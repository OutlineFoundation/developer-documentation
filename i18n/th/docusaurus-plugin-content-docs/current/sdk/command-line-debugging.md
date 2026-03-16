---
title: "Command Line Debugging"
sidebar_label: "Command Line Debugging"
---

คู่มือนี้แสดงวิธีใช้เครื่องมือบรรทัดคำสั่งของ Outline SDK เพื่อ
ทำความเข้าใจและหลีกเลี่ยงการรบกวนเครือข่ายจากมุมมองระยะไกล คุณจะได้เรียนรู้วิธีใช้เครื่องมือของ SDK เพื่อวัดการรบกวนเครือข่าย ทดสอบ
กลยุทธ์การหลบเลี่ยง และวิเคราะห์ผลลัพธ์ คู่มือนี้จะมุ่งเน้นที่เครื่องมือ
`resolve`, `fetch` และ `http2transport`

## เริ่มต้นใช้งานเครื่องมือ Outline SDK

คุณเริ่มใช้เครื่องมือ Outline SDK ได้โดยตรงจากบรรทัดคำสั่ง

### แก้ไข DNS

`resolve` ช่วยให้คุณค้นหา DNS ด้วยรีโซลเวอร์ที่ระบุได้

วิธีแก้ไขระเบียน A ของโดเมน

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type A 1.2.3.4.nip.io
```

วิธีแก้ไขระเบียน CNAME

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type CNAME www.google.com
```

### ดึงข้อมูลหน้าเว็บ

คุณใช้เครื่องมือ `fetch` เพื่อดึงเนื้อหาของหน้าเว็บได้

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest https://example.com
```

นอกจากนี้ยังบังคับให้การเชื่อมต่อใช้ QUIC ได้ด้วย

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -proto=h3 https://www.youtube.com
```

### ใช้พร็อกซีในเครื่อง

เครื่องมือ `http2transport` จะสร้างพร็อกซีในเครื่องเพื่อกำหนดเส้นทางการรับส่งข้อมูล
วิธีเริ่มพร็อกซีในพื้นที่ด้วยการรับส่ง Shadowsocks

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/http2transport@latest -localAddr 127.0.0.1:8080 -transport "ss://{your_shadowsocks_credentials}"
```

จากนั้นคุณจะใช้พร็อกซีนี้กับเครื่องมืออื่นๆ เช่น curl ได้

```sh
curl -p -x http://127.0.0.1:8080 https://ipinfo.io
```

## ระบุกลยุทธ์การหลบเลี่ยง

Outline SDK ช่วยให้ระบุกลยุทธ์การหลบเลี่ยงต่างๆ ได้
ซึ่งสามารถนำมารวมกันเพื่อข้ามการรบกวนเครือข่ายรูปแบบต่างๆ 
ข้อกำหนดสำหรับกลยุทธ์เหล่านี้อยู่ใน[เอกสารประกอบของ Go](https://pkg.go.dev/github.com/OutlineFoundation/outline-sdk/x@v0.0.3/configurl)

### กลยุทธ์ที่ประกอบกันได้

คุณสามารถรวมกลยุทธ์เหล่านี้เพื่อสร้างเทคนิคการหลบเลี่ยงที่แข็งแกร่งยิ่งขึ้น

* **DNS-over-HTTPS ที่มีการแยกส่วน TLS**: `doh:name=cloudflare-dns.com&address=cloudflare.net:443 | tlsfrag:1`

* **SOCKS5-over-TLS ที่มี Domain Fronting**: `tls:sni=decoy.example.com&certname=[HOST] | socks5:[HOST]:[PORT]`

* **การกำหนดเส้นทางแบบหลายช่วงด้วย Shadowsocks**: `ss://[USERINFO1]@[HOST1]:[PORT1] | ss://[USERINFO2]@[HOST2]:[PORT2] | ss://[USERINFO3]@[HOST3]:[PORT3]`

## การเข้าถึงและการวัดผลจากระยะไกล

หากต้องการวัดการรบกวนเครือข่ายตามที่พบในภูมิภาคต่างๆ คุณ
สามารถใช้พร็อกซีระยะไกลได้ คุณค้นหาหรือสร้างพร็อกซีระยะไกลเพื่อเชื่อมต่อได้

### ตัวเลือกการเข้าถึงระยะไกล

การใช้`fetch`เครื่องมือนี้จะช่วยให้คุณทดสอบการเชื่อมต่อจากระยะไกลได้หลายวิธี

#### เซิร์ฟเวอร์ Outline

เชื่อมต่อกับเซิร์ฟเวอร์ Outline มาตรฐานจากระยะไกลด้วยการรับส่งข้อมูล Shadowsocks

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "ss://{remote_shadowsocks_credentials}" https://ipinfo.io | jq
```

#### SOCKS5 ผ่าน SSH

สร้างพร็อกซี SOCKS5 โดยใช้อุโมงค์ข้อมูล SSH

```sh
ssh -D 127.0.0.1:1080 -C -N $USER@$HOST:$PORT
```

เชื่อมต่อกับอุโมงค์นั้นโดยใช้คำสั่ง fetch

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "socks5://localhost:1080" https://ipinfo.io | jq
```

## กรณีศึกษา: การหลบเลี่ยงการบล็อก YouTube ในอิหร่าน

ต่อไปนี้คือตัวอย่างการตรวจหาและหลีกเลี่ยงการรบกวนเครือข่าย

### ตรวจหาบล็อก

เมื่อพยายามดึงข้อมูลหน้าแรกของ YouTube ผ่านพร็อกซีของอิหร่าน คำขอจะหมดเวลา ซึ่งบ่งชี้ว่ามีการบล็อก

```sh
export TRANSPORT="ss://{remote_shadowsocks_credentials}"
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)" https://www.youtube.com
```

คำสั่งนี้จะล้มเหลวเนื่องจากหมดเวลา

### ข้ามด้วยการแยกส่วน TLS

การเพิ่มการแยกส่วน TLS ลงในการรับส่งจะช่วยให้เราหลีกเลี่ยงการบล็อกนี้ได้

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)|tlsfrag:1" https://www.youtube.com | grep -oe '<title>.*</title>'
```

คำสั่งนี้ดึงชื่อหน้าแรกของ YouTube ได้สำเร็จ ซึ่งก็คือ
`<title>YouTube</title>`

### การข้ามด้วยการแยกส่วน TLS และ DNS-over-HTTPS

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|tlsfrag:1|doh:name=cloudflare-dns.com&address=www.cloudflare.net" https://www.youtube.com | grep -oe '<title>.*</title>'
```

ซึ่งจะส่งคืน `<title>YouTube</title>` ได้สำเร็จด้วย

### ข้ามการบล็อกด้วยเซิร์ฟเวอร์ Outline

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|ss://<your_shadowsocks_credentials>" https://www.youtube.com | grep -oe '<title>.*</title>'
```

ซึ่งจะแสดงผลเป็น `<title>YouTube</title>` เช่นกัน

## การวิเคราะห์และแหล่งข้อมูลเพิ่มเติม

หากต้องการพูดคุยและถามคำถาม โปรดไปที่[กลุ่มสนทนาเกี่ยวกับ Outline SDK](https://github.com/OutlineFoundation/outline-sdk/discussions)
