---
title: "與他人分享管理權限"
sidebar_label: "與他人分享管理權限"
---

Outline 服務規模擴大後，您可能需要將管理職責委派給其他信任的人員。本文介紹了與其他管理員分享管理權限的各種方法。

具體採用哪種方式，取決於您當初如何部署 Outline 伺服器。

## 雲端服務供應商部署 {#cloud_provider_deployments}

如果 Outline 伺服器部署在 DigitalOcean、AWS、Google Cloud 等雲端平台，管理權限通常是直接用供應商的整合式身分與存取權管理 (IAM) 功能控制。相較於手動分享設定，這種做法更安全可控。

### DigitalOcean {#digitalocean}

DigitalOcean 提供強大的 **Teams** 功能，讓您可以邀請其他 DigitalOcean 使用者共同管理專案。如果 Outline 伺服器託管於該平台，強烈建議用這項功能來授予管理權限。

#### 1. 授權團隊 {#1_grant_team_access}

如要與他人共同管理託管於 DigitalOcean 的 Outline 伺服器，最有效率的方式是使用 DigitalOcean 的 **Teams** 功能。

- 登入 DigitalOcean 帳戶。

- 前往「Teams」****專區。

- 如尚未建立團隊，請先建立團隊，或邀請現有的 DigitalOcean 使用者加入您的團隊。

- 邀請成員時，您可以為他們指派特定角色，並授予特定資源的存取權，例如執行 Outline 的 Droplet。

#### 2. 控管權限 {#2_control_permissions}

請謹慎評估授予團隊成員的權限。若只是要管理 Outline 伺服器，通常給予特定 Droplet 的「讀取」和「寫入」權限就足夠。這樣他們就可以：

- 查看 Droplet 的詳細資料 (IP 位址、狀態等)。

- 在需要排解問題時，進入 Droplet 的控制台。

- 根據授權情況，或許能執行重新啟動 Droplet 等操作。

使用者將 Outline Manager 連結至 DigitalOcean 帳戶後，就能查看並管理該帳戶連結的所有 Outline 伺服器。


:::tip
為提升安全性，建議新管理員在雲端服務供應商帳戶中啟用多重驗證 (MFA)。
:::

## 手動安裝 {#manual_installations}


:::caution
如果將管理權限分享給手動安裝 Outline 的使用者，之後會很難撤銷。最直接的方式是重新安裝整個伺服器，這會產生新的設定，但也會重設所有使用者的存取金鑰。
:::

若要授予管理權限的對象，是用[安裝指令碼](../getting-started/server-setup-advanced)在伺服器上手動安裝 Outline，主要的授權方式是分享**存取設定**。

Outline Manager 應用程式需要一組特定的設定字串，才能連上及管理 Outline 伺服器。這組設定字串包含所有必要資訊，包括伺服器位址、通訊埠及用於驗證的密鑰。

### 1. 找出 `access.txt` 檔案 {#1_locate_the_accesstxt_file}

請在安裝 Outline 的伺服器上進入 Outline 目錄。具體路徑可能因安裝方式略有差異，常見位置包括：

- `/opt/outline/access.txt`

- `/etc/outline/access.txt`

- Outline 伺服器容器所用的 Docker 磁碟區內。

### 2. 擷取存取設定 {#2_retrieve_the_access_config}

將找到的 `access.txt` 檔案轉換為 JSON 格式，以備下一步在 Outline Manager 中使用。

```sh
sed -n '2s/^apiUrl://p; 1s/^certSha256://p' /opt/outline/access.txt | paste -d'\n' -s | sed 'H;1h;$!d;x;s/\n/", \"apiUrl\": \"/g; s/^/{"certSha256": \"/; s/$/\"}/'
```

輸出內容會包含自行簽署的憑證指紋 (`certSha256`)，以及伺服器的管理 API 端點 (`apiUrl`)：

```json
{"certSha256": "1DCC18CC9F6C34EBBB639255F4D1BC6984C2F6A47B15F7A49AA8AFB69B7E4DDE", "apiUrl": "https://1.1.1.1:12345/Fw-CkWFNSN7Ml8LLM8Pduw"}
```


:::warning[Important]
這一行包含機密資訊，只宜分享給需要管理權限的信任對象。
:::

### 3. 安全分享存取設定 {#3_share_the_access_config_securely}

請複製輸出內容，並以安全方式分享給新的 Outline 管理員。建議避免使用未加密的管道，例如一般電子郵件或即時通訊軟體。您可以考慮使用密碼管理工具的安全分享功能，或其他具加密功能的通訊方式。

將**存取設定**貼入 Outline Manager 後，新管理員就能透過這個介面新增並管理 Outline 伺服器。如需 Outline Manager 的更多操作說明，請前往 [Outline 說明中心](https://support.google.com/outline)。
