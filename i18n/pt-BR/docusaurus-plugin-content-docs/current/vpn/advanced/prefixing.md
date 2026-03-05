---
title: "Disguise Connections with Prefixes"
sidebar_label: "Connection Prefixes"
---

A partir da versão 1.9.0 do app cliente do Outline, é possível usar prefixos com as chaves de acesso. Os
prefixos são uma lista de bytes usados no início do
[sal](https://shadowsocks.org/guide/aead.html) de uma conexão TCP do Shadowsocks.
Isso pode fazer com que a conexão funcione como um protocolo permitido na
rede, contornando firewalls que rejeitam protocolos não reconhecidos.

## Quando devo usar?

Se suspeitar que os usuários da implantação do Outline ainda estão sendo bloqueados, você
tente usar outros prefixos.

## Instruções

O prefixo só pode ter até 16 bytes. É possível que prefixos mais longos causem colisões de
sal, o que pode comprometer a segurança da criptografia e fazer com que as conexões sejam
detectadas. Use o menor prefixo possível para contornar o bloqueio que você estiver
enfrentando.

A porta usada deve ser a do protocolo que seu prefixo está fingindo ser.
A organização IANA mantém um [registro dos números porta de protocolo de transporte](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)
que mapeia protocolos e números de portas.

Alguns dos prefixos que funcionam são parecidos com protocolos comuns:

Porta recomendada
codificado para JSON
codificado para URL

solicitação HTTP
80 (http)
`"POST "`
`POST%20`

resposta HTTP
80 (http)
`"HTTP/1.1 "`
`HTTP%2F1.1%20`

solicitação DNS-sobre-TCP
53 (dns)
`"\u0005\u00DC\u005F\u00E0\u0001\u0020"`
`%05%C3%9C_%C3%A0%01%20`

TLS ClientHello
443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps-data), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (Apple APN), 5228 (Play Store), 5349 (turns)
`"\u0016\u0003\u0001\u0000\u00a8\u0001\u0001"`
`%16%03%01%00%C2%A8%01%01`

Dados de aplicação TLS
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

### Chaves de acesso dinâmicas

Para usar o recurso de prefixo com [chaves de acesso dinâmicas](../management/dynamic-access-keys) (`ssconf://`),
adicione uma chave como prefixo ao objeto JSON, com um valor **codificado para JSON**
representando o prefixo que você quer. Veja exemplos na tabela acima. Você pode
usar códigos de escape (como \u00FF) para representar pontos de código Unicode não imprimíveis no
intervalo entre `U+0` e `U+FF`. Por exemplo:

```json
{
    "server": "example.com",
    "server_port": 8388,
    "password": "example",
    "method": "chacha20-ietf-poly1305",
    "prefix": "\u0005\u00DC\u005F\u00E0\u0001\u0020"
}
```

### Chaves de acesso estáticas

Para usar prefixos com **chaves de acesso estáticas** (ss://), você precisa modificar sua
chave antes de distribuí-la. Se você tiver uma chave de acesso estática gerada
pelo Outline Manager, adicione uma versão **codificada para URL** do prefixo (exemplos
na tabela acima) no fim da chave, assim:

`ss://Z34nthataITHiTNIHTohithITHbVBqQ1o3bkk@127.0.0.1:33142/?outline=1&prefix=<your url-encoded prefix goes here>`

Se você é um usuário avançado, pode usar a função `encodeURIComponent()`
do navegador para converter o prefixo **codificado para JSON** em outro **codificado para URL**. Para fazer isso,
abra o console de inspeção na Web
(*Desenvolvedor > Console JavaScript na Web* no Chrome) e digite o seguinte:

```js
encodeURIComponent("<your json-encoded prefix goes here>")
```

Pressione "Enter". O valor resultante será a versão *codificada para URL*. Por exemplo:

```js
encodeURIComponent("\u0016\u0003\u0001\u0000\u00a8\u0001\u0001")
'%16%03%01%00%C2%A8%01%01'
```
