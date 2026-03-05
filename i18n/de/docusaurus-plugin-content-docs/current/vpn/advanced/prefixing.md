---
title: "Disguise Connections with Prefixes"
sidebar_label: "Connection Prefixes"
---

Bei Version 1.9.0 des Outline-Clients unterstützen Zugriffsschlüssel die Option „Präfixe“. Ein
„Präfix“ ist eine Liste mit Bytes, die als erste Bytes des
[Salt](https://shadowsocks.org/guide/aead.html) einer Shadowsocks TCP-Verbindung verwendet werden.
Dadurch wirkt die Verbindung möglicherweise wie ein Protokoll, das im Netzwerk zugelassen ist, und umgeht Firewalls, die eigentlich unbekannte Protokolle abwehren.

## Wann sollte ich das anwenden?

Wenn Sie annehmen, dass die Nutzer Ihrer Outline-Bereitstellung noch immer blockiert werden, können Sie weitere Präfixe anwenden.

## Anleitung

Das Präfix sollte nicht länger sein als 16 Bytes. Längere Präfixe könnten Salt-Kollisionen verursachen. Dadurch könnte die Sicherheit der Verschlüsselung beeinträchtigt und Verbindungen entdeckt werden. Nutzen Sie das kürzeste Präfix, das Sie kennen, um die Blockierung zu umgehen.

Der von Ihnen genutzte Port sollte mit dem Protokoll übereinstimmen, als das Ihr Präfix sich ausgibt.
IANA gibt eine [Liste registrierter Portnummern für Transportprotokolle](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml) vor, die Protokolle und Portnummern enthält.

Die folgenden Beispiele zeigen effektiver Präfixe:

Empfohlener Port
Im JSON-Format verschlüsselt
URL-codiert:

HTTP-Anfrage
80 (http)
`"POST "`
`POST%20`

HTTP-Antwort
80 (http)
`"HTTP/1.1 "`
`HTTP%2F1.1%20`

DNS-über-TCP-Anfrage
53 (dns)
`"\u0005\u00DC\u005F\u00E0\u0001\u0020"`
`%05%C3%9C_%C3%A0%01%20`

TLS ClientHello
443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps-data), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (Apple APN), 5228 (Play Store), 5349 (turns)
`"\u0016\u0003\u0001\u0000\u00a8\u0001\u0001"`
`%16%03%01%00%C2%A8%01%01`

TLS-Anwendungsdaten
443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps-data), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (Apple APN), 5228 (Play Store), 5349 (turns)
`"\u0013\u0003\u0003\u003F"`
`%13%03%03%3F`

TLS ServerHello
443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps-data), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (Apple APN), 5228 (Play Store), 5349 (turns)
`"\u0016\u0003\u0003\u0040\u0000\u0002"`
`%16%03%03%40%00%02`

SSH
22 (ssh), 830 (netconf-ssh), 4334 (netconf-ch-ssh), 5162 (snmpssh-trap)
`"SSH-2.0\r\n"`
`SSH-2.0%0D%0A`

### Dynamische Zugriffsschlüssel

Um die Präfix-Funktion mit [dynamischen Zugriffsschlüsseln](../management/dynamic-access-keys) (`ssconf://`) zu nutzen,
fügen Sie dem JSON-Objekt einen „Präfix“ hinzu. Dabei sollte ein **im JSON-Format verschlüsselter** Wert
den Präfix repräsentieren, den Sie möchten (Siehe Beispiele in der Tabelle oben). Sie können Escape-Codes (wie \u00FF) verwenden, um nicht druckbare Unicode-Zeichen im Bereich `U+0` bis `U+FF` zu repräsentieren. Beispiel:

### Statische Zugriffsschlüssel

Um Präfixe mit **statischen Zugriffsschlüsseln** (ss://) zu verwenden, müssen Sie Ihren bestehenden Schlüssel ändern, bevor Sie ihn bereitstellen. Wenn Sie einen vom Outline-Manager erstellten Zugriffsschlüssel haben, verwenden Sie eine **URL-codierte** Version Ihres Präfixes (siehe Beispiele in der Tabelle oben) und fügen Sie sie wie im Folgenden beschrieben am Ende des Zugriffsschlüssels ein:

`ss://Z34nthataITHiTNIHTohithITHbVBqQ1o3bkk@127.0.0.1:33142/?outline=1&prefix=<your url-encoded prefix goes here>`

Fortgeschrittene Nutzer können die `encodeURIComponent()`-Funktion ihres Browsers nutzen, um ihren **JSON-codierten** Präfix in ein **URL-codiertes** zu konvertieren. Rufen Sie dafür Ihre Web Inspector-Konsole auf (*Entwickler> JavaScript Web Console *auf Chrome), und tippen Sie das Folgende ein:

Drücken Sie die Eingabetaste. Der erzielte Wert ist die *URL-codierte *Version. Beispiel:
