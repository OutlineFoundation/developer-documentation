---
title: "Disguise Connections with Prefixes"
sidebar_label: "Connection Prefixes"
---

A partire dalla versione 1.9.0 del client Outline, i tasti di accesso supportano l'opzione "prefisso". Il
"prefisso" è un elenco di byte utilizzati come primi byte del
[salt](https://shadowsocks.org/guide/aead.html) di una connessione TCP Shadowsocks.
Ciò può far apparire la connessione come un protocollo consentito nella
rete, aggirando i firewall che rifiutano i protocolli che non riconoscono.

## Quando dovrei verificarlo?

Se sospetti che gli utenti del tuo deployment Outline siano ancora bloccati, potresti provare alcuni prefissi diversi.

## Istruzioni

Il prefisso non deve essere più lungo di 16 byte. Prefissi più lunghi possono causare conflitti
di salt, che possono compromettere la sicurezza della crittografia e causare il rilevamento
delle connessioni. Usa il prefisso più breve che puoi per aggirare il blocco che stai
affrontando.

La porta utilizzata deve corrispondere al protocollo che il prefisso finge di essere.
IANA mantiene un [registro dei numeri di porta del protocollo di trasporto](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)
che mappa i protocolli e i numeri di porta.

Alcuni esempi di prefissi efficaci sono simili ai protocolli comuni:

Porta consigliata
Con codifica JSON
Con codifica URL

Richiesta HTTP
80 (http)
`"POST "`
`POST%20`

Risposta HTTP
80 (http)
`"HTTP/1.1 "`
`HTTP%2F1.1%20`

Richiesta DNS-over-TCP
53 (dns)
`"\u0005\u00DC\u005F\u00E0\u0001\u0020"`
`%05%C3%9C_%C3%A0%01%20`

ClientHello TLS
443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps-data), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (Apple APN), 5228 (Play Store), 5349 (turns)
`"\u0016\u0003\u0001\u0000\u00a8\u0001\u0001"`
`%16%03%01%00%C2%A8%01%01`

Dati applicazioni TLS
443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps-data), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (Apple APN), 5228 (Play Store), 5349 (turns)
`"\u0013\u0003\u0003\u003F"`
`%13%03%03%3F`

ServerHello TLS
443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps-data), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (Apple APN), 5228 (Play Store), 5349 (turns)
`"\u0016\u0003\u0003\u0040\u0000\u0002"`
`%16%03%03%40%00%02`

SSH
22 (ssh), 830 (netconf-ssh), 4334 (netconf-ch-ssh), 5162 (snmpssh-trap)
`"SSH-2.0\r\n"`
`SSH-2.0%0D%0A`

### Chiavi di accesso dinamiche

Per utilizzare la funzionalità prefisso con [chiavi di accesso dinamiche](../management/dynamic-access-keys) (`ssconf://`),
aggiungi una chiave "prefisso" all'oggetto JSON, con un valore **JSON-encoded**
che rappresenta il prefisso desiderato (vedi esempi nella tabella sopra)_. Puoi
utilizzare codici di escape (come \u00FF) per rappresentare codepoint Unicode non stampabili nell'intervallo da `U+0` a `U+FF`. Ad esempio:

```json
{
    "server": "example.com",
    "server_port": 8388,
    "password": "example",
    "method": "chacha20-ietf-poly1305",
    "prefix": "\u0005\u00DC\u005F\u00E0\u0001\u0020"
}
```

### Chiavi di accesso statiche

Per utilizzare i prefissi con **chiavi di accesso statiche** (ss://), dovrai modificare la
chiave esistente prima di distribuirla. Se hai una chiave di accesso statica generata
da Outline Manager, prendi una versione **con codifica URL** del tuo prefisso (vedi esempi
nella tabella sopra) e aggiungila alla fine della chiave di accesso in questo modo:

`ss://Z34nthataITHiTNIHTohithITHbVBqQ1o3bkk@127.0.0.1:33142/?outline=1&prefix=<your url-encoded prefix goes here>`

Per gli utenti avanzati, è possibile utilizzare la funzione `encodeURIComponent()` del browser
per convertire il prefisso **con codifica JSON** in uno **con codifica URL**. Per fare ciò,
apri la console dell'ispezione web
(*Sviluppatore > Console web JavaScript* su Chrome) e digita quanto segue:

```js
encodeURIComponent("<your json-encoded prefix goes here>")
```

Premi Invio. Il valore prodotto sarà la versione *con codifica URL*. Ad esempio:

```js
encodeURIComponent("\u0016\u0003\u0001\u0000\u00a8\u0001\u0001")
'%16%03%01%00%C2%A8%01%01'
```
