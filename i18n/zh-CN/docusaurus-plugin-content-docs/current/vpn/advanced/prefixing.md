---
title: "连接前缀伪装"
sidebar_label: "连接前缀伪装"
---

从 Outline 客户端 1.9.0 版开始，访问密钥支持“prefix”选项。“prefix”是一个字节列表，用作 Shadowsocks TCP 连接的[盐](https://shadowsocks.org/doc/aead.html)的第一个字节。
这可以让连接看起来像是网络允许的协议，从而绕过会拒绝陌生协议的防火墙。

## 何时尝试此选项？ {#when_should_i_try_this}

如果您怀疑自己的 Outline 部署的用户仍然处于被封锁状态，不妨考虑尝试一些不同的 prefix。

## 操作说明 {#instructions}

prefix 不应超过 16 个字节。prefix 太长可能会导致盐冲突，进而影响到加密安全性，造成连接被检测到。请使用尽可能短的 prefix，这有助于绕过您当前面临的封锁。

您使用的端口应与 prefix 所伪装的协议相匹配。IANA 维护着一个[传输协议端口号注册表](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)，该表将协议和端口号对应起来。

下面是一些可伪装成常见协议的有效 prefix 示例：

建议的端口
JSON 编码格式
网址编码格式

HTTP 请求
80 (http)
`"POST "`
`POST%20`

HTTP 响应
80 (http)
`"HTTP/1.1 "`
`HTTP%2F1.1%20`

DNS-over-TCP 请求
53 (dns)
`"\u0005\u00DC\u005F\u00E0\u0001\u0020"`
`%05%C3%9C_%C3%A0%01%20`

TLS ClientHello
443 (https)、463 (smtps)、563 (nntps)、636 (ldaps)、989 (ftps-data)、990 (ftps)、993 (imaps)、995 (pop3s)、5223 (Apple APN)、5228 (Play 商店)、5349 (turns)
`"\u0016\u0003\u0001\u0000\u00a8\u0001\u0001"`
`%16%03%01%00%C2%A8%01%01`

TLS 应用数据
443 (https)、463 (smtps)、563 (nntps)、636 (ldaps)、989 (ftps-data)、990 (ftps)、993 (imaps)、995 (pop3s)、5223 (Apple APN)、5228 (Play 商店)、5349 (turns)
`"\u0013\u0003\u0003\u003F"`
`%13%03%03%3F`

TLS ServerHello
443 (https)、463 (smtps)、563 (nntps)、636 (ldaps)、989 (ftps-data)、990 (ftps)、993 (imaps)、995 (pop3s)、5223 (Apple APN)、5228 (Play 商店)、5349 (turns)
`"\u0016\u0003\u0003\u0040\u0000\u0002"`
`%16%03%03%40%00%02`

SSH
22 (ssh)、830 (netconf-ssh)、4334 (netconf-ch-ssh)、5162 (snmpssh-trap)
`"SSH-2.0\r\n"`
`SSH-2.0%0D%0A`

### 动态访问密钥 {#dynamic_access_keys}

如需将 prefix 功能与[动态访问密钥](../management/dynamic-access-keys) (`ssconf://`) 搭配使用，请为 JSON 对象添加一个“prefix”键，并采用 **JSON 编码**值来表示所需的 prefix（请参见上方表格中的示例）。您可以使用转义代码（例如 \u00FF）来表示 `U+0` 至 `U+FF` 范围内不可打印的 Unicode 代码点。例如：

```json
{
    "server": "example.com",
    "server_port": 8388,
    "password": "example",
    "method": "chacha20-ietf-poly1305",
    "prefix": "\u0005\u00DC\u005F\u00E0\u0001\u0020"
}
```

### 静态访问密钥 {#static_access_keys}

如需将 prefix 与**静态访问密钥** (ss://) 搭配使用，您需要修改现有的密钥，然后再进行分发。如果您拥有 Outline 管理器生成的静态访问密钥，请提取**网址编码**格式的 prefix（请参见上方表格中的示例），然后将其添加到访问密钥的末尾，例如：

`ss://Z34nthataITHiTNIHTohithITHbVBqQ1o3bkk@127.0.0.1:33142/?outline=1&prefix=<your url-encoded prefix goes here>`

对于高级用户，您可以使用浏览器的 `encodeURIComponent()` 函数，将 **JSON 编码格式**的 prefix 转换为**网址编码格式**的 prefix。为此，请打开 Web Inspector 控制台（在 Chrome 中依次找到*“开发者”>“JavaScript Web 控制台”*），然后输入以下内容：

```js
encodeURIComponent("<your json-encoded prefix goes here>")
```

按 Enter 键。所生成的值将采用*网址编码*格式。例如：

```js
encodeURIComponent("\u0016\u0003\u0001\u0000\u00a8\u0001\u0001")
'%16%03%01%00%C2%A8%01%01'
```
