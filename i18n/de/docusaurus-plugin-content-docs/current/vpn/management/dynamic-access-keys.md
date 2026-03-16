---
title: "Dynamic Access Keys"
sidebar_label: "Dynamic Access Keys"
---

Outline bietet zwei Arten von Zugriffsschlüsseln: statische und dynamische. Statische Schlüssel enthalten alle Verbindungsinformationen in codierter Form im Schlüssel selbst. Dynamische Schlüssel hingegen enthalten lediglich den Speicherort der Verbindungsinformationen, sodass Sie diese Informationen unabhängig vom Schlüssel speichern und bei Bedarf ändern können. Das heißt, Sie haben die Möglichkeit, Ihre Serverkonfiguration zu aktualisieren, ohne dass Sie neue Schlüssel generieren und an Ihre Nutzer verteilen müssen. In diesem Dokument wird erläutert, wie Sie Ihren Outline-Server mit dynamischen Zugriffsschlüsseln flexibler und effizienter verwalten können.

Die Zugangsinformationen für die dynamischen Zugangsschlüssel lassen sich in drei verschiedenen Formaten angeben:

### `ss://`-Link {#use_an_ss_link}

*Outline-Client v1.8.1+*

Sie können einen vorhandenen `ss://`-Link direkt verwenden. Diese Methode ist ideal, wenn Sie den Server, den Port oder die Verschlüsselungsmethode nicht häufig ändern müssen, aber dennoch die Möglichkeit haben möchten, die Serveradresse zu aktualisieren.

**Beispiel:**

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

### JSON-Objekt {#use_a_json_object}

*Outline-Client v1.8.0+*

Diese Methode bietet flexiblere Möglichkeiten, alle Aspekte der Outline-Verbindungen Ihrer Nutzer zu verwalten. Hiermit können Sie Server, Port, Passwort und Verschlüsselungsmethode aktualisieren.

**Beispiel:**

```json
{
  "server": "outline-server.example.com",
  "server_port": 8388,
  "password": "example",
  "method": "chacha20-ietf-poly1305"
}
```

- **server:** die Domain oder IP-Adresse des VPN-Servers.

- **server_port:** die Nummer des Ports, über den der VPN-Server ausgeführt wird.

- **password:** das Passwort, das notwendig ist, um eine Verbindung mit dem VPN herzustellen.

- **method:** die vom VPN genutzte Verschlüsselungsmethode. Von Shadowsocks unterstützte [AEAD-Chiffren](https://shadowsocks.org/doc/aead.html)

### YAML-Objekt {#use_a_yaml_object}

*Outline-Client v1.15.0+*

Diese Methode ähnelt der Methode mit dem JSON-Objekt, bietet aber noch mehr Flexibilität, weil das erweiterte Konfigurationsformat von Outline genutzt wird. Hiermit können Sie Server, Port, Passwort, Verschlüsselungsmethode und mehr aktualisieren.

**Beispiel:**

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

- **transport:** Definiert die zu verwendenden Transportprotokolle (in diesem Fall TCP und UDP).

- **tcp/udp:** Die Konfiguration der einzelnen Protokolle.

    - **$type:** Die Art der Konfiguration, in diesem Fall Shadowsocks.

    - **endpoint:** Die Domain oder IP-Adresse und der Port Ihres VPN-Servers.

    - **secret:** Das Passwort, um eine Verbindung mit dem VPN herzustellen.

    - **cipher:** Die vom VPN genutzte Verschlüsselungsmethode. Von Shadowsocks unterstützte [AEAD-Chiffren finden Sie hier](https://shadowsocks.org/doc/aead.html).

Detaillierte Informationen zu allen Möglichkeiten zur Konfiguration des Zugriffs auf Ihren Online-Server, einschließlich Transport, Endpunkte, Dialer und Packet-Listener, finden Sie unter [Access Key Configuration](config).

## Zugriffsinformationen aus einem statischen Schlüssel extrahieren {#extract_access_information_from_a_static_key}

Wenn Sie einen vorhandenen statischen Zugriffsschlüssel haben, können Sie die Informationen extrahieren, um einen JSON- oder YAML-basierten dynamischen Zugriffsschlüssel zu erstellen. Statische Zugriffsschlüssel haben das folgende Muster:

```none
SS-URI = "ss://" userinfo "@" hostname ":" port [ "/" ] [ "#" tag ]
userinfo = websafe-base64-encode-utf8(method  ":" password)
           method ":" password
```

Beispiel:

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

- **Server:** `outline-server.example.com`

- **Server-Port:** `8388`

- **Nutzerinfo:** `Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl` Decodiert als [base64](https://en.wikipedia.org/wiki/Base64) mit einem Tool wie der [Google Admin Toolbox](https://toolbox.googleapps.com/apps/encode_decode/)

    - **Methode**: `chacha20-ietf-poly1305`

    - **Passwort**: `example`

## Hostingplattform auswählen {#choose_a_hosting_platform}

Jetzt wissen Sie, wie dynamische Zugriffsschlüssel erstellt werden. Als Nächstes müssen Sie eine geeignete Hostingplattform für die Konfiguration des Zugriffsschlüssels auswählen. Bei dieser Entscheidung sollten Sie Faktoren wie Zuverlässigkeit, Sicherheit, Nutzerfreundlichkeit und Zensurresistenz berücksichtigen. Sind Ihre Zugriffsschlüssel-Informationen auf der Plattform ohne Unterbrechung verfügbar? Bietet sie geeignete Sicherheitsmechanismen zum Schutz Ihrer Konfiguration? Wie einfach ist es, die Zugriffsschlüssel-Informationen auf der Plattform zu verwalten? Ist die Plattform in Regionen mit Internetzensur verfügbar?

In Fällen, in denen der Zugriff auf Informationen möglicherweise eingeschränkt ist, erwägen Sie das Hosting auf einer zensurresistenten Plattform wie [Google Drive](https://drive.google.com), [pad.riseup.net](https://pad.riseup.net/), [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html) (mit Zugriffspfad), [Netlify](https://dev.to/alexmercedcoder/delivering-json-data-with-netlify-1j96) oder [GitHub secret gists](https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists/creating-gists).
Wählen Sie eine Plattform aus, die die Anforderungen Ihrer Bereitstellung insbesondere an Zugänglichkeit und Sicherheit erfüllt.
