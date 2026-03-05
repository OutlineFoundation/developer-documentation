---
title: "Configure Access Keys"
sidebar_label: "Configure Access Keys"
---

Outline nutzt eine YAML-basierte Konfiguration, um VPN-Parameter zu definieren und TCP-/UDP-Traffic zu bewältigen. Die Konfiguration unterstützt Komponierbarkeit auf mehreren Ebenen und ermöglicht so flexible und erweiterbare Setups.

[TunnelConfig](../reference/access-key-config#tunnelconfig) ist das Element auf oberster Ebene der Konfiguration.

## Beispiele

Eine typische Shadowsocks-Konfiguration sieht so aus:

Hinweis: TCP und UDP können über verschiedene Ports oder auf unterschiedlichen Endpunkten ausgeführt werden und sich in ihren Präfixen unterscheiden.

Sie können YAML-Anker und den Merge-Schlüssel `<<` verwenden, um Duplikate zu vermeiden:

Es ist jetzt möglich, Strategien zu komponieren und Multi-Hops auszuführen:

Statt „getarnte“ Protokolle wie Shadowsocks zu blockieren, können Sie Shadowsocks-over-WebSockets verwenden. In der [Server-Beispielkonfiguration](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml) sehen Sie, wie dies bereitgestellt wird. Eine Client-Konfiguration sieht so aus:

Hinweis: Der WebSocket-Endpunkt kann wiederum einen Endpunkt haben, der genutzt werden kann, um die DNS-basierte Blockierung zu umgehen:

Um die Kompatibilität mit unterschiedlichen Outline-Client-Versionen sicherzustellen, verwenden Sie die Option `first-supported` in Ihrer Konfiguration. Das ist besonders wichtig, da Outline neue Strategien und Funktionen hinzugefügt werden und möglicherweise nicht alle Nutzer die neueste Clientsoftware haben. Mit `first-supported` können Sie eine Konfiguration bereitstellen, die auf verschiedenen Plattformen und Clientversionen nahtlos funktioniert. So sorgen Sie für Abwärtskompatibilität und eine einheitliche Nutzererfahrung.
