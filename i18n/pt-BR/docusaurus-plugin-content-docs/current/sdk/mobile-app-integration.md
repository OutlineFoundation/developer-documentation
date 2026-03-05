---
title: "Add Outline SDK to Your Mobile App"
sidebar_label: "Mobile App Integration"
---

Este documento resume como integrar o SDK Outline aos seus aplicativos
para dispositivos móveis, com foco na biblioteca `MobileProxy` para gerenciamento simplificado de proxies
locais.

`MobileProxy` é uma biblioteca com base no Go, criada para simplificar a integração de funcionalidades de proxy a apps para dispositivos móveis. Ela usa o [Go
Mobile](https://go.dev/wiki/Mobile) (em inglês) para gerar bibliotecas para dispositivos móveis. Dessa forma, você
pode configurar as bibliotecas de rede do seu aplicativo para encaminhar o tráfego por um proxy
local.

**App sem MobileProxy**

![App de conteúdo sem MobileProxy](/images/mobileproxy-before.png)

**App com MobileProxy**

![App de conteúdo com MobileProxy](/images/mobileproxy-after.png)

## Etapa 1: como criar bibliotecas para dispositivos móveis com MobileProxy

Use o [gomobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile) (em inglês) para compilar
o código Go em bibliotecas para Android e iOS.

1. 

Clone o repositório do SDK Outline:

2. 

Crie os binários do Go Mobile com [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies) (em inglês):

#### Adicionar suporte do Psiphon

Você pode adicionar suporte para usar a rede do [Psiphon](https://psiphon.ca/) (em inglês)
seguindo estas etapas extras:

    - Entre em contato com a equipe do Psiphon para obter uma configuração que dê acesso à
rede deles. Isso pode requerer um contrato.

    - Adicione a configuração do Psiphon que você recebeu à seção `fallback` da sua
configuração `SmartDialer`.

    - 

Crie a MobileProxy usando o sinalizador `-tags psiphon`:

O sinalizador `-tags psiphon` é obrigatório, porque a base de código Psiphon é
licenciada sob o GPL, que pode impor restrições de licença ao seu próprio
código. Pode ser uma boa ideia adquirir uma licença especial com eles.

3. 

Gere bibliotecas para dispositivos móveis e adicione-as ao seu projeto:

### Android

No Android Studio, selecione **File > Import Project…** para importar o pacote `out/mobileproxy.aar` gerado. Se quiser mais ajuda, confira [Como criar e implantar no Android](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1) (em inglês) em Go Mobile.

### iOS

Arraste o pacote `out/mobileproxy.xcframework` para o projeto Xcode. Se
quiser mais ajuda, confira [Como criar e implantar no iOS](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1) (em inglês) em Go
Mobile.

## Etapa 2: executar a MobileProxy

Abra o app e inicie o proxy local `MobileProxy` dentro do tempo de execução do seu app.
Você pode usar uma configuração de transporte estática ou o Proxy Inteligente para a
seleção dinâmica de estratégias.

- 

**Configuração de transporte estática**: use a função `RunProxy` com uma configuração
de transporte e endereço local.

### Android

### iOS

- 

**Proxy Inteligente**: o Proxy Inteligente seleciona dinamicamente estratégias de DNS e TLS
com base em domínios de teste especificados. Você precisa especificar a estratégia
de configuração no formato YAML
([exemplo](https://github.com/Jigsaw-Code/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml), em inglês).

### Android

### iOS

## Etapa 3: configurar as bibliotecas de rede e clientes HTTP

Configure suas bibliotecas de rede para usar a porta e endereço do proxy local.

### Dart/Flutter HttpClient

Defina o proxy com
[`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html) (em inglês).

### OkHttp (Android)

Defina o proxy com
[`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/) (em inglês).

### JVM (Java, Kotlin)

Configure o proxy para usar com [propriedades
do sistema](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html) (em inglês):

### WebView do Android

Aplique uma configuração de proxy para todas as visualizações da Web no seu aplicativo com
a biblioteca
[`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController):

### WebView do iOS

Desde o iOS 17, é possível adicionar uma configuração de proxy a um `WKWebView` usando a
[propriedade
`WKWebsiteDataStore`](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration) (em inglês):

## Avançado: gere uma biblioteca para dispositivos móveis personalizada

Para casos de uso avançados, você pode gerar suas próprias bibliotecas para dispositivos móveis:

1. **Criar uma biblioteca Go**: desenvolva um pacote Go reunindo as funcionalidades do SDK
necessárias.

2. **Gerar bibliotecas para dispositivos móveis**: use `gomobile bind` para produzir ARchives do
Android (AAR) e Apple Frameworks. Exemplos (em inglês):

    - [ARchive do Android do Outline](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [Apple Framework do Outline](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **Integrar ao seu app**: adicione a biblioteca gerada ao seu aplicativo para dispositivos
móveis.
