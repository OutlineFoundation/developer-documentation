---
title: "和他人分享管理权限"
sidebar_label: "和他人分享管理权限"
---

随着 Outline 服务规模的扩大，您可能会发现有必要将管理职责委托给其他值得信赖的人员。本文档概述了与其他管理员分享管理权限的各种方法。

分享管理权限的方法因 Outline 服务器的初始部署方式而异。

## 云服务提供商部署 {#cloud_provider_deployments}

对于部署在 DigitalOcean、AWS 或 Google Cloud 等云平台上的 Outline 服务器，通常通过提供商的集成式身份和访问权限管理 (IAM) 功能来管控管理权限，与手动分享配置相比，这种方式更加安全可控。

### DigitalOcean {#digitalocean}

DigitalOcean 提供强大的**团队**功能，让您可以邀请其他 DigitalOcean 用户协同处理项目。对于托管在该平台上的 Outline 服务器，建议使用此功能来授予管理权限。

#### 1. 向团队授予访问权限 {#1_grant_team_access}

要分享 DigitalOcean 上托管的 Outline 服务器的管理权限，最有效的方式是使用 DigitalOcean 的**团队**功能。

- 登录您的 DigitalOcean 账号。

- 前往**团队**部分。

- 创建一个新团队（如果尚未创建），或邀请现有 DigitalOcean 用户加入您的团队。

- 邀请成员时，您可分配特定角色并授予特定资源（包括运行 Outline 的 Droplet）的访问权限。

#### 2. 控制权限 {#2_control_permissions}

谨慎考虑应授予团队成员哪种权限。如需对方管理 Outline 服务器，可授予特定 Droplet 的读写权限。这样他们便可以：

- 查看 Droplet 的详细信息，如 IP 地址、状态等。

- 在需要排查问题时，访问 Droplet 的控制台。

- 或许还能执行重启 Droplet 等操作，具体取决于授予的权限。

现在，如果用户将 Outline 管理器关联到 DigitalOcean 账号，则可查看和管理该账号下的所有 Outline 服务器。

## 手动安装 {#manual_installations}

如果用户使用[安装脚本](../getting-started/server-setup-advanced)在自己的服务器上手动安装 Outline，那么授予管理权限的主要方法是分享**访问权限配置**。

Outline 管理器应用需要使用特定的配置字符串来连接和管理 Outline 服务器。此配置字符串包含所有必要信息，包括服务器地址、端口和用于身份验证的密钥。

### 1. 查找 `access.txt` 文件 {#1_locate_the_accesstxt_file}

在安装 Outline 的服务器上，前往 Outline 目录。具体位置可能因安装方法而略有不同，不过，常见的位置包括：

- `/opt/outline/access.txt`

- `/etc/outline/access.txt`

- Outline 服务器容器使用的 Docker 卷内。

### 2. 检索访问权限配置 {#2_retrieve_the_access_config}

找到 `access.txt` 文件后，将其转换为 JSON 格式，以便接下来在 Outline 管理器中使用。

```sh
sed -n '2s/^apiUrl://p; 1s/^certSha256://p' /opt/outline/access.txt | paste -d'\n' -s | sed 'H;1h;$!d;x;s/\n/", \"apiUrl\": \"/g; s/^/{"certSha256": \"/; s/$/\"}/'
```

输出内容将包含自签名证书指纹 (`certSha256`) 以及服务器上的管理 API 端点 (`apiUrl`)：

```json
{"certSha256": "1DCC18CC9F6C34EBBB639255F4D1BC6984C2F6A47B15F7A49AA8AFB69B7E4DDE", "apiUrl": "https://1.1.1.1:12345/Fw-CkWFNSN7Ml8LLM8Pduw"}
```

### 3. 安全地分享访问权限配置 {#3_share_the_access_config_securely}

复制输出内容并以安全的方式分享给新 Outline 管理员。避免通过未加密的渠道（例如纯文本邮件或即时消息）发送。建议使用密码管理工具的安全分享功能或其他加密通信方式。

将提供的**访问权限配置**粘贴到 Outline 管理器中，新管理员便可以通过该应用的界面添加和管理 Outline 服务器。如需获取关于如何使用 Outline 管理器的更多支持信息，请访问 [Outline 帮助中心](https://support.google.com/outline)。
