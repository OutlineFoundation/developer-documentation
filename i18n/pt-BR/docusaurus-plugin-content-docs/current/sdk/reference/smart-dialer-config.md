---
title: "Smart Dialer Configuration"
sidebar_label: "Smart Dialer Config"
---

O **Discador Inteligente** procura uma estratégia de desbloqueio de DNS e TLS para uma
lista de domínios de teste. Ele aceita configurações que descrevem várias estratégias
opcionais.

## Configuração do YAML para o Discador Inteligente

As configurações que o Discador Inteligente aceita devem estar no formato YAML. Veja um exemplo:

### Configuração do DNS

- O campo `dns` especifica uma lista de resolvedores de DNS para testar.

- Cada resolvedor de DNS pode ser de um dos seguintes tipos:

    - `system`: use o resolvedor do sistema. Especifique com um objeto vazio.

    - `https`: use um resolvedor criptografado de DNS sobre HTTPS (DoH).

    - `tls`: use um resolvedor criptografado de DNS sobre TLS (DoT).

    - `udp`: use um resolvedor de UDP.

    - `tcp`: use um resolvedor de TCP.

#### Resolvedor de DNS sobre HTTPS (DoH)

- `name`: o nome de domínio do servidor de DoH.

- `address`: o host:porta do servidor de DoH. O padrão é `name`:443.

#### Resolvedor de DNS sobre TLS (DoT)

- `name`: o nome de domínio do servidor de DoT.

- `address`: o host:porta do servidor de DoT. O padrão é `name`:853.

#### Resolvedor de UDP

- `address`: o host:porta do resolvedor de UDP.

#### Resolvedor de TCP

- `address`: o host:porta do resolvedor de TCP.

### Configuração de TLS

- O campo `tls` especifica uma lista de transportes de TLS para testar.

- Cada transporte de TLS é uma string que especifica o transporte a ser usado.

- Por exemplo, `override:host=cloudflare.net|tlsfrag:1` especifica um transporte
que usa domain fronting com Cloudflare e fragmentação de TLS. Confira a
[documentação de configuração](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x/configurl#hdr-Config_Format)
(em inglês) para mais detalhes.

### Configuração alternativa

Uma configuração alternativa é usada se a conexão não for possível com nenhuma das estratégias
sem proxy. Por exemplo, ela pode especificar um servidor proxy de backup para tentar conectar
o usuário. Ao usar uma configuração alternativa, o início será mais lento, já que primeiro as outras
estratégias de DNS/TLS precisam falhar ou exceder o tempo limite.

As strings alternativas devem ser:

- Uma string de configuração `StreamDialer` válida conforme definido em [`configurl`](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x/configurl#hdr-Proxy_Protocols) (em inglês).

- Um objeto de configuração Psiphon como filho de um campo `psiphon`.

#### Exemplo de servidor do Shadowsocks

#### Exemplo de servidor do SOCKS5

#### Exemplo de configuração do Psiphon

Para usar a rede [Psiphon](https://psiphon.ca/), você vai precisar:

1. Entrar em contato com a equipe do Psiphon para obter uma configuração que dê acesso à
rede deles. Isso pode requerer um contrato.

2. Adicionar a configuração do Psiphon que você recebeu à seção `fallback` da sua configuração do
Discador Inteligente. Já que JSON e YAML são compatíveis, você pode copiar e colar
sua configuração do Psiphon diretamente na seção `fallback`, assim:

### Como usar o Discador Inteligente

Para usar o Discador Inteligente, crie um objeto `StrategyFinder` e chame o
método `NewDialer`, transmitindo a lista de domínios de teste e a configuração do YAML.
O método `NewDialer` vai retornar um `transport.StreamDialer` que pode ser usado
para criar conexões usando a estratégia encontrada. Por exemplo:

Este é um exemplo básico. Adapte-o ao seu caso de uso específico.
