---
title: "Use a Domain Name with Floating IPs"
sidebar_label: "Domain with Floating IPs"
---

## 簡介

在網路審查嚴格的環境下，Outline 伺服器有時會被發現與封鎖，但只要伺服器設定正確，恢復運作並不困難。為了實現這一點，我們將結合使用 DNS 和浮動 IP。DNS 是一項網際網路技術，可將 `getoutline.org` 這樣的網域名稱轉換為 `216.239.36.21` 之類的實體 IP 位址；浮動 IP 則是一項雲端功能，能向 Outline 伺服器指派多個 IP 位址。

## 需求條件

依本指南操作的技術門檻較低。瞭解 DNS 的基本概念會有幫助，但並非必要。您可以參考 [MDN](https://developer.mozilla.org/docs/Learn/Common_questions/What_is_a_domain_name) 指南對網域名稱的介紹。

為了提供具體示例，我們將使用 DigitalOcean 和 Google Domains 示範。不過，其他支援指派 IP 位址的雲端服務供應商 (例如 Google Cloud 或 [AWS Lightsail](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/lightsail-create-static-ip)) 和網域註冊商 (例如 [AWS Route 53](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-using-route-53-to-point-a-domain-to-an-instance)) 也同樣適用。

## 操作說明

1. 

以下是輪換伺服器 IP 位址的大致步驟：

2. 

購買網域名稱。

3. 

將網域名稱指向我們伺服器的 IP 位址。

4. 

使用網域名稱核發存取金鑰。

5. 

將浮動 IP 指派給伺服器的 Droplet。

6. 

將網域名稱改成指向新的 IP 位址。

## 在 DigitalOcean 上建立 Outline 伺服器

如果已有運作中的 DigitalOcean 伺服器，請略過此步驟。

1. 

開啟 Outline Manager，點選左下方的「+」，進入伺服器建立畫面。

2. 

點選「DigitalOcean」按鈕上的「建立伺服器」，按照應用程式中的指示操作。

![建立伺服器](/images/create-DO-server.png)

## 設定伺服器的主機名稱

1. 

前往 [Google Domains](https://domains.google.com/m/registrar/)，點選「尋找合適的網域」。

2. 

在搜尋列輸入網域名稱，然後選取名稱。我們以 `outlinedemo.info` 為例說明。

3. 

前往 Google Domains 的「DNS」分頁。在「自訂資源記錄」底下的「IPV4 位址」的欄位中，輸入您的伺服器 IP 位址。

4. 

在 Outline Manager 中前往伺服器的「設定」分頁。在「主機名稱」欄位輸入您購買的主機名稱，點選「儲存」。如此一來，日後建立的存取金鑰就一律會使用這個主機名稱，而非伺服器的 IP 位址。

![設定主機名稱](/images/set-hostname.png)

## 變更伺服器 IP 位址

1. 

前往 DigitalOcean 的「Droplets」頁面，找出您的伺服器。

2. 

在視窗右上方，點選「Floating IP」旁的「Enable Now」。

![啟用浮動 IP](/images/floating-ip-DO.png)

1. 在「Droplets」清單中找出您的伺服器，點選「Assign Floating IP」。

![指派浮動 IP](/images/assign-floating-ip-DO.png)

1. 

返回 Google Domains 的「DNS」分頁。

2. 

像先前一樣變更 IP 位址，但這次改用新的浮動 IP 位址。這最多要 48 小時才會生效，但通常只需要幾分鐘。

3. 

開啟 [Google 的線上 DNS 工具](https://toolbox.googleapps.com/apps/dig/#A/)，輸入您的網域名稱，查看上一步的變更是否生效。

![在 Google DNS 工具中搜尋您的網域](/images/google-dns.png)

變更生效後，用戶端就會連線至新的 IP 位址。您可以使用新金鑰連上伺服器，然後開啟 <https://ipinfo.io>，確認伺服器已切換至新的 IP 位址。

結論
藉由輪換 Outline 伺服器的 IP 位址，您可以快速解封伺服器並恢復用戶端服務。如有其他問題，歡迎在[公告貼文](https://redd.it/hrbhz4)下留言、造訪 [Outline 支援頁面](https://support.getoutline.org/)或[直接聯繫我們](https://support.getoutline.org/s/contactsupport)。
