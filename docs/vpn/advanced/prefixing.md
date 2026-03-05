---
title: "Disguise Connections with Prefixes"
sidebar_label: "Connection Prefixes"
---

# Connection Prefix Disguises

As of Outline Client version 1.9.0, access keys support the "prefix" option. The
"prefix" is a list of bytes used as the first bytes of the
[salt](https://shadowsocks.org/guide/aead.html) of a Shadowsocks TCP connection.
This can make the connection look like a protocol that is allowed in the
network, circumventing firewalls that reject protocols they don't recognize.

## When should I try this?

If you suspect the users of your Outline deployment are still being blocked, you
may want to consider trying a few different prefixes.

## Instructions

The prefix should be no longer than 16 bytes. Longer prefixes may cause salt
collisions, which can compromise the encryption safety and cause connections to
be detected. Use the shortest prefix you can to bypass the blocking you are
facing.

The port you use should match the protocol that your prefix is pretending to be.
IANA keeps a [transport protocol port number registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)
that maps protocols and port numbers.

Some examples of effective prefixes look like common protocols:

|                      | Recommended Port                                                                                                                                             | JSON-encoded                                 | URL-encoded              |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------|--------------------------|
| HTTP request         | 80 (http)                                                                                                                                                    | `"POST "`                                      | `POST%20`                  |
| HTTP response        | 80 (http)                                                                                                                                                    | `"HTTP/1.1 "`                                  | `HTTP%2F1.1%20`            |
| DNS-over-TCP request | 53 (dns)                                                                                                                                                     | `"\u0005\u00DC\u005F\u00E0\u0001\u0020"`       | `%05%C3%9C_%C3%A0%01%20`   |
| TLS ClientHello      | 443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps-data), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (Apple APN), 5228 (Play Store), 5349 (turns) | `"\u0016\u0003\u0001\u0000\u00a8\u0001\u0001"` | `%16%03%01%00%C2%A8%01%01` |
| TLS Application Data | 443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps-data), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (Apple APN), 5228 (Play Store), 5349 (turns) | `"\u0013\u0003\u0003\u003F"`                   | `%13%03%03%3F`             |
| TLS ServerHello      | 443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps-data), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (Apple APN), 5228 (Play Store), 5349 (turns) | `"\u0016\u0003\u0003\u0040\u0000\u0002"`       | `%16%03%03%40%00%02`       |
| SSH                  | 22 (ssh), 830 (netconf-ssh), 4334 (netconf-ch-ssh), 5162 (snmpssh-trap)                                                                                      | `"SSH-2.0\r\n"`                                | `SSH-2.0%0D%0A`            |

### Dynamic Access Keys

To use the prefix feature with [Dynamic Access Keys](../management/dynamic-access-keys.md) (`ssconf://`),
add a "prefix" key to the JSON object, with a **JSON-encoded** value
representing the prefix you want (see examples in the table above). You can
use escape codes (like \u00FF) to represent non-printable Unicode codepoints in
the `U+0` to `U+FF` range. For example:

```json
{
    "server": "example.com",
    "server_port": 8388,
    "password": "example",
    "method": "chacha20-ietf-poly1305",
    "prefix": "\u0005\u00DC\u005F\u00E0\u0001\u0020"
}
```

### Static Access Keys

To use prefixes with **Static Access Keys** (ss://), you'll need to modify your
existing key before distributing it. If you have a Static Access Key generated
by Outline Manager, grab a **URL-encoded** version of your prefix (see examples
of these in the table above) and add it to the end of the access key like so:

`ss://Z34nthataITHiTNIHTohithITHbVBqQ1o3bkk@127.0.0.1:33142/?outline=1&prefix=<your url-encoded prefix goes here>`

For advanced users, you can use your browser's `encodeURIComponent()` function
to convert your **JSON-encoded** prefix to a **URL-encoded** one. To do this,
open your web inspector console
(*Developer > Javascript Web Console *on Chrome), and type the following:

```js
encodeURIComponent("<your json-encoded prefix goes here>")
```

Press enter. The value produced will be the *URL-encoded *version. For example:

```js
encodeURIComponent("\u0016\u0003\u0001\u0000\u00a8\u0001\u0001")
'%16%03%01%00%C2%A8%01%01'
```