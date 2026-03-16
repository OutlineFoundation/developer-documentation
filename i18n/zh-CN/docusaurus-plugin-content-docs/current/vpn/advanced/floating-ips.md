---
title: "Use a Domain Name with Floating IPs"
sidebar_label: "Domain with Floating IPs"
---

## 简介 {#introduction}

在网络审查严格的环境下，Outline 服务器有时可能会被发现和封锁。如果服务器设置正确，即使被封锁也有可能恢复，并且操作难度也不大。我们将使用 DNS 和浮动 IP 来恢复被封锁的服务器。DNS 是一种互联网技术，可以将域名（例如 `getoutline.org`）转换为实际 IP 地址（例如 `216.239.36.21`）；而浮动 IP 是一项云功能，支持向一个 Outline 服务器分配多个 IP 地址。

## 要求 {#requirements}

只要具备一定基础技能，就能按照本指南完成操作。对 DNS 有基本了解会起到帮助作用，但并非必要条件。这篇 [MDN](https://developer.mozilla.org/docs/Learn/Common_questions/What_is_a_domain_name) 指南介绍了域名的概念，可供参考。

为了提供具体示例，我们将使用 DigitalOcean 和 Google Domains，但只要是支持分配 IP 地址的云提供商（例如 Google Cloud 或 [AWS Lightsail](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/lightsail-create-static-ip)）以及域名注册商（例如 [AWS Route 53](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-using-route-53-to-point-a-domain-to-an-instance)）均可使用。

## 操作说明 {#instructions}

1. 下表概述了轮换服务器 IP 地址的步骤：

2. 购买域名。

3. 将该域名指向我们服务器的 IP 地址。

4. 使用该域名发放访问密钥。

5. 为服务器的 Droplet 分配浮动 IP。

6. 更改域名，使其指向新的 IP 地址。

## 在 DigitalOcean 上创建 Outline 服务器 {#create_an_outline_server_on_digitalocean}

如果您已有正在运行的 DigitalOcean 服务器，请直接跳到下一步。

1. 打开 Outline 管理器，点击左下角的“+”进入服务器创建界面。

2. 点击“DigitalOcean”按钮上的“创建服务器”，按照应用中的说明操作。

![创建服务器](/images/create-DO-server.png)

## 为服务器设置主机名 {#make_a_hostname_for_your_server}

1. 前往 [Google Domains](https://domains.google.com/m/registrar/)，点击“找到最佳选择”。

2. 在搜索栏中输入域名，然后选择一个想要的名称。在示例中，我们使用了 `outlinedemo.info`。

3. 前往 Google Domains 中的“DNS”标签页。在“自定义资源记录”下的“IPV4 地址”字段中输入服务器的 IP 地址。

4. 在 Outline 管理器中，前往服务器的“设置”标签页。在“主机名”下输入您购买的主机名，然后点击“保存”。这会使得日后所有的访问密钥使用此主机名，而不是使用服务器的 IP 地址。

![设置主机名](/images/set-hostname.png)

## 更改服务器的 IP 地址 {#change_the_servers_ip_address}

1. 在 DigitalOcean 的“Droplets”页面上找到您的服务器。

2. 在窗口的右上角，点击“Floating IP”（浮动 IP）旁边的“Enable Now”（立即启用）。

![启用浮动 IP](/images/floating-ip-DO.png)

1. 在 Droplet 列表中找到您的服务器，然后点击“Assign Floating IP”（分配浮动 IP）。

![分配浮动 IP](/images/assign-floating-ip-DO.png)

1. 返回 Google Domains 中的“DNS”标签页。

2. 像之前一样更改 IP 地址，但这一次改用新的浮动 IP 地址。此操作最多可能需要 48 小时才能生效，但通常只需要几分钟。

3. 进入 [Google 的在线 DNS 工具](https://toolbox.googleapps.com/apps/dig/#A/)，输入您的域名即可查看在最后一步中完成的更改何时生效。

![在 Google DNS 工具中搜索域名](/images/google-dns.png)

一旦此更改生效，客户端就会连接到新的 IP 地址。您可以使用新密钥连接到服务器，打开 <https://ipinfo.io>，确保页面显示了服务器的新 IP 地址。

总结
轮换 Outline 服务器的 IP 地址可以快速将服务器解除封锁，恢复对客户端的服务。如有其他疑问，欢迎随时在[通知帖子](https://redd.it/hrbhz4)下发表评论，访问 [Outline 的支持页面](https://support.getoutline.org/)，或者[直接与我们联系](https://support.getoutline.org/s/contactsupport)。
