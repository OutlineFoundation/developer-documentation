---
title: "Dynamic Access Keys"
sidebar_label: "Dynamic Access Keys"
---

Outline biedt 2 typen toegangssleutels: statische en dynamische. Statische sleutels coderen alle verbindingsinformatie in de sleutel zelf. Dynamische sleutels coderen de locatie van de verbindingsinformatie, zodat je die op afstand kunt opslaan en indien nodig kunt wijzigen. Je kunt dan je serverconfiguratie updaten zonder nieuwe sleutels te hoeven maken en naar je gebruikers te sturen. In dit document staat uitgelegd hoe je dynamische toegangssleutels kunt gebruiken om je Outline-server flexibeler en efficiënter te beheren.

Er zijn 3 indelingen om de toegangsinformatie op te geven die de dynamische toegangssleutels gebruiken:

### Een `ss://`-link gebruiken

*Outline-client v1.8.1+.*

Je kunt een bestaande `ss://`-link rechtstreeks gebruiken. Deze methode is ideaal als je de server, poort of versleutelingsmethode niet regelmatig hoeft te wijzigen, maar nog wel de flexibiliteit wilt hebben om het serveradres te updaten.

**Voorbeeld:**

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

### Een json-object gebruiken

*Outline-client v1.8.0+.*

Met deze methode heb je de flexibiliteit om alle aspecten van de Outline-verbinding van je gebruikers te beheren. Hiermee kun je de server, de poort, het wachtwoord en de versleutelingsmethode updaten.

**Voorbeeld:**

```json
{
  "server": "outline-server.example.com",
  "server_port": 8388,
  "password": "example",
  "method": "chacha20-ietf-poly1305"
}
```

- **server:** Het domein of IP-adres van je VPN-server.

- **server_port:** Het poortnummer waarop je VPN-server wordt uitgevoerd.

- **password:** Het wachtwoord om verbinding te maken met de VPN.

- **method:** De versleutelingsmethode die de VPN gebruikt. Controleer de door Shadowsocks ondersteunde [AEAD-coderingen](https://shadowsocks.org/doc/aead.html).

### Een YAML-object gebruiken

*Outline-client v1.15.0+.*

Deze methode lijkt op de eerder genoemde json-methode, maar voegt nog meer flexibiliteit toe door de geavanceerde configuratie-indeling van Outline in te zetten. Je kunt naast de server, de poort, het wachtwoord en de versleutelingsmethode nog veel meer updaten.

**Voorbeeld:**

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

- **transport:** De transportprotocollen die moeten worden gebruikt (in dit geval TCP en UDP).

- **tcp/udp:** De configuratie voor elk protocol.

    - **$type:** Het type configuratie, in dit geval Shadowsocks.

    - **endpoint:** Het domein of IP-adres en de poort van je VPN-server.

    - **secret:** Het wachtwoord om verbinding te maken met de VPN.

    - **cipher:** De versleutelingsmethode die de VPN gebruikt. Controleer de door Shadowsocks ondersteunde [AEAD-coderingen](https://shadowsocks.org/doc/aead.html).

Ga naar [Configuratie van toegangssleutel](config) voor informatie over alle manieren waarop je de toegang tot je Outline-server kunt instellen, inclusief transporten, eindpunten, dialers en pakketlisteners.

## Toegangsinformatie ophalen uit een statische sleutel

Als je een bestaande statische sleutel hebt, kun je de informatie daaruit ophalen om een op json of YAML gebaseerde dynamische toegangssleutel te maken. Statische toegangssleutels volgen dit patroon:

```none
SS-URI = "ss://" userinfo "@" hostname ":" port [ "/" ] [ "#" tag ]
userinfo = websafe-base64-encode-utf8(method  ":" password)
           method ":" password
```

Voorbeeld:

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

- **Server:** `outline-server.example.com`

- **Serverpoort:** `8388`

- **Gebruikersgegevens:** `Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl` Gedecodeerd als [base64](https://en.wikipedia.org/wiki/Base64) via een tool als [Encode/Decode in de Google Admin Toolbox](https://toolbox.googleapps.com/apps/encode_decode/)

    - **Methode**: `chacha20-ietf-poly1305`

    - **Wachtwoord**: `example`

## Een hostingplatform kiezen

Nu je weet hoe je dynamische toegangssleutels maakt, is het belangrijk dat je een geschikt hostingplatform kiest voor de configuratie van je toegangssleutel. Neem hierbij de betrouwbaarheid, de beveiliging, het gebruiksgemak en de weerbaarheid tegen censuur in overweging. Geeft het platform je toegangssleutel continu weer zonder downtime? Biedt het platform de juiste beveiligingsmaatregelen om je configuratie te beschermen? Hoe makkelijk is het om de gegevens van je toegangssleutel te beheren via het platform? Is het platform toegankelijk in regio's waar het internet wordt gecensureerd?

Voor situaties waar de toegang tot informatie mogelijk beperkt is, raden we je aan je configuratie te hosten op platforms die bestand zijn tegen censuur, zoals [Google Drive](https://drive.google.com), [pad.riseup.net](https://pad.riseup.net/), [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html) (met toegang in padvorm), [Netlify](https://dev.to/alexmercedcoder/delivering-json-data-with-netlify-1j96) of [geheime gists op GitHub](https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists/creating-gists).
Breng de specifieke behoeften van je implementatie in kaart en kies een platform dat voldoet aan je vereisten voor toegankelijkheid en beveiliging.
