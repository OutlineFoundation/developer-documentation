---
title: "Shadowsocks-over-WebSockets"
sidebar_label: "Shadowsocks-over-WebSockets"
---

*Outline-Client v1.15.0+*

Dieses Tutorial bietet eine Schritt-für-Schritt-Anleitung zur Implementierung von Shadowsocks-over-WebSockets, ein effektives Verfahren zur Umgehung von Zensuren in Umgebungen, in denen reguläre Shadowsocks-Verbindungen blockiert werden. Durch die Kapselung des Shadowsocks-Traffics in WebSockets können Sie ihn als Standard-Web-Traffic tarnen – für höhere Ausfallsicherheit und Zugänglichkeit.


:::note
Shadowsocks-over-WebSockets wird nur auf Outline-Clients mit der Version v1.15.0+ unterstützt. Zur Unterstützung älterer Client-Versionen müssen Sie Ihre vorhandenen Konfigurationen beibehalten.
:::

## Schritt 1: Outline-Server konfigurieren und ausführen {#step_1_configure_and_run_an_outline_server}

Erstellen Sie eine neue `config.yaml`-Datei mit der folgenden Konfiguration:

```yaml
web:
  servers:
    - id: server1
        listen: 127.0.0.1:<WEB_SERVER_PORT>

services:
  - listeners:
      - type: websocket-stream
        web_server: server1
        path: /<TCP_PATH>
      - type: websocket-packet
        web_server: server1
        path: /<UDP_PATH>
    keys:
      - id: 1
        cipher: chacha20-ietf-poly1305
        secret: <SHADOWSOCKS_SECRET>
```

:::tip
Behalten Sie das `path`-Secret bei, um Prüfungen zu vermeiden. Es fungiert als geheimer Endpunkt. Wir empfehlen einen langen, nach dem Zufallsprinzip generierten Pfad.
:::


Laden Sie den neuesten [`outline-ss-server`](https://github.com/OutlineFoundation/outline-ss-server/releases) herunter und führen Sie ihn mit der erstellten Konfiguration aus:

```sh
outline-ss-server -config=config.yaml
```

## Schritt 2: Webserver freigeben {#step_2_expose_the_web_server}

Um Ihren WebSocket-Webserver öffentlich zugänglich zu machen, müssen Sie ihn im Internet freigeben und [TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security) konfigurieren.
Hierfür gibt es mehrere Optionen. Sie können einen lokalen Webserver wie [Caddy](https://caddyserver.com/), [nginx](https://nginx.org/) oder
[Apache](https://httpd.apache.org/) verwenden und sicherstellen, dass dieser ein gültiges TLS-Zertifikat hat. Oder Sie verwenden einen Tunneling-Dienst wie [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) oder [ngrok](https://ngrok.com/).

### Beispiel mit TryCloudflare {#example_using_trycloudflare}


:::caution
TryCloudflare ist ausschließlich für Demos und Tests vorgesehen.
:::

In diesem Beispiel erstellen wir mit [TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/) schnell einen Tunnel. So können Sie Ihren lokalen Webserver einfach und sicher freigeben, ohne Eingangs-Ports zu öffnen.

1. Laden Sie [`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) herunter und führen Sie die Installation durch.

2. Erstellen Sie einen Tunnel, der auf den Port Ihres lokalen Webservers zeigt:

```sh
cloudflared tunnel --url http://127.0.0.1:<WEB_SERVER_PORT>
```

Cloudflare stellt eine Subdomain (z. B. `acids-iceland-davidson-lb.trycloudflare.com`) für den Zugriff auf Ihren WebSocket-Endpunkt und die automatische Handhabung von TLS bereit. Notieren Sie sich die Subdomain. Sie benötigen sie später.

## Schritt 3: Dynamischen Zugriffsschlüssel erstellen {#step_3_create_a_dynamic_access_key}

Generieren Sie eine YAML-Datei mit dem Client-Zugriffsschlüssel für die Nutzer. Verwenden Sie dazu das Format für die [Zugriffsschlüssel-Konfiguration](../management/config) und die WebSocket-Endpunkte, die Sie zuvor auf Serverseite konfiguriert haben:

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN>/<TCP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>

  udp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN>/<UDP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>
```

Nachdem Sie die YAML-Datei mit dem dynamischen Zugriffsschlüssel erstellt haben, müssen Sie diese Ihren Nutzern zukommen lassen. Sie können die Datei auf einem statischen Webhosting-Dienst hosten oder dynamisch generieren. Weitere Informationen zur Verwendung von [dynamischen Zugriffsschlüsseln](../management/dynamic-access-keys)

## Schritt 4: Mit dem Outline-Client verbinden {#step_4_connect_with_the_outline_client}

Fügen Sie in einer der offiziellen [Outline-Client](../../download-links)-Anwendungen (ab Version 1.15.0) den gerade erstellten dynamischen Zugriffsschlüssel für den Server hinzu. Klicken Sie auf **Verbinden**, um mit der Shadowsocks-over-Websocket-Konfiguration eine Tunnelverbindung zu Ihrem Server herzustellen.

Vergewissern Sie sich mit einem Tool wie [IPInfo](https://ipinfo.io), dass Sie über Ihren Outline-Server mit dem Internet verbunden sind.
