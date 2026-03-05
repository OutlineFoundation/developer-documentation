---
title: "Dynamic Access Keys"
sidebar_label: "Dynamic Access Keys"
---

Outline 提供两种类型的访问密钥：静态访问密钥和动态访问密钥。静态密钥对密钥本身内的所有连接信息进行编码，动态密钥则对连接信息的位置进行编码，使您能够远程存储这些信息，并根据需要进行更改。这意味着您可以更新服务器配置，而无需生成新密钥并将其分发给用户。本文档介绍了如何使用动态访问密钥来更灵活、更高效地管理 Outline 服务器。

您可以通过以下三种格式指定动态访问密钥所用的访问信息：

### 使用 `ss://` 链接

Outline 客户端 1.8.1 及以上版本。**

您可以直接使用现有 `ss://` 链接。如果您不需要频繁更改服务器、端口或加密方法，但又希望能够灵活更新服务器地址，那么此方法是理想选择。

**示例：**

### 使用 JSON 对象

Outline 客户端 1.8.0 及以上版本。**

此种方法可以让您更灵活地管理用户 Outline 连接的各个方面。您可以用这种方式更新服务器、端口、密码和加密方法。

**示例：**

- **server**：VPN 服务器的域名或 IP 地址。

- **server_port**：运行 VPN 服务器的端口号。

- **password**：连接到 VPN 所需的密码。

- **method**：VPN 使用的加密方法。请参阅 Shadowsocks 支持的 [AEAD 加密](https://shadowsocks.org/doc/aead.html)。

### 使用 YAML 对象

Outline 客户端 1.15.0 及以上版本。**

此方法与前面的 JSON 方法类似，但它利用 Outline 的高级配置格式增加了更多灵活性。您可以更新服务器、端口、密码、加密方法等等。

**示例：**

- **transport**：定义要使用的传输协议（本例中为 TCP 和 UDP）。

- **tcp/udp**：指定每种协议的配置。

    - **$type**：指示配置类型（本例中为 Shadowsocks）。

    - **endpoint**：VPN 服务器的域名或 IP 地址和端口。

    - **secret**：连接到 VPN 所需的密码。

    - **cipher**：VPN 使用的加密方法。请参阅 Shadowsocks 支持的 [AEAD 加密](https://shadowsocks.org/doc/aead.html)。

如需详细了解配置 Outline 服务器访问权限的所有方式（包括传输、端点、拨号器和数据包监听器），请参阅[访问密钥配置](config)。

## 从静态密钥中提取访问信息

如果您已有静态访问密钥，则可以从中提取信息来创建基于 JSON 或 YAML 的动态访问密钥。静态访问密钥遵循以下模式：

示例：

- **服务器**：`outline-server.example.com`

- **服务器端口**：`8388`

- **用户信息**：`Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl` 使用 [Google 管理员工具箱编码/解码](https://toolbox.googleapps.com/apps/encode_decode/)等工具以 [base64](https://en.wikipedia.org/wiki/Base64) 进行解码

    - **方法**：`chacha20-ietf-poly1305`

    - **密码**：`example`

## 选择托管平台

您已了解了如何创建动态访问密钥，而为访问密钥配置选择一个合适的托管平台也非常重要。进行选择时，请综合考虑平台的可靠性、安全性、易用性和抗审查能力等因素。平台能否始终如一地提供访问密钥信息而不中断？平台能否提供适当的安全措施来保护您的配置？在平台上管理访问密钥信息的难易程度如何？平台能否在实行互联网审查制度的地区顺畅访问？

如果访问信息有可能受到限制，不妨考虑托管在具有抗审查能力的平台上，例如 [Google 云端硬盘](https://drive.google.com)、[pad.riseup.net](https://pad.riseup.net/)、[Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html)（提供路径样式访问）、[Netlify](https://dev.to/alexmercedcoder/delivering-json-data-with-netlify-1j96) 或 [GitHub 机密 Gist](https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists/creating-gists)。请评估具体部署需求，选择能够满足您的可访问性和安全性要求的平台。
