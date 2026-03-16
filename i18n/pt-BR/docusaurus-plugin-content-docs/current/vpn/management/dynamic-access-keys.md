---
title: "Dynamic Access Keys"
sidebar_label: "Dynamic Access Keys"
---

O Outline oferece dois tipos de chaves de acesso: estáticas e dinâmicas. As chaves estáticas codificam
todas as informações de conexão na própria chave, enquanto as dinâmicas codificam
a localização das informações de conexão, permitindo armazená-las remotamente e alterá-las, se necessário. Isso significa que você pode atualizar
a configuração do seu servidor sem precisar gerar e distribuir novas chaves para seus
usuários. Este documento explica como usar as chaves de acesso dinâmicas para um gerenciamento
mais flexível e eficiente do seu servidor Outline.

Existem três formatos para especificar as informações de acesso que serão usadas por
suas chaves de acesso dinâmicas:

### Usar um link `ss://` {#use_an_ss_link}

*App cliente do Outline v1.8.1+.*

Você pode usar um link `ss://`. Esse método é ideal se você não
precisa alterar frequentemente o servidor, a porta ou o método de criptografia, mas ainda quer
ter flexibilidade para atualizar o endereço do servidor.

**Exemplo:**

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

### Usar um objeto JSON {#use_a_json_object}

*App cliente do Outline v1.8.0+.*

Esse método oferece mais flexibilidade para gerenciar todos os aspectos da conexão dos seus usuários
com o Outline. Ele permite atualizar o servidor, a porta, a senha e o método
de criptografia.

**Exemplo:**

```json
{
  "server": "outline-server.example.com",
  "server_port": 8388,
  "password": "example",
  "method": "chacha20-ietf-poly1305"
}
```

- **server**: domínio ou endereço IP do seu servidor de VPN.

- **server_port**: número da porta em que o servidor de VPN está sendo executado.

- **password**: senha necessária para se conectar à VPN.

- **method**: método de criptografia usado pela VPN. Consulte a [criptografia AEAD](https://shadowsocks.org/doc/aead.html) (em inglês) oferecida pelo Shadowsocks.

### Usar um objeto YAML {#use_a_yaml_object}

*App cliente do Outline v1.15.0+.*

Esse método é semelhante ao método JSON anterior, mas oferece ainda mais
flexibilidade ao aproveitar o formato de configuração avançado do Outline. Você pode
atualizar o servidor, a porta, a senha, o método de criptografia e muito mais.

**Exemplo:**

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

- **transport**: define os protocolos de transporte a serem usados (TCP e UDP,
neste caso).

- **tcp/udp**: especifica a configuração para cada protocolo.

    - **$type**: indica o tipo de configuração. Neste caso, é o Shadowsocks.

    - **endpoint**: domínio ou endereço IP e porta do seu servidor de VPN.

    - **secret**: senha necessária para se conectar à VPN.

    - **cipher**: método de criptografia usado pela VPN. Consulte a
[criptografia AEAD](https://shadowsocks.org/doc/aead.html) (em inglês) aceitas
pelo Shadowsocks.

Consulte [Configuração de chave de acesso](config) para obter detalhes sobre as maneiras
de configurar o acesso ao seu servidor Outline, incluindo transportes, endpoints,
discadores e listeners de pacotes.

## Extrair informações de acesso de uma chave estática {#extract_access_information_from_a_static_key}

Se você tiver uma chave de acesso estática, poderá extrair as informações para
criar uma chave de acesso dinâmica baseada em JSON ou YAML. As chaves de acesso estáticas obedecem ao
seguinte padrão:

```none
SS-URI = "ss://" userinfo "@" hostname ":" port [ "/" ] [ "#" tag ]
userinfo = websafe-base64-encode-utf8(method  ":" password)
           method ":" password
```

Exemplo:

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

- **Servidor**: `outline-server.example.com`

- **Porta do servidor**: `8388`

- **Informações do usuário**: `Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl` decodificadas como
[base64](https://en.wikipedia.org/wiki/Base64) com uma ferramenta como a [Codificação/Decodificação
do Google
Admin Toolbox](https://toolbox.googleapps.com/apps/encode_decode/)

    - **Método**: `chacha20-ietf-poly1305`

    - **Senha**: `example`

## Escolher uma plataforma de hospedagem {#choose_a_hosting_platform}

Agora que você sabe criar chaves de acesso dinâmicas, é importante
escolher uma plataforma de hospedagem adequada para sua configuração de chaves de acesso. Ao decidir,
considere fatores como confiabilidade,
segurança, facilidade de uso e resistência à censura da plataforma. A plataforma fornece suas informações de chave de acesso
de forma consistente sem inatividade? Ela oferece medidas de segurança
adequadas para proteger sua configuração? É fácil gerenciar suas
informações de chaves de acesso na plataforma? A plataforma é acessível em regiões
onde a Internet sofre censura?

Para situações em que o acesso à informação pode ser restrito, considere hospedar em plataformas resistentes à censura, como [Google Drive](https://drive.google.com),
[pad.riseup.net](https://pad.riseup.net/), [Amazon
S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html)
(com acesso no estilo de caminho),
[Netlify](https://dev.to/alexmercedcoder/delivering-json-data-with-netlify-1j96)
ou [gists secretos
do GitHub](https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists/creating-gists) (alguns links em inglês).
Avalie os requisitos da sua implantação e escolha uma plataforma alinhada
aos seus critérios de acessibilidade e segurança.
