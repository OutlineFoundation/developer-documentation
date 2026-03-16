---
title: "動態存取金鑰"
sidebar_label: "動態存取金鑰"
---

Outline 提供兩種存取金鑰：靜態金鑰與動態金鑰。靜態金鑰將所有連線資訊編碼在金鑰本身，而動態金鑰則編碼連線資訊的位置，讓您能遠端儲存資訊並視需要修改。這表示您可以輕鬆更新伺服器設定，不需要產生新的金鑰來重新分發給使用者。本文件將說明如何使用動態存取金鑰，更靈活有效率地管理 Outline 伺服器。

您可以用三種格式指定動態存取金鑰所用的存取資訊：

### 使用 `ss://` 連結 {#use_an_ss_link}

Outline 用戶端 1.8.1 以上版本。**

您可以直接使用現有的 `ss://` 連結。如果您不需要經常變更伺服器、通訊埠或加密方法，但又希望能彈性更新伺服器位址，就適合採用這種方法。

**示例：**

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

### 使用 JSON 物件 {#use_a_json_object}

Outline 用戶端 1.8.0 以上版本。**

採用這種方法，您可以更靈活管理使用者的 Outline 連線設定，例如更新伺服器、通訊埠、密碼及加密方法。

**示例：**

```json
{
  "server": "outline-server.example.com",
  "server_port": 8388,
  "password": "example",
  "method": "chacha20-ietf-poly1305"
}
```

- **server：**VPN 伺服器的網域或 IP 位址。

- **server_port：**VPN 伺服器運作的埠號。

- **password：**連線至 VPN 所需的密碼。

- **method：**VPN 使用的加密方法。請參考 Shadowsocks 支援的 [AEAD 編碼器](https://shadowsocks.org/doc/aead.html)。

### 使用 YAML 物件 {#use_a_yaml_object}

Outline 用戶端 1.15.0 以上版本。**

這種方法和上述的 JSON 方法類似，但因使用 Outline 的進階設定格式而更具彈性。您可以更新伺服器、通訊埠、密碼、加密方法等設定。

**示例：**

```yaml
transport:
  $type: tcpudp
  tcp:
    $type: shadowsocks
    endpoint: outline-server.example.com:8388
    cipher: chacha20-ietf-poly1305
    secret: example
  udp:
    $type: shadowsocks
    endpoint: outline-server.example.com:8388
    cipher: chacha20-ietf-poly1305
    secret: example
```

- **transport：**定義要使用的傳輸通訊協定 (此例中為 TCP 和 UDP)。

- **tcp/udp：**指定每種通訊協定的設定。

    - **$type：**表示設定類型，此處為 shadowsocks。

    - **endpoint：**VPN 伺服器的網域或 IP 位址和通訊埠。

    - **secret：**連線至 VPN 所需的密碼。

    - **cipher：**VPN 使用的加密方法。請參考 Shadowsocks 支援的 [AEAD 編碼器](https://shadowsocks.org/doc/aead.html)。

關於如何設定 Outline 伺服器存取權，包括傳輸、端點、撥號程式和封包監聽器，詳見「[存取金鑰設定](config)」。

## 從靜態金鑰擷取存取資訊 {#extract_access_information_from_a_static_key}

如果您已經有靜態存取金鑰，可以擷取其中的資訊來建立 JSON 或 YAML 格式的動態存取金鑰。靜態存取金鑰的形式如下：

```none
SS-URI = "ss://" userinfo "@" hostname ":" port [ "/" ] [ "#" tag ]
userinfo = websafe-base64-encode-utf8(method  ":" password)
           method ":" password
```

示例：

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

- **Server：**`outline-server.example.com`

- **Server Port：**`8388`

- **User Info：**`Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl`；可用 [Google Admin Toolbox 編碼/解碼](https://toolbox.googleapps.com/apps/encode_decode/)之類工具進行 [base64](https://en.wikipedia.org/wiki/Base64) 解碼

    - **Method**：`chacha20-ietf-poly1305`

    - **Password**：`example`

## 選擇託管平台 {#choose_a_hosting_platform}

瞭解如何建立動態存取金鑰後，選擇合適的託管平台來存放您的存取金鑰設定至關重要。在選擇平台時，請考慮其穩定性、安全性、易用性及抗審查能力，包括：能否穩定提供存取金鑰資訊而不停機？是否有適當的安全措施保護您的設定？管理存取金鑰資訊是否方便？在實施網路審查的地區能否正常存取？

如果存取資訊可能受到限制，建議將資訊託管於能對抗審查的平台，例如 [Google 雲端硬碟](https://drive.google.com)、[pad.riseup.net](https://pad.riseup.net/)、[Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html) (使用路徑樣式存取格式)、[Netlify](https://dev.to/alexmercedcoder/delivering-json-data-with-netlify-1j96) 或 [GitHub 的私密 gist](https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists/creating-gists)。請根據您的部署需求，選擇符合存取性和安全性要求的平台。
