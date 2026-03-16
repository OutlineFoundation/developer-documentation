---
title: "Vermommingen van verbindingsvoorvoegsels"
sidebar_label: "Vermommingen van verbindingsvoorvoegsels"
---

Sinds Outline-client versie 1.9.0 ondersteunen toegangssleutels de optie om een 'prefix' (voorvoegsel) toe te voegen. De 'prefix' is een lijst met bytes die wordt gebruikt als de eerste bytes van de [salt](https://shadowsocks.org/guide/aead.html) van een Shadowsocks TCP-verbinding.
De verbinding lijkt dan op een protocol dat is toegestaan in het netwerk, waardoor firewalls worden omzeild die protocollen weigeren die ze niet herkennen.

## Wanneer moet ik dit proberen? {#when_should_i_try_this}

Als je denkt dat de gebruikers van je Outline-implementatie nog steeds worden geblokkeerd, kun je verschillende prefixes proberen.

## Instructies {#instructions}

De prefix mag niet langer zijn dan 16 bytes. Langere prefixes kunnen leiden tot salt-botsingen, wat de veiligheid van de versleuteling in gevaar kan brengen en ertoe kan leiden dat verbindingen worden gedetecteerd. Gebruik de kortst mogelijke prefix om de specifieke blokkade te omzeilen.

De poort die je gebruikt, moet overeenkomen met het protocol dat wordt gesimuleerd door de prefix.
IANA heeft een [lijst met poortnummers van transportprotocollen](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml).

Sommige voorbeelden van effectieve prefixes lijken op veelgebruikte protocollen:

Aanbevolen poort
Json-gecodeerd
URL-gecodeerd

HTTP-verzoek
80 (http)
`"POST "`
`POST%20`

HTTP-reactie
80 (http)
`"HTTP/1.1 "`
`HTTP%2F1.1%20`

DNS-over-TCP-verzoek
53 (dns)
`"\u0005\u00DC\u005F\u00E0\u0001\u0020"`
`%05%C3%9C_%C3%A0%01%20`

TLS ClientHello
443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps-data), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (Apple APN), 5228 (Play Store), 5349 (turns)
`"\u0016\u0003\u0001\u0000\u00a8\u0001\u0001"`
`%16%03%01%00%C2%A8%01%01`

TLS Application Data
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

### Dynamische toegangssleutels {#dynamic_access_keys}

Als je een prefix wilt gebruiken met [dynamische toegangssleutels](../management/dynamic-access-keys) (`ssconf://`), voeg je een 'prefix'-sleutel toe aan het json-object, met een **json-gecodeerde** waarde die de gewenste prefix aangeeft (ga naar de tabel hierboven voor voorbeelden). Je kunt escapecodes (zoals \u00FF) gebruiken om niet-afdrukbare Unicode-codepunten in het bereik `U+0` tot `U+FF` te vertegenwoordigen. Bijvoorbeeld:

```json
{
    "server": "example.com",
    "server_port": 8388,
    "password": "example",
    "method": "chacha20-ietf-poly1305",
    "prefix": "\u0005\u00DC\u005F\u00E0\u0001\u0020"
}
```

### Statische toegangssleutels {#static_access_keys}

Als je prefixes wilt gebruiken met **statische toegangssleutels** (ss://) moet je je bestaande sleutel aanpassen voordat je deze aan anderen geeft. Als je een statische toegangssleutel hebt die is gegenereerd door Outline Manager, neem je een **URL-gecodeerde** versie van de prefix (ga naar de tabel hierboven voor voorbeelden) en voeg je die op deze manier toe aan het einde van de toegangssleutel:

`ss://Z34nthataITHiTNIHTohithITHbVBqQ1o3bkk@127.0.0.1:33142/?outline=1&prefix=<your url-encoded prefix goes here>`

Geavanceerde gebruikers kunnen de functie `encodeURIComponent()` van de browser gebruiken om een **json-gecodeerde** prefix om te zetten in een **URL-gecodeerde** prefix. Open hiervoor de webinspectieconsole (in Chrome is dit *Ontwikkelaars > JavaScript-webconsole*) en typ het volgende:

```js
encodeURIComponent("<your json-encoded prefix goes here>")
```

Druk op Enter. De resulterende waarde is de *URL-gecodeerde* versie. Bijvoorbeeld:

```js
encodeURIComponent("\u0016\u0003\u0001\u0000\u00a8\u0001\u0001")
'%16%03%01%00%C2%A8%01%01'
```
