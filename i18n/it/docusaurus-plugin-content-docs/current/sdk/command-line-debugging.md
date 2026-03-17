---
title: "Caratterizzazione e bypass da remoto delle interferenze di rete con l'SDK Outline"
sidebar_label: "Caratterizzazione e bypass da remoto delle interferenze di rete con l'SDK Outline"
---

Questa guida mostra come utilizzare gli strumenti a riga di comando dell'SDK Outline per
comprendere e aggirare le interferenze di rete da una prospettiva remota. Imparerai a utilizzare gli strumenti dell'SDK per misurare le interferenze di rete, testare le strategie di elusione e analizzare i risultati. Questa guida si concentrerà sugli strumenti
`resolve`, `fetch` e `http2transport`.

## Iniziare a utilizzare gli strumenti dell'SDK Outline

Puoi iniziare a utilizzare gli strumenti dell'SDK Outline direttamente dalla riga di comando.

### Risolvi DNS

Lo strumento `resolve` ti consente di eseguire ricerche DNS con un resolver specificato.

Per risolvere un record A di un dominio:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type A 1.2.3.4.nip.io
```

Per risolvere un record CNAME:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type CNAME www.google.com
```

### Recuperare una pagina web

Lo strumento `fetch` può essere utilizzato per recuperare i contenuti di una pagina web.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest https://example.com
```

Può anche forzare la connessione a utilizzare QUIC.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -proto=h3 https://www.youtube.com
```

### Utilizzare un proxy locale

Lo strumento `http2transport` crea un proxy locale per instradare il traffico.
Per avviare un proxy locale con un trasporto Shadowsocks:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/http2transport@latest -localAddr 127.0.0.1:8080 -transport "ss://{your_shadowsocks_credentials}"
```

Puoi quindi utilizzare questo proxy con altri strumenti come curl:

```sh
curl -p -x http://127.0.0.1:8080 https://ipinfo.io
```

## Specificare le strategie di elusione

L'SDK Outline consente la specifica di varie strategie di elusione
che possono essere combinate per aggirare diverse forme di interferenza di rete. Le
specifiche di queste strategie sono riportate nella [documentazione di Go](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl).

### Strategie componibili

Queste strategie possono essere combinate per creare tecniche di elusione più efficaci.

* **DNS over HTTPS con frammentazione TLS**: `doh:name=cloudflare-dns.com&address=cloudflare.net:443 | tlsfrag:1`

* **SOCKS5 su TLS con Domain Fronting**: `tls:sni=decoy.example.com&certname=[HOST] | socks5:[HOST]:[PORT]`

* **Routing multi-hop con Shadowsocks**: `ss://[USERINFO1]@[HOST1]:[PORT1] | ss://[USERINFO2]@[HOST2]:[PORT2] | ss://[USERINFO3]@[HOST3]:[PORT3]`

## Accesso remoto e misurazione

Per misurare le interferenze di rete così come vengono percepite in regioni diverse, puoi utilizzare proxy remoti. Puoi trovare o creare proxy remoti a cui connetterti.

### Opzioni di accesso remoto

Utilizzando lo strumento `fetch` puoi testare le connessioni da remoto in vari modi.

#### Server Outline

Connettiti in remoto a un server Outline standard con un trasporto Shadowsocks.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "ss://{remote_shadowsocks_credentials}" https://ipinfo.io | jq
```

#### SOCKS5 su SSH

Crea un proxy SOCKS5 utilizzando un tunnel SSH.

```sh
ssh -D 127.0.0.1:1080 -C -N $USER@$HOST:$PORT
```

Connettiti a questo tunnel utilizzando fetch

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "socks5://localhost:1080" https://ipinfo.io | jq
```

## Case study: aggirare il blocco di YouTube in Iran

Ecco un esempio pratico di rilevamento e bypass delle interferenze di rete.

### Rilevare il blocco

Quando si tenta di recuperare la home page di YouTube tramite un proxy iraniano, la richiesta
scade, indicando un blocco.

```sh
export TRANSPORT="ss://{remote_shadowsocks_credentials}"
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)" https://www.youtube.com
```

Questo comando non va a buon fine e si verifica un timeout.

### Aggiramento con la frammentazione TLS

Se aggiungiamo la frammentazione TLS al trasporto, possiamo aggirare questo blocco.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)|tlsfrag:1" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Questo comando recupera correttamente il titolo della home page di YouTube, ovvero
`<title>YouTube</title>`.

### Bypass con frammentazione TLS e DNS over HTTPS

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|tlsfrag:1|doh:name=cloudflare-dns.com&address=www.cloudflare.net" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Restituisce correttamente anche `<title>YouTube</title>`.

### Eseguire il bypass con un server Outline

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|ss://<your_shadowsocks_credentials>" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Anche questa restituisce `<title>YouTube</title>`.

## Ulteriori analisi e risorse

Per discussioni e domande, visita il [gruppo di discussione dell'SDK Outline](https://github.com/OutlineFoundation/outline-sdk/discussions).
