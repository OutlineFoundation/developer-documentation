---
title: "Share Management Access"
sidebar_label: "Share Management Access"
---

Conforme seu serviço do Outline cresce, você pode achar necessário delegar
responsabilidades de gestão para outras pessoas de confiança. Este documento descreve
os vários métodos disponíveis para fazer isso.

O método escolhido varia dependendo de como seu servidor
do Outline foi implantado inicialmente.

## Implantações do provedor de nuvem

Para servidores do Outline implantados em plataformas de nuvem, como DigitalOcean, AWS ou
Google Cloud, o acesso de gerenciamento normalmente acontece por meio dos recursos de
gerenciamento de identidade e acesso (IAM) integrados do provedor. Essa abordagem é mais
segura e controlada em comparação com o compartilhamento manual de configurações.

### DigitalOcean

O DigitalOcean oferece um recurso **Teams** robusto, que permite convidar outros
usuários do DigitalOcean para colaborar nos seus projetos. Essa é a maneira recomendada
de conceder acesso de gerenciamento ao seu servidor do Outline hospedado na plataforma.

#### 1. Conceder acesso à equipe

A maneira mais eficaz de compartilhar o gerenciamento do seu servidor do Outline hospedado no
DigitalOcean é com o recurso **Teams**.

- Faça login na sua conta do DigitalOcean.

- Vá para a seção **Teams**.

- Crie uma nova equipe (se ainda não fez isso) ou convide usuários do DigitalOcean para sua equipe.

- Ao convidar membros, você pode atribuir papéis específicos a eles ou conceder
acesso a recursos específicos, incluindo seus droplets que executam o Outline.

#### 2. Controlar permissões

Pense com cuidado nas permissões que você concederá aos membros da equipe. Para gerenciar o
servidor do Outline, você pode conceder a eles acesso de "Leitura" e "Gravação" a um droplet
específico. Assim eles poderão:

- Ver os detalhes do droplet (endereço IP, status etc.).

- Acessar o console do droplet (se necessário para solução de problemas).

- Realizar ações como reiniciar o droplet (dependendo das
permissões concedidas).

Os usuários com o Outline Manager conectado à conta do DigitalOcean agora podem
ver e gerenciar todos os servidores do Outline vinculados a essa conta.

## Instalações manuais

Para quem instalou o Outline manualmente nos servidores usando o
[script de instalação](../getting-started/server-setup-advanced), a principal maneira de conceder
acesso de gerenciamento é compartilhando a **configuração de acesso**.

O aplicativo Outline Manager precisa de uma string de configuração específica para se conectar
e gerenciar um servidor do Outline. Essa string de configuração contém todas as
informações necessárias, incluindo o endereço do servidor, porta e chave secreta para
autenticação.

### 1. Localizar o arquivo `access.txt`

No servidor em que o Outline foi instalado, vá até o diretório do Outline. A
localização exata pode variar um pouco dependendo do método de instalação, mas
alguns locais comuns são:

- `/opt/outline/access.txt`

- `/etc/outline/access.txt`

- Dentro do volume do Docker usado pelo contêiner do servidor do Outline

### 2. Recuperar a configuração de acesso

Depois de encontrar o arquivo `access.txt`, converta-o para JSON, que é o formato
esperado pelo Outline Manager na próxima etapa.

O arquivo resultante conterá a impressão digital do certificado autoassinado (`certSha256`)
e o endpoint da API Management no servidor (`apiUrl`):

### 3. Compartilhar a configuração de acesso de forma segura

Copie o arquivo resultante e o compartilhe de forma segura com o novo gerente do Outline. Evite
enviá-lo usando canais não criptografados, como e-mail comum ou mensagens instantâneas.
Use o compartilhamento seguro de um gerenciador de senhas ou outro método
de comunicação criptografado.

Ao colar a **configuração de acesso** fornecida no Outline Manager, o novo
gerente poderá adicionar e depois gerenciar o servidor do Outline pela
interface do aplicativo. Para mais ajuda sobre como usar o Outline Manager,
visite a [Central de Ajuda do Outline](https://support.google.com/outline).
