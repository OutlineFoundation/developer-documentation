---
title: "Command Line Debugging"
sidebar_label: "Command Line Debugging"
---

Este guia demonstra como usar as ferramentas de linha de comando do SDK do Outline para
entender e evitar interferências de rede de uma perspectiva remota. Você vai aprender a usar as ferramentas do SDK para medir a interferência na rede, testar estratégias de evasão e analisar os resultados. Este guia vai se concentrar nas ferramentas
`resolve`, `fetch` e `http2transport`.

## Como começar a usar as ferramentas do SDK Outline

Você pode começar a usar as ferramentas do SDK do Outline diretamente na linha de comando.

### Resolver DNS

Com a ferramenta `resolve`, é possível fazer pesquisas de DNS com um resolvedor especificado.

Para resolver um registro A de um domínio:

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type A 1.2.3.4.nip.io
```

Para resolver um registro CNAME:

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type CNAME www.google.com
```

### Buscar uma página da Web

A ferramenta `fetch` pode ser usada para recuperar o conteúdo de uma página da Web.

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest https://example.com
```

Ele também pode forçar a conexão a usar o QUIC.

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -proto=h3 https://www.youtube.com
```

### Usar um proxy local

A ferramenta `http2transport` cria um proxy local para rotear seu tráfego.
Para iniciar um proxy local com um transporte do Shadowsocks:

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/http2transport@latest -localAddr 127.0.0.1:8080 -transport "ss://{your_shadowsocks_credentials}"
```

Em seguida, use esse proxy com outras ferramentas, como curl:

```sh
curl -p -x http://127.0.0.1:8080 https://ipinfo.io
```

## Especificar estratégias de fraude

O SDK do Outline permite a especificação de várias estratégias de evasão
que podem ser combinadas para contornar diferentes formas de interferência na rede. A especificação dessas estratégias está na [documentação do Go](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x@v0.0.3/configurl).

### Estratégias combináveis

Essas estratégias podem ser combinadas para criar técnicas de evasão mais robustas.

* **DNS sobre HTTPS com fragmentação TLS**: `doh:name=cloudflare-dns.com&address=cloudflare.net:443 | tlsfrag:1`

* **SOCKS5 por TLS com Domain Fronting**: `tls:sni=decoy.example.com&certname=[HOST] | socks5:[HOST]:[PORT]`

* **Roteamento de vários saltos com Shadowsocks**: `ss://[USERINFO1]@[HOST1]:[PORT1] | ss://[USERINFO2]@[HOST2]:[PORT2] | ss://[USERINFO3]@[HOST3]:[PORT3]`

## Acesso e medição remotos

Para medir a interferência de rede em diferentes regiões, use proxies remotos. Você pode encontrar ou criar proxies remotos para se conectar.

### Opções de acesso remoto

Com a ferramenta `fetch`, é possível testar conexões remotamente de várias maneiras.

#### Servidor do Outline

Conecte-se remotamente a um servidor padrão do Outline com um transporte do Shadowsocks.

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "ss://{remote_shadowsocks_credentials}" https://ipinfo.io | jq
```

#### SOCKS5 por SSH

Crie um proxy SOCKS5 usando um túnel SSH.

```sh
ssh -D 127.0.0.1:1080 -C -N $USER@$HOST:$PORT
```

Conecte-se a esse túnel usando fetch

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "socks5://localhost:1080" https://ipinfo.io | jq
```

## Estudo de caso: como burlar o bloqueio do YouTube no Irã

Confira um exemplo prático de como detectar e ignorar interferências na rede.

### Detectar o bloqueio

Ao tentar buscar a página inicial do YouTube por um proxy iraniano, a solicitação
expira, indicando um bloqueio.

```sh
export TRANSPORT="ss://{remote_shadowsocks_credentials}"
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)" https://www.youtube.com
```

Esse comando falha com um tempo limite.

### Bypass com fragmentação TLS

Ao adicionar a fragmentação de TLS ao transporte, podemos contornar esse bloqueio.

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)|tlsfrag:1" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Esse comando recupera o título da página inicial do YouTube, que é
`<title>YouTube</title>`.

### Bypass com fragmentação TLS e DNS sobre HTTPS

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|tlsfrag:1|doh:name=cloudflare-dns.com&address=www.cloudflare.net" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Isso também retorna `<title>YouTube</title>`.

### Burlar com um servidor do Outline

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|ss://<your_shadowsocks_credentials>" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Isso também retorna `<title>YouTube</title>`.

## Mais análises e recursos

Para discussões e perguntas, acesse o [grupo de discussão do SDK do Outline](https://github.com/Jigsaw-Code/outline-sdk/discussions).
