Project: /outline/_project.yaml
Book: /outline/_book.yaml

# Dynamic Access Keys

Outline offers two types of access keys: static and dynamic. Static keys encode
all the connection information within the key itself, while dynamic keys encode
the location of the connection information, allowing you to store that
information remotely and change it if needed. This means you can update your
server configuration without having to generate and distribute new keys to your
users. This document explains how to use dynamic access keys for more flexible
and efficient management of your Outline server.

There are three formats to specify the access information that will be used by
your dynamic access keys:

### Use an `ss://` Link

_Outline Client v1.8.1+._

You can directly use an existing `ss://` link. This method is ideal if you don't
need to frequently change the server, port, or encryption method, but still want
the flexibility to update the server address.

**Example:**

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

### Use a JSON object

_Outline Client v1.8.0+._

This method offers more flexibility for managing all aspects of your users'
Outline connection. You can update the server, port, password, and encryption
method this way.

**Example:**

```json
{
  "server": "outline-server.example.com",
  "server_port": 8388,
  "password": "example",
  "method": "chacha20-ietf-poly1305"
}
```

-   **server:** The domain or IP address of your VPN server.
-   **server_port:** The port number your VPN server is running on.
-   **password:** The password required to connect to the VPN.
-   **method:** The encryption method used by the VPN. Refer to the Shadowsocks
    supported [AEAD ciphers](https://shadowsocks.org/doc/aead.html)

### Use a YAML Object

_Outline Client v1.15.0+._

This method is similar to the previous JSON method but adds even more
flexibility by leveraging Outline's advanced configuration format. You can
update the server, port, password, encryption method, and much more.

**Example:**

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

-   **transport:** Defines the transport protocols to be used (TCP and UDP in
    this case).
-   **tcp/udp:** Specifies the configuration for each protocol.
    -   **$type:** Indicates the type of configuration, here it's shadowsocks.
    -   **endpoint:** The domain or IP address and port of your VPN server.
    -   **secret:** The password required to connect to the VPN.
    -   **cipher:** The encryption method used by the VPN. Refer to the
        Shadowsocks supported [AEAD
        ciphers](https://shadowsocks.org/doc/aead.html).

See [Access Key Configuration](config) for details on all the ways you can
configure access to your Outline server, including transports, endpoints,
dialers, and packet listeners.

## Extract Access Information from a Static Key

If you have an existing static access key, you can extract the information to
create a JSON- or YAML-based dynamic access key. Static access keys follow the
following pattern:

```none
SS-URI = "ss://" userinfo "@" hostname ":" port [ "/" ] [ "#" tag ]
userinfo = websafe-base64-encode-utf8(method  ":" password)
           method ":" password
```

Example:

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

-   **Server:** `outline-server.example.com`
-   **Server Port:** `8388`
-   **User Info:** `Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl` Decoded as
    [base64](https://en.wikipedia.org/wiki/Base64) using a tool like the [Google
    Admin Toolbox
    Encode/Decode](https://toolbox.googleapps.com/apps/encode_decode/)

    -   **Method**: `chacha20-ietf-poly1305`
    -   **Password**: `example`

## Choose a Hosting Platform

Now that you understand how to create dynamic access keys, it's important to
choose a suitable hosting platform for your access key configuration. When
making this decision, consider factors like the platform's reliability,
security, ease of use, and censorship resistance. Will the platform consistently
serve your access key information without downtime? Does it offer appropriate
security measures to protect your configuration? How easy is it to manage your
access key information on the platform? Is the platform accessible in regions
with internet censorship?

For situations where access to information might be restricted, consider hosting
on censorship-resistant platforms like [Google Drive](https://drive.google.com),
[pad.riseup.net](https://pad.riseup.net/), [Amazon
S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html)
(with path-style access),
[Netlify](https://dev.to/alexmercedcoder/delivering-json-data-with-netlify-1j96),
or [GitHub secret
gists](https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists/creating-gists).
Evaluate the specific needs of your deployment and choose a platform that aligns
with your requirements for accessibility and security.