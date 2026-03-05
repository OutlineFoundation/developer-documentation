---
title: "Dynamic Access Keys"
sidebar_label: "Dynamic Access Keys"
---

Outline offre due tipi di chiavi di accesso: statiche e dinamiche. Le chiavi statiche codificano tutte le informazioni di connessione all'interno della chiave stessa, mentre le chiavi dinamiche codificano la posizione delle informazioni di connessione, consentendoti di archiviare queste informazioni in remoto e modificarle in base alle tue necessità. Ciò significa che puoi aggiornare la configurazione del server senza dover generare e distribuire nuove chiavi ai tuoi utenti. Questo documento spiega come utilizzare le chiavi di accesso dinamiche per una gestione più flessibile ed efficiente del server Outline.

Sono disponibili tre formati per specificare le informazioni di accesso che verranno utilizzate dalle chiavi di accesso dinamiche:

### Utilizza un link `ss://`

*Client Outline 1.8.1 e versioni successive.*

Puoi utilizzare direttamente un link `ss://` esistente. Questo metodo è ideale se non hai bisogno di cambiare frequentemente il server, la porta o il metodo di crittografia, ma desideri comunque avere la flessibilità di aggiornare l'indirizzo del server.

**Esempio:**

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

### Utilizza un oggetto JSON

*Client Outline 1.8.0 e versioni successive.*

Questo metodo offre maggiore flessibilità nella gestione di tutti gli aspetti della connessione Outline dei tuoi utenti. In questo modo puoi aggiornare il server, la porta, la password e il metodo di crittografia.

**Esempio:**

```json
{
  "server": "outline-server.example.com",
  "server_port": 8388,
  "password": "example",
  "method": "chacha20-ietf-poly1305"
}
```

- **server:** il dominio o l'indirizzo IP del tuo server VPN.

- **server_port:** il numero di porta su cui è in esecuzione il tuo server VPN.

- **password:** la password necessaria per connettersi alla VPN.

- **method:** il metodo di crittografia utilizzato dalla VPN. Consulta i [cifrari di crittografia autenticata con dati associati](https://shadowsocks.org/doc/aead.html) supportati da Shadowsocks.

### Utilizza un oggetto YAML

*Client Outline 1.15.0 e versioni successive.*

Questo metodo è simile al precedente metodo JSON, ma aggiunge ancora più flessibilità sfruttando il formato di configurazione avanzato di Outline. Puoi aggiornare il server, la porta, la password, il metodo di crittografia e molto altro.

**Esempio:**

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

- **transport:** definisce i protocolli di trasporto da utilizzare (in questo caso TCP e UDP).

- **tcp/udp:** specifica la configurazione per ciascun protocollo.

    - **$type:** indica il tipo di configurazione, in questo caso shadowsocks.

    - **endpoint:** il dominio o l'indirizzo IP e la porta del tuo server VPN.

    - **secret:** la password necessaria per connettersi alla VPN.

    - **cipher:** il metodo di crittografia utilizzato dalla VPN. Consulta i [cifrari di crittografia autenticata con dati associati](https://shadowsocks.org/doc/aead.html) supportati da Shadowsocks.

Consulta [Configurazione delle chiavi di accesso](config) per informazioni dettagliate su tutti i modi in cui puoi configurare l'accesso al server Outline, inclusi trasporti, endpoint, dialer e listener di pacchetti.

## Estrai le informazioni di accesso da una chiave statica

Se hai una chiave di accesso statica esistente, puoi estrarre le informazioni per creare una chiave di accesso dinamica basata su JSON o YAML. Le chiavi di accesso statiche seguono questo pattern:

```none
SS-URI = "ss://" userinfo "@" hostname ":" port [ "/" ] [ "#" tag ]
userinfo = websafe-base64-encode-utf8(method  ":" password)
           method ":" password
```

Esempio:

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

- **Server:** `outline-server.example.com`

- **Porta server:** `8388`

- **Informazioni utente:** `Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl` decodificato come [base64](https://en.wikipedia.org/wiki/Base64) utilizzando uno strumento come la [codifica/decodifica di Strumenti amministrativi Google](https://toolbox.googleapps.com/apps/encode_decode/)

    - **Metodo:** `chacha20-ietf-poly1305`

    - **Password:** `example`

## Scegli una piattaforma di hosting

Ora che hai capito come creare le chiavi di accesso dinamiche, è importante scegliere una piattaforma di hosting adatta per la configurazione delle tue chiavi di accesso. Per prendere questa decisione, valuta fattori come l'affidabilità, la sicurezza, la facilità d'uso e la resistenza alla censura della piattaforma. La piattaforma fornirà costantemente le informazioni relative alle tue chiavi di accesso senza tempi di inattività? Offre misure di sicurezza appropriate per proteggere la tua configurazione? Quanto è facile gestire le informazioni relative alle tue chiavi di accesso sulla piattaforma? La piattaforma è accessibile in regioni con censura di internet?

Per i casi in cui l'accesso alle informazioni potrebbe essere limitato, prendi in considerazione l'hosting su piattaforme resistenti alla censura come [Google Drive](https://drive.google.com), [pad.riseup.net](https://pad.riseup.net/), [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html) (con accesso in stile percorso), [Netlify](https://dev.to/alexmercedcoder/delivering-json-data-with-netlify-1j96) o i [secret gist di GitHub](https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists/creating-gists).
Valuta le esigenze specifiche del tuo deployment e scegli una piattaforma che si allinei ai tuoi requisiti di accessibilità e sicurezza.
