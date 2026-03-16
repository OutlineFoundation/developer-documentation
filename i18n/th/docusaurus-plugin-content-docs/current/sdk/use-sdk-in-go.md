---
title: "เพิ่ม Outline SDK ลงในโค้ด Go"
sidebar_label: "เพิ่ม Outline SDK ลงในโค้ด Go"
---

คู่มือนี้จะอธิบายกระบวนการตั้งค่าสภาพแวดล้อม Go และการใช้ Outline SDK ในโค้ด Go

เราจะสร้างแอปพลิเคชันตัวอย่างที่ชื่อว่า `splitfetch` ซึ่งจะแสดงฟีเจอร์ของ SDK แม้ว่าแอปพลิเคชันนี้จะดึงข้อมูลหน้าเว็บ แต่แทนที่จะส่งคำขอในแพ็กเก็ตเครือข่ายเดียว **แอปพลิเคชันจะใช้ Outline SDK เพื่อแบ่งสตรีม TCP เริ่มต้นออกเป็น 2 แพ็กเก็ตแยกจากกัน** ซึ่งอาจช่วยข้ามการแทรกแซงทางเครือข่ายบางรูปแบบได้

คุณจะเรียกใช้แอปพลิเคชันใน **Linux, Mac, และ Windows** ได้
ดูข้อมูลเกี่ยวกับการผสานรวมกับแอปบนมือถือได้ที่หัวข้อ[เพิ่ม Outline SDK ลงในแอปบนมือถือ](mobile-app-integration)

## ขั้นตอนที่ 1: ตั้งค่า Go {#step_1_set_up_go}

อันดับแรก คุณจะต้องใช้ [Go Programming Language](https://go.dev/)
หากคุณได้ติดตั้ง Go (เวอร์ชัน 1.21 หรือใหม่กว่า) ไว้แล้ว คุณก็ข้ามไปยังขั้นตอนถัดไปได้เลย

คุณสามารถติดตั้งได้โดยทำตาม[คู่มืออย่างเป็นทางการ](https://go.dev/doc/install) หรือหากคุณใช้เครื่องมือจัดการแพ็กเกจ ให้ทำดังนี้

### Linux {#linux}

ทำตามขั้นตอนใน [Go Wiki: Ubuntu](https://go.dev/wiki/Ubuntu)

### Mac {#mac}

```sh
brew install go
```

### Windows {#windows}

```powershell
winget install --id=GoLang.Go  -e
```

หลังจากติดตั้ง Go แล้ว คุณสามารถยืนยันว่าการติดตั้งถูกต้องแล้วได้โดยเรียกใช้คำสั่งต่อไปนี้ในเทอร์มินัล

```sh
go version
```

## ขั้นตอนที่ 2: สร้างแอปพลิเคชัน `splitfetch` {#step_2_create_the_splitfetch_application}

ทำการตั้งค่าโปรเจ็กต์ `splitfetch` ให้เสร็จสิ้น ก่อนอื่นให้สร้างไดเรกทอรีโปรเจ็กต์และเริ่มต้นโมดูล Go

```sh
mkdir splitfetch
cd splitfetch
go mod init example/splitfetch
```

ถัดไป ให้เพิ่ม Outline SDK ลงไปและสร้างไฟล์ `main.go`

```sh
go get github.com/OutlineFoundation/outline-sdk@latest
touch main.go
```

## ขั้นตอนที่ 3: ใช้ Outline SDK ในแอปพลิเคชัน {#step_3_use_outline_sdk_in_the_application}

เปิดไฟล์ `main.go` ในตัวแก้ไขโค้ดที่คุณชื่นชอบแล้ววางโค้ดต่อไปนี้ลงไป ซึ่งโค้ดนี้มีตรรกะทั้งหมดสำหรับแอปพลิเคชัน `splitfetch`

```go
package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"net"
	"net/http"
	"os"

	"github.com/OutlineFoundation/outline-sdk/transport"
	"github.com/OutlineFoundation/outline-sdk/transport/split"
)

// The number of bytes to send in the first packet.
const splitPacketSize = 3

func main() {
	// 1. Get the URL from the command-line arguments.
	if len(os.Args) < 2 {
		log.Fatalf("Usage: %s <URL>", os.Args[0])
	}
	url := os.Args[1]

	// 2. Create a split dialer from the Outline SDK.
	// This dialer wraps a standard TCP dialer to add the splitting behavior.
	dialer, err := split.NewStreamDialer(&transport.TCPDialer{}, split.NewFixedSplitIterator(splitPacketSize))
	if err != nil {
		log.Fatalf("Failed to create split dialer: %v", err)
	}

	// 3. Configure an HTTP client to use our custom split dialer for TCP connections.
	httpClient := &http.Client{
		Transport: &http.Transport{
			DialContext: func(ctx context.Context, network, addr string) (net.Conn, error) {
				return dialer.DialStream(ctx, addr)
			},
		},
	}

	// 4. Use the custom client to make the HTTP GET request.
	resp, err := httpClient.Get(url)
	if err != nil {
		log.Fatalf("HTTP request failed: %v", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("Failed to read response body: %v", err)
	}
	fmt.Println(string(body))
}
```

หลังจากบันทึกโค้ดแล้ว ให้เรียกใช้คำสั่งต่อไปนี้ในเทอร์มินัลเพื่อตรวจสอบว่าไฟล์ `go.mod` ได้รับการอัปเดตอย่างถูกต้อง

```sh
go mod tidy
```

## ขั้นตอนที่ 4: เรียกใช้แอปพลิเคชัน {#step_4_run_the_application}

เมื่อมีโค้ดแล้ว คุณก็จะเรียกใช้แอปพลิเคชัน `splitfetch` ได้

จากภายในไดเรกทอรี `splitfetch` ให้เรียกใช้คำสั่งต่อไปนี้ในเทอร์มินัล ซึ่งส่งผ่าน URL เป็นอาร์กิวเมนต์

```sh
go run . https://getoutline.org
```

การดำเนินการนี้จะคอมไพล์และเรียกใช้แอปพลิเคชัน ซึ่งจะแสดงเนื้อหา HTML ของหน้าเว็บ

หากต้องการสร้างและแจกจ่ายโปรแกรมแบบสแตนด์อโลนที่คุณเรียกใช้ได้โดยไม่ต้องมี `go` ให้ใช้คำสั่ง `go build`

### Linux และ Mac {#linux-mac}

```sh
go build -o splitfetch .
```

### Windows {#windows_1}

```sh
go build -o splitfetch.exe .
```

เมื่อเสร็จสิ้นการสร้างแล้ว คุณจะแจกจ่ายและเรียกใช้แอปพลิเคชันได้
เช่น

```sh
./splitfetch https://getoutline.org
```
