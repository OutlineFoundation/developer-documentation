---
title: "Add Outline SDK to Your Go Code"
sidebar_label: "Go Integration"
---

Este guia orienta todo o processo de configuração do ambiente Go e
uso do SDK Outline no seu código Go.

Vamos criar um aplicativo de exemplo, chamado `splitfetch`, que demonstra o
recurso do SDK. Esse aplicativo busca uma página da Web, mas em vez de enviar
a solicitação em um único pacote de rede, **ele usa o SDK Outline para dividir o
stream inicial do TCP em dois pacotes separados**. Isso pode ajudar a ignorar algumas formas
de intervenção na rede.

O aplicativo poderá ser executado no **Linux, Mac e Windows**.
Para integração com dispositivos móveis, confira [Adicionar o SDK Outline ao seu app para dispositivos móveis](mobile-app-integration).

## Etapa 1: configurar o Go

Primeiro você vai precisar da [Linguagem de programação Go](https://go.dev/) (em inglês).
Se você já tem o Go (versão 1.21 ou mais recente) instalado, pule para a
próxima etapa.

Para a instalação, você pode seguir o [guia oficial](https://go.dev/doc/install) (em inglês);
ou, se você usa o gerenciador de pacotes:

### Linux

Siga as etapas em [Wiki Go: Ubuntu](https://go.dev/wiki/Ubuntu) (em inglês).

### Mac

### Windows

Quando o Go estiver instalado, você poderá confirmar que a instalação foi bem-sucedida executando
o comando a seguir em um terminal:

## Etapa 2: criar o aplicativo `splitfetch`

Vamos configurar o projeto `splitfetch`. Primeiro crie o diretório do projeto e
inicialize um módulo Go:

A seguir, adicione as dependências do SDK Outline e crie o arquivo `main.go`:

## Etapa 3: usar o SDK Outline no aplicativo

Abra o arquivo `main.go` no seu editor de código favorito e cole
o código a seguir. Esse código contém toda a lógica do nosso aplicativo `splitfetch`.

Depois de salvar o código, execute o comando a seguir no seu terminal para se certificar que
o arquivo `go.mod` seja atualizado corretamente.

## Etapa 4: executar o aplicativo

Com o código pronto, você pode executar o aplicativo `splitfetch`.

De dentro do diretório `splitfetch`, execute o comando a seguir no seu
terminal, passando um URL como um argumento:

Isso compila e executa o aplicativo, exibindo o conteúdo HTML da página da web.

Se quiser criar e distribuir um programa independente que possa ser executado
sem `go`, use o comando `go build`:

### Linux e Mac

### Windows

Quando o build estiver pronto, você poderá distribuir e executar seu aplicativo.
Por exemplo:
