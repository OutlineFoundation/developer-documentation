---
title: "概念"
sidebar_label: "概念"
---

Outline 可協助使用者繞過限制，順利存取開放網際網路。想瞭解這項服務的運作方式，請先掌握以下重要概念：

## 服務供應商和使用者 {#service_providers_and_end_users}

Outline 系統涉及兩個主要角色：管理伺服器的**服務供應商**，以及透過伺服器上網的**使用者**。

- **服務供應商**會建立 Outline 伺服器、產生**存取金鑰**並**分發金鑰**給使用者。這些步驟可以透過 **Outline Manager** 應用程式完成。

- **使用者**安裝 **Outline 用戶端**應用程式後，只需貼上收到的**存取金鑰**，即可**連線**至安全通道。

## 存取金鑰 {#access-keys}

存取金鑰是使用者連線至 Outline 伺服器的憑證，內含 Outline 用戶端建立安全連線所需的資訊。存取金鑰有兩種：

- **靜態存取金鑰**會將連線所需的伺服器資訊 (伺服器位址、通訊埠、密碼、加密方法) 編碼，防止存取資訊遭到修改。使用者將金鑰貼至 Outline 用戶端即可連線。

示例：

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTo1UkVmeFRqbHR6Mkw@outline-server.example.com:17178/?outline=1
```

- 使用**動態存取金鑰**時，服務供應商可以遠端託管伺服器存取資訊。即使更新伺服器設定 (伺服器位址、通訊埠、密碼、加密方法)，也無需向使用者重新發放存取金鑰。如需更多資訊，請參閱「[動態存取金鑰](vpn/management/dynamic-access-keys)」一文。
