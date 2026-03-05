---
title: "Configure Access Keys"
sidebar_label: "Configure Access Keys"
---

O Outline usa uma configuração baseada em YAML para definir parâmetros de VPN e gerenciar
o tráfego TCP/UDP. A configuração oferece suporte à composição em vários níveis,
permitindo configurações flexíveis e extensíveis.

A configuração de nível superior especifica uma
[TunnelConfig](../reference/access-key-config#tunnelconfig).

## Exemplos

Uma configuração típica do Shadowsocks será semelhante a esta:

Observe como agora podemos ter TCP e UDP em execução em diferentes portas ou endpoints e
com diferentes prefixos.

Você pode usar âncoras YAML e a chave de mesclagem `<<` para evitar duplicação:

Agora é possível compor estratégias e fazer vários saltos:

Em caso de bloqueio de protocolos look-like-nothing como o Shadowsocks, você pode
usar o Shadowsocks sobre Websockets. Confira o [exemplo de
configuração do servidor](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml) (em inglês)
para saber como implantá-lo. Uma configuração de cliente será semelhante a:

Observe que o endpoint do Websocket pode, por sua vez, tomar um endpoint, que pode ser
aproveitado para ignorar o bloqueio baseado em DNS:

Para garantir a compatibilidade entre diferentes versões do app cliente do Outline, use a
opção `first-supported` na sua configuração. Isso é particularmente importante
à medida que novas estratégias e recursos são adicionados ao Outline, porque nem todos os usuários podem ter
atualizado para o software cliente mais recente. Ao usar o `first-supported`, você pode
fornecer uma configuração única que funciona em várias plataformas
e versões de cliente, garantindo compatibilidade com versões anteriores e uma experiência
de usuário consistente.
