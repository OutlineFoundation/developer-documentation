---
title: "Add Outline SDK to Your Go Code"
sidebar_label: "Go Integration"
---

En esta guía se explica el proceso para configurar el entorno de Go y usar el SDK de Outline en tu código de Go.

Vamos a compilar una aplicación de ejemplo llamada `splitfetch` que muestre una función del SDK. Esta aplicación obtiene una página web, pero, en lugar de enviar la solicitud en un solo paquete de red, **usa el SDK de Outline para dividir el flujo de TCP inicial en dos paquetes independientes**. Esta opción puede resultar útil para sortear algunas formas de intervención en la red.

La aplicación se podrá ejecutar en **Linux, Mac y Windows**.
Si quieres integrar el SDK con aplicaciones móviles, consulta [Añadir el SDK de Outline a tu aplicación móvil](mobile-app-integration).

## Paso 1: Configurar Go

En primer lugar, necesitas el [Lenguaje de programación Go](https://go.dev/).
Si ya tienes instalada la versión 1.21 de Go o una posterior, ve al paso siguiente.

Para instalarlo, sigue la [guía oficial](https://go.dev/doc/install). Si usas un gestor de paquetes:

### Linux

Sigue los pasos que se explican en [Go Wiki: Ubuntu](https://go.dev/wiki/Ubuntu).

### Mac

### Windows

Cuando termines, comprueba si Go se ha instalado correctamente. Para ello, ejecuta el siguiente comando en un terminal:

## Paso 2: Crear la aplicación `splitfetch`

Vamos a configurar el proyecto `splitfetch`. Primero, crea el directorio del proyecto e inicializa un módulo de Go:

A continuación, añade el SDK de Outline y crea tu archivo `main.go`:

## Paso 3: Usar el SDK de Outline en la aplicación

Abre el archivo `main.go` en el editor de código que prefieras y pega en él el siguiente código. Este código incluye toda la lógica de nuestra aplicación `splitfetch`.

Después de guardar el código, ejecuta el siguiente comando en el terminal para comprobar si el archivo `go.mod` se ha actualizado correctamente.

## Paso 4: Ejecutar la aplicación

Una vez que el código esté listo, ya puedes ejecutar la aplicación `splitfetch`.

Desde el directorio `splitfetch`, ejecuta el siguiente comando en el terminal y envía una URL como argumento:

Así se compila y se ejecuta la aplicación, que muestra el contenido HTML de la página web.

Si quieres crear y distribuir un programa independiente que puedas ejecutar sin `go`, usa el comando `go build`:

### Linux y Mac

### Windows

Una vez terminada la compilación, ya puedes distribuir y ejecutar la aplicación.
Por ejemplo:
