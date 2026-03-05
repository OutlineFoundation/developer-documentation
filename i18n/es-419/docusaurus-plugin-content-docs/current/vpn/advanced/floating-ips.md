---
title: "Use a Domain Name with Floating IPs"
sidebar_label: "Domain with Floating IPs"
---

## Introducción

A veces, los servidores de Outline, pueden enfrentar el problema de que se descubran en redes altamente
censuradas y se bloqueen de ellas. Es posible (y sencillo) recuperar un
servidor bloqueado si se configuró correctamente. Para ello, usaremos un DNS, la
tecnología de Internet que traduce los nombres de dominios (como `getoutline.org`) a
direcciones IP físicas (como `216.239.36.21`), y también IPs flotantes, una función de la nube
que te permite asignar más de una dirección IP como un servidor de Outline.

## Requisitos

Se requiere un nivel mínimo de habilidades técnicas para seguir los pasos en esta guía. También es recomendable (aunque no necesario)
tener conocimientos básicos sobre DNS. Revisa la guía de
[MDN](https://developer.mozilla.org/docs/Learn/Common_questions/What_is_a_domain_name)
sobre nombres de dominios para consultar una introducción.

Para tener un ejemplo concreto, usaremos DigitalOcean y Google Domains, pero servirá cualquier
proveedor de servicios en la nube que permita la
asignación de direcciones IP (p. ej., Google Cloud o
[AWS Lightsail](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/lightsail-create-static-ip))
y cualquier registrador de nombres (p. ej.,
[AWS Route 53](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-using-route-53-to-point-a-domain-to-an-instance)).

## Instrucciones

1. 

En la siguiente lista, se resumen los pasos para rotar las direcciones IP de un servidor:

2. 

Compra un nombre de dominio.

3. 

Dirige el nombre del dominio a la dirección IP de nuestro servidor.

4. 

Proporciona claves de acceso usando ese nombre.

5. 

Asigna una IP flotante al Droplet del servidor.

6. 

Cambia el nombre de dominio para que dirija a la nueva dirección IP.

## Crea un servidor de Outline en DigitalOcean

Si tienes un servidor de DigitalOcean en ejecución, avanza al próximo paso.

1. 

Abre Outline Manager y haz clic en "+" en la parte inferior izquierda para ingresar a la pantalla
de creación del servidor.

2. 

Haz clic en "Crear servidor" en el botón "DigitalOcean" y sigue las instrucciones
de la app.

![Crear servidor](/images/create-DO-server.png)

## Crea un nombre de host para tu servidor

1. 

Navega a [Google Domains](https://domains.google.com/m/registrar/) y
haz clic en "Buscar el dominio perfecto".

2. 

Ingresa un nombre de dominio en la barra de búsqueda y elige un nombre. Usamos
`outlinedemo.info` como ejemplo.

3. 

Navega a la pestaña DNS en Google Domains. En "Registros de recursos personalizados",
escribe la dirección IP de tu servidor en el campo marcado "Dirección IPV4".

4. 

Navega a la pestaña "Configuración" de tu servidor en Outline Manager. En
"Nombre de host", escribe el nombre que compraste y haz clic en "GUARDAR". Esto hará
que todas las claves de acceso futuras usen este nombre de host en lugar de la dirección IP del servidor.

![Configura el nombre de host](/images/set-hostname.png)

## Cambia la dirección IP del servidor

1. 

Navega a tu servidor en la página "Droplets" de DigitalOcean.

2. 

Haz clic en "Enable Now" en la esquina superior derecha de la ventana junto a "Floating IP".

![Habilita la IP flotante](/images/floating-ip-DO.png)

1. Busca tu servidor en la lista de Droplets y haz clic en "Assign Floating IP".

![Asigna una IP flotante](/images/assign-floating-ip-DO.png)

1. 

Regresa a la pestaña DNS en Google Domains.

2. 

Cambia la dirección IP como antes, pero esta vez con la nueva dirección IP
flotante. Este proceso puede tardar hasta 48 horas en realizarse, pero, a menudo, solo toma unos minutos.

3. 

Navega a la [herramienta del DNS en línea de Google](https://toolbox.googleapps.com/apps/dig/#A/)
y, allí, ingresa tu nombre de dominio para ver cuándo se realizó el cambio en el último
paso.

![Busca tu dominio en la herramienta del DNS de Google](/images/google-dns.png)

Una vez que se propague este cambio, los clientes se conectarán a la nueva dirección IP. Puedes
conectar tu servidor con una clave nueva y abrir <https://ipinfo.io> para garantizar
que ves la nueva dirección IP de tu servidor.

Conclusión
Rotar las direcciones IP de un servidor de Outline puede ser una manera rápida de desbloquear un servidor
y restablecer el servicio para los clientes. Para realizar más preguntas, no dudes en comentar en la
[publicación de anuncios](https://redd.it/hrbhz4), visitar
[la página de asistencia de Outline](https://support.getoutline.org/) o
[comunicarte con nosotros directamente.](https://support.getoutline.org/s/contactsupport).
