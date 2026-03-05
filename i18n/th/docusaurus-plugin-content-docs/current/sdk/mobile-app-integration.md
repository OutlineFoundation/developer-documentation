---
title: "Add Outline SDK to Your Mobile App"
sidebar_label: "Mobile App Integration"
---

เอกสารฉบับนี้สรุปวิธีผสานรวม Outline SDK เข้ากับแอปพลิเคชันบนมือถือ โดยจะมุ่งเน้นที่ไลบรารี `MobileProxy` สำหรับการจัดการพร็อกซีในระบบแบบง่าย

`MobileProxy` คือไลบรารีที่พัฒนาด้วยภาษา Go ซึ่งออกแบบมาเพื่อเพิ่มความคล่องตัวให้กับการผสานรวมฟังก์ชันการทำงานของพร็อกซีเข้ากับแอปบนมือถือ โดยจะใช้ [Go
Mobile](https://go.dev/wiki/Mobile) ในการสร้างไลบรารีมือถือ ซึ่งช่วยให้คุณสามารถกำหนดค่าไลบรารีระบบเครือข่ายของแอปให้กำหนดเส้นทางการรับส่งข้อมูลผ่านพร็อกซีในระบบ

**แอปที่ไม่มี MobileProxy**

![แอปเนื้อหาที่ไม่มี MobileProxy](/images/mobileproxy-before.png)

**แอปที่มี MobileProxy**

![แอปเนื้อหาที่มี MobileProxy](/images/mobileproxy-after.png)

## ขั้นตอนที่ 1: การสร้างไลบรารี MobileProxy สำหรับมือถือ

ใช้ [gomobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile) เพื่อคอมไพล์โค้ด Go ลงในไลบรารีสำหรับ Android และ iOS

1. 

โคลนที่เก็บ Outline SDK

2. 

สร้างไบนารี Go Mobile ด้วย [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies)

#### เพิ่มการรองรับ Psiphon

คุณเพิ่มการรองรับเพื่อใช้เครือข่าย [Psiphon](https://psiphon.ca/) ได้โดยทำตามขั้นตอนเพิ่มเติมต่อไปนี้

    - ติดต่อทีม Psiphon เพื่อรับการกำหนดค่าที่ให้สิทธิ์เข้าถึงเครือข่าย ซึ่งการดำเนินการนี้อาจต้องมีการทำสัญญา

    - เพิ่มการกำหนดค่า Psiphon ที่ได้รับมาในส่วน `fallback` ของการกำหนดค่า `SmartDialer`

    - 

สร้าง Mobile Proxy โดยใช้แฟล็ก `-tags psiphon`

จำเป็นต้องใช้แฟล็ก `-tags psiphon` เนื่องจากฐานของโค้ด Psiphon ได้รับใบอนุญาตภายใต้ GPL ซึ่งสามารถบังคับใช้ข้อจำกัดของใบอนุญาตกับโค้ดของคุณเองได้ คุณจึงอาจต้องพิจารณาขอรับใบอนุญาตพิเศษจากทีมดังกล่าว

3. 

สร้างไลบรารีมือถือและเพิ่มไปยังโปรเจ็กต์ของคุณ โดยทำดังนี้

### Android

ใน Android Studio ให้เลือก **ไฟล์ > นำเข้าโปรเจ็กต์…** เพื่อนำเข้าแพ็กเกจ `out/mobileproxy.aar` ที่สร้าง โปรดดูความช่วยเหลือเพิ่มเติมที่บทความ[การสร้างและการติดตั้งใช้งานกับ Android](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1) ของ Go Mobile

### iOS

ลากแพ็กเกจ `out/mobileproxy.xcframework` ไปยังโปรเจ็กต์ Xcode โปรดดูความช่วยเหลือเพิ่มเติมที่บทความ[การสร้างและการติดตั้งใช้งานกับ iOS](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1) ของ Go Mobile

## ขั้นตอนที่ 2: เรียกใช้ MobileProxy

เริ่มต้นพร็อกซีในระบบ `MobileProxy` ภายในรันไทม์ของแอป
คุณใช้การกำหนดค่าการรับส่งข้อมูลแบบคงที่หรือ Smart Proxy สำหรับการเลือกกลยุทธ์แบบไดนามิกได้

- 

**การกำหนดค่าการรับส่งข้อมูลแบบคงที่**: ใช้ฟังก์ชัน `RunProxy` กับที่อยู่ในระบบและการกำหนดค่าการรับส่งข้อมูล

### Android

### iOS

- 

**Smart Proxy**: Smart Proxy จะเลือกกลยุทธ์ DNS และ TLS ตามโดเมนทดสอบที่ระบุแบบไดนามิก คุณต้องระบุกลยุทธ์การกำหนดค่าในรูปแบบ YAML ([ตัวอย่าง](https://github.com/Jigsaw-Code/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml))

### Android

### iOS

## ขั้นตอนที่ 3: กำหนดค่าไคลเอ็นต์ HTTP และไลบรารีระบบเครือข่าย

กำหนดค่าไลบรารีระบบเครือข่ายเพื่อใช้ที่อยู่พร็อกซีและพอร์ตในระบบ

### Dart/Flutter HttpClient

ตั้งค่าพร็อกซีด้วย
[`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html)

### OkHttp (Android)

ตั้งค่าพร็อกซีด้วย
[`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/)

### JVM (Java, Kotlin)

กำหนดค่าพร็อกซีเพื่อใช้กับ[พร็อพเพอร์ตี้ระบบ](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html)

### Android Web View

ใช้การกำหนดค่าพร็อกซีกับมุมมองเว็บทั้งหมดในแอปพลิเคชันด้วยไลบรารี [`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController)

### iOS Web View

ตั้งแต่ iOS 17 เป็นต้นไป คุณสามารถเพิ่มการกำหนดค่าพร็อกซีลงใน `WKWebView` โดยใช้[พร็อพเพอร์ตี้ `WKWebsiteDataStore`](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration)

## ขั้นสูง: สร้างไลบรารีมือถือที่กำหนดเอง

สำหรับ Use Case ขั้นสูง คุณสร้างไลบรารีมือถือของคุณเองได้

1. **สร้างไลบรารี Go**: พัฒนาแพ็กเกจ Go ที่รวมฟังก์ชันการทำงาน SDK ที่จำเป็นเข้าด้วยกัน

2. **สร้างไลบรารีมือถือ**: ใช้ `gomobile bind` เพื่อสร้าง Android ARchive (AAR) และ Apple Framework โดยตัวอย่างมีดังนี้

    - [Outline Android Archive](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [Outline Apple Framework](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **ผสานรวมลงในแอป**: เพิ่มไลบรารีที่สร้างขึ้นลงในแอปพลิเคชันบนมือถือ
