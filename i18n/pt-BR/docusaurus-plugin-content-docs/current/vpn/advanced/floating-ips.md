---
title: "Configurar um servidor resistente a bloqueio com IPs flutuantes"
sidebar_label: "Configurar um servidor resistente a bloqueio com IPs flutuantes"
---

## Introdução {#introduction}

Às vezes, servidores do Outline são descobertos e bloqueados
por redes altamente censuradas. É possível e relativamente fácil recuperar
um servidor bloqueado se ele tiver sido configurado corretamente. Vamos mostrar como fazer isso usando o DNS, a
tecnologia de Internet que converte nomes de domínios (como `getoutline.org`) em
endereços IP físicos (como `216.239.36.21`). Também vamos usar IPs flutuantes, um recurso na nuvem,
para a atribuição de mais de um endereço IP a um servidor do Outline.

## Requisitos {#requirements}

Para seguir as instruções deste guia, é necessário ter um nível mínimo de habilidades técnicas. Noções
básicas sobre DNS podem ser úteis, mas não são obrigatórias. Confira a
introdução no guia [MDN](https://developer.mozilla.org/docs/Learn/Common_questions/What_is_a_domain_name)
sobre nomes de domínio.

Para vermos um exemplo concreto, vamos usar domínios da DigitalOcean e do Google, mas qualquer
provedor de nuvem que permita a atribuição de endereços IP (como Google Cloud ou
[AWS Lightsail](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/lightsail-create-static-ip))
e qualquer registrador de domínio (como
[AWS Route 53](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-using-route-53-to-point-a-domain-to-an-instance))
vai funcionar também.

## Instruções {#instructions}

1. A lista a seguir resume as etapas para fazer a rotação do endereço IP de um servidor:

2. Compre um nome de domínio.

3. Aponte o nome de domínio para o endereço IP do nosso servidor.

4. Gere chaves de acesso usando o nome de domínio.

5. Atribua um IP flutuante ao droplet do servidor.

6. Altere o nome de domínio para apontar para o novo endereço IP.

## Criar um servidor do Outline na plataforma DigitalOcean {#create_an_outline_server_on_digitalocean}

Se você já tiver um servidor da DigitalOcean, pule para a próxima etapa.

1. Abra o Outline Manager e clique no botão "+" na parte inferior esquerda da tela para entrar na tela de
criação do servidor.

2. Clique em "Criar servidor" no botão "DigitalOcean" e siga as instruções
no app.

![Criar servidor](/images/create-DO-server.png)

## Definir o nome do host para o servidor {#make_a_hostname_for_your_server}

1. Vá para [Google Domains](https://domains.google.com/m/registrar/) e
clique em "Encontre o domínio perfeito".

2. Insira o nome de domínio na barra de pesquisa e escolha um nome. Nós usamos
`outlinedemo.info` como exemplo.

3. Vá para a guia "DNS" no Google Domains. Em "Registros de recursos personalizados",
digite o endereço IP do seu servidor no campo indicado como "Endereço IPV4".

4. Vá para a guia "Configurações" do seu servidor no Outline Manager. Em "Nome do host", digite o nome que você comprou e clique em "Salvar". Com isso, todas as futuras chaves de acesso vão usar esse nome do host em vez do endereço IP do servidor.

![Definir o nome do host](/images/set-hostname.png)

## Mudar o endereço IP do servidor {#change_the_servers_ip_address}

1. Vá para seu servidor na página "Droplets" da DigitalOcean.

2. Clique em "Ativar agora" na parte superior direita da janela ao lado de "IP flutuante".

![Ativar o IP flutuante](/images/floating-ip-DO.png)

1. Encontre seu servidor na lista de droplets e clique em "Atribuir IP flutuante".

![Atribuir IP flutuante](/images/assign-floating-ip-DO.png)

1. Volte para a guia "DNS" no Google Domains.

2. Altere o endereço IP como você já fez, mas dessa vez o substitua pelo endereço IP
flutuante. A mudança pode demorar 48 horas para entrar em vigor, mas geralmente leva
poucos minutos.

3. Vá para a [ferramenta DNS on-line do Google](https://toolbox.googleapps.com/apps/dig/#A/)
e insira seu nome de domínio para ver quando a mudança foi feita na última
etapa.

![Pesquisar o domínio na ferramenta DNS do Google](/images/google-dns.png)

Quando essa mudança se propagar, os clientes vão se conectar ao novo endereço IP. Você
pode se conectar ao seu servidor com uma nova chave e abrir <https://ipinfo.io> para
confirmar que o novo endereço IP está aparecendo.

Conclusão:
a rotação de endereços IP de um servidor do Outline é uma forma rápida de desbloquear um servidor
e restaurar o serviço para os clientes. Se tiver dúvidas, você pode comentar no
[post do anúncio](https://redd.it/hrbhz4), visitar a
[página de suporte do Outline](https://support.getoutline.org/) ou
[entrar em contato direto conosco](https://support.getoutline.org/s/contactsupport).
