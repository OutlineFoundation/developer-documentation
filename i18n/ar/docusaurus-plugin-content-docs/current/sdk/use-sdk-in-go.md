---
title: "Add Outline SDK to Your Go Code"
sidebar_label: "Go Integration"
---

سنتعرّف في هذا الدليل على عملية إعداد لغة Go البرمجية
واستخدام Outline SDK في رمز Go البرمجي.

سنعمل على إنشاء تطبيق نموذجي يُسمى `splitfetch` ويبرز
ميزة معيّنة في حزمة تطوير البرامج (SDK). ويتيح
هذا التطبيق إمكانية استرجاع صفحة ويب، و**يستخدِم Outline SDK لتقسيم اتصالات
البثّ الأوّلية عبر بروتوكول TCP إلى حزمتَين منفصلتين** بدلاً من إرسال طلب الاسترجاع في حزمة شبكة واحدة، ما قد يساعد في تفادي بعض أشكال
تداخُل الشبكات.

سيصبح بإمكانك تشغيل هذا التطبيق على أنظمة **Linux وMac وWindows**.
ولضمان تكامله مع تطبيقات أخرى على الأجهزة الجوّالة، يمكنك الاطّلاع على المقالة [إضافة Outline SDK إلى التطبيقات على الأجهزة الجوّالة](mobile-app-integration).

## الخطوة 1: إعداد لغة Go {#step_1_set_up_go}

أولاً، يجب إعداد [لغة Go البرمجية](https://go.dev/).
وفي حال تثبيتها (الإصدار 1.21 أو الأحدث)، يمكنك الانتقال
إلى الخطوة التالية.

لتثبيت اللغة، يمكنك اتّباع الخطوات المقدَّمة في [الدليل الرسمي](https://go.dev/doc/install)
أو استخدام أي أداة لإدارة الحِزم:

### Linux {#linux}

اتّبِع الخطوات الموجودة في الموقع [Go Wiki: Ubuntu](https://go.dev/wiki/Ubuntu).

### Mac {#mac}

```sh
brew install go
```

### Windows {#windows}

```powershell
winget install --id=GoLang.Go  -e
```

بعد تثبيت لغة Go، يمكنك التأكّد من تثبيتها بشكل صحيح عن طريق اختبارها
بتنفيذ الأمر التالي في وحدة طرفية:

```sh
go version
```

## الخطوة 2: إنشاء التطبيق `splitfetch` {#step_2_create_the_splitfetch_application}

لإعداد المشروع `splitfetch`، عليك أولاً إنشاء دليل المشروع
وبدء تهيئة وحدة Go على النحو التالي:

```sh
mkdir splitfetch
cd splitfetch
go mod init example/splitfetch
```

بعد ذلك، عليك إضافة اعتمادية Outline SDK وإنشاء ملف `main.go`:

```sh
go get github.com/Jigsaw-Code/outline-sdk@latest
touch main.go
```

## الخطوة 3: استخدام Outline SDK في التطبيق {#step_3_use_outline_sdk_in_the_application}

افتح ملف `main.go` في أداة تعديل الرموز المفضّلة لديك والصِق الرمز
التالي، والذي يحتوي على طريقة عمل تطبيق `splitfetch`.

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

	"github.com/Jigsaw-Code/outline-sdk/transport"
	"github.com/Jigsaw-Code/outline-sdk/transport/split"
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

بعد حفظ الرمز، يجب تشغيل الأمر التالي في الوحدة الطرفية للتأكّد
من أنّ ملف `go.mod` تم تعديله بشكل صحيح.

```sh
go mod tidy
```

## الخطوة 4: تشغيل التطبيق {#step_4_run_the_application}

بعد الانتهاء من إعداد الرمز البرمجي وحفظه، يمكنك الآن تشغيل تطبيق `splitfetch`.

ضِمن دليل `splitfetch`، عليك تشغيل الأمر التالي في
الوحدة الطرفية، مع ضبط عنوان URL كوسيطة:

```sh
go run . https://getoutline.org
```

يعمل هذا الإجراء على تجميع التطبيق وتشغيله، ما يؤدي إلى عرض محتوى HTML لصفحة الويب.

في حال أردت إنشاء برنامج مستقل ونشره، بحيث تتمكّن من تشغيله
بدون `go`، عليك استخدام أمر `go build` على النحو الآتي:

### ‫Linux وMac {#linux-mac}

```sh
go build -o splitfetch .
```

### Windows {#windows_1}

```sh
go build -o splitfetch.exe .
```

بعد الانتهاء من إنشاء الإصدار، يمكنك نشر تطبيقك وتشغيله.
على سبيل المثال:

```sh
./splitfetch https://getoutline.org
```
