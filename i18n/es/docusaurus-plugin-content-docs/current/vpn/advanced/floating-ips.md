---
title: "Configura un servidor resistente a los bloqueos con IPs flotantes"
sidebar_label: "Configura un servidor resistente a los bloqueos con IPs flotantes"
---

## Introducción {#introduction}

A veces, los servidores de Outline son descubiertos y bloqueados por redes muy censuradas. Recuperar un servidor bloqueado es factible, y no muy complicado, si se ha configurado correctamente. Para ello, vamos a usar DNS, la tecnología de Internet que traduce nombres de dominio (como `getoutline.org`) a direcciones IP físicas (como `216.239.36.21`), e IPs flotantes, una función en la nube que te permite asignar más de una dirección IP a un servidor de Outline.

## Requisitos {#requirements}

Para seguir esta guía, no se necesita un alto nivel de conocimientos técnicos. Contar con unas nociones básicas sobre DNS es útil, pero no obligatorio. Consulta una introducción en la guía de [MDN](https://developer.mozilla.org/docs/Learn/Common_questions/What_is_a_domain_name) sobre nombres de dominio.

En este ejemplo, vamos a usar DigitalOcean y Google Domains, pero también sirve cualquier otro proveedor de servicios en la nube que permita las direcciones IP (por ejemplo, Google Cloud o [AWS Lightsail](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/lightsail-create-static-ip)) y cualquier registrador de dominios (por ejemplo, [AWS Route 53](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-using-route-53-to-point-a-domain-to-an-instance)).

## Instrucciones {#instructions}

1. La siguiente lista resume los pasos para rotar la dirección IP de un servidor:

2. Compra un nombre de dominio.

3. Dirige el nombre de dominio a la dirección IP del servidor.

4. Emite claves de acceso usando el nombre de dominio.

5. Asigna una IP flotante al Droplet del servidor.

6. Cambia el nombre de dominio para que dirija a la nueva dirección IP.

## Crear un servidor de Outline en DigitalOcean {#create_an_outline_server_on_digitalocean}

Si tienes un servidor de DigitalOcean activo, ve al siguiente paso.

1. Abre Administrador de Outline y haz clic en el símbolo "+" de la parte inferior izquierda para acceder a la pantalla de creación del servidor.

2. Haz clic en "Create Server" (Crear servidor) en la sección "DigitalOcean" y sigue las indicaciones en la aplicación.

![Crear servidor](/images/create-DO-server.png)

## Asignar un nombre de host a tu servidor {#make_a_hostname_for_your_server}

1. Ve a [Google Domains](https://domains.google.com/m/registrar/) y haz clic en "Encuentra el dominio perfecto".

2. Introduce un nombre de dominio en la barra de búsqueda y elige un nombre. En este ejemplo hemos usado `outlinedemo.info`.

3. Ve a la pestaña DNS en Google Domains. En "Registros de recursos personalizados", escribe la dirección IP de tu servidor en el campo "Dirección IPv4".

4. Ve a la pestaña "Ajustes" de tu servidor en Administrador de Outline. En "Nombre de host", escribe el nombre del que has comprado y haz clic en "GUARDAR". De esta forma, las futuras claves de acceso usarán este nombre de host en lugar de la dirección IP del servidor.

![Configurar el nombre de host](/images/set-hostname.png)

## Cambiar la dirección IP del servidor {#change_the_servers_ip_address}

1. Ve a tu servidor en la página "Droplets" de DigitalOcean.

2. Haz clic en "Enable now" (Habilitar ahora) en la parte superior derecha de la ventana situada junto a "Floating IP" (IP flotante).

![Habilitar la IP flotante](/images/floating-ip-DO.png)

1. Busca tu servidor en la lista de Droplets y haz clic en "Assign Floating IP" (Asignar IP flotante).

![Asignar la IP flotante](/images/assign-floating-ip-DO.png)

1. Vuelve a la pestaña DNS en Google Domains.

2. Cambia la dirección IP como antes, pero esta vez por la nueva dirección IP flotante. Normalmente, el cambio suele surtir efecto en unos minutos, pero puede tardar hasta 48 horas.

3. Ve a la [herramienta DNS online de Google](https://toolbox.googleapps.com/apps/dig/#A/) y escribe tu nombre de dominio para ver cuándo se efectuó el cambio del último paso.

![Buscar tu dominio en la herramienta DNS de Google](/images/google-dns.png)

Cuando se propague este cambio, los clientes se conectarán a la nueva dirección IP. Puedes conectarte a tu servidor con una clave nueva y abrir <https://ipinfo.io> para asegurarte de que ves la nueva dirección IP de tu servidor.

Conclusión
Rotar las direcciones IP de un servidor de Outline puede ser una forma rápida de desbloquearlo y restaurar el servicio de los clientes. Si tienes preguntas, puedes comentar en la [publicación del anuncio](https://redd.it/hrbhz4), visitar la [página de asistencia de Outline](https://support.getoutline.org/) o [ponerte en contacto con nosotros directamente](https://support.getoutline.org/s/contactsupport).
