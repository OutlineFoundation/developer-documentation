---
title: "Disguise Connections as Web Traffic with Shadowsocks-over-WebSockets"
sidebar_label: "WebSockets"
---

*Outline-Client v1.15.0+*

Dieses Tutorial bietet eine Schritt-für-Schritt-Anleitung zur Implementierung von Shadowsocks-over-WebSockets, ein effektives Verfahren zur Umgehung von Zensuren in Umgebungen, in denen reguläre Shadowsocks-Verbindungen blockiert werden. Durch die Kapselung des Shadowsocks-Traffics in WebSockets können Sie ihn als Standard-Web-Traffic tarnen – für höhere Ausfallsicherheit und Zugänglichkeit.

## Schritt 1: Outline-Server konfigurieren und ausführen

Erstellen Sie eine neue `config.yaml`-Datei mit der folgenden Konfiguration:

Laden Sie den neuesten [`outline-ss-server`](https://github.com/Jigsaw-Code/outline-ss-server/releases) herunter und führen Sie ihn mit der erstellten Konfiguration aus:

## Schritt 2: Webserver freigeben

Um Ihren WebSocket-Webserver öffentlich zugänglich zu machen, müssen Sie ihn im Internet freigeben und [TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security) konfigurieren.
Hierfür gibt es mehrere Optionen. Sie können einen lokalen Webserver wie [Caddy](https://caddyserver.com/), [nginx](https://nginx.org/) oder
[Apache](https://httpd.apache.org/) verwenden und sicherstellen, dass dieser ein gültiges TLS-Zertifikat hat. Oder Sie verwenden einen Tunneling-Dienst wie [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) oder [ngrok](https://ngrok.com/).

### Beispiel mit TryCloudflare

In diesem Beispiel erstellen wir mit [TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/) schnell einen Tunnel. So können Sie Ihren lokalen Webserver einfach und sicher freigeben, ohne Eingangs-Ports zu öffnen.

1. Laden Sie [`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) herunter und führen Sie die Installation durch.

2. Erstellen Sie einen Tunnel, der auf den Port Ihres lokalen Webservers zeigt:

Cloudflare stellt eine Subdomain (z. B. `acids-iceland-davidson-lb.trycloudflare.com`) für den Zugriff auf Ihren WebSocket-Endpunkt und die automatische Handhabung von TLS bereit. Notieren Sie sich die Subdomain. Sie benötigen sie später.

## Schritt 3: Dynamischen Zugriffsschlüssel erstellen

Generieren Sie eine YAML-Datei mit dem Client-Zugriffsschlüssel für die Nutzer. Verwenden Sie dazu das Format für die [Zugriffsschlüssel-Konfiguration](../management/config) und die WebSocket-Endpunkte, die Sie zuvor auf Serverseite konfiguriert haben:

Nachdem Sie die YAML-Datei mit dem dynamischen Zugriffsschlüssel erstellt haben, müssen Sie diese Ihren Nutzern zukommen lassen. Sie können die Datei auf einem statischen Webhosting-Dienst hosten oder dynamisch generieren. Weitere Informationen zur Verwendung von [dynamischen Zugriffsschlüsseln](../management/dynamic-access-keys)

## Schritt 4: Mit dem Outline-Client verbinden

Fügen Sie in einer der offiziellen [Outline-Client](../../download-links)-Anwendungen (ab Version 1.15.0) den gerade erstellten dynamischen Zugriffsschlüssel für den Server hinzu. Klicken Sie auf **Verbinden**, um mit der Shadowsocks-over-Websocket-Konfiguration eine Tunnelverbindung zu Ihrem Server herzustellen.

Vergewissern Sie sich mit einem Tool wie [IPInfo](https://ipinfo.io), dass Sie über Ihren Outline-Server mit dem Internet verbunden sind.
