---
title: "Share Management Access"
sidebar_label: "Share Management Access"
---

A medida que amplíes tu servicio de Outline, quizá tengas que delegar tareas de gestión en otras personas de confianza. En esta página se describen los diversos métodos que hay para compartir el acceso de gestión con otros administradores.

El procedimiento adecuado depende de cómo hayas implementado tu servidor de Outline inicialmente.

## Implementaciones de proveedores de servicios en la nube

Si implementas el servidor de Outline en plataformas en la nube, como DigitalOcean, AWS o Google Cloud, el acceso de gestión se suele administrar con las funciones de gestión de identidades y accesos del proveedor, ya que es un método más seguro y controlado que compartir la configuración manualmente.

### DigitalOcean

La función avanzada **Teams** de DigitalOcean te permite invitar a otros usuarios de DigitalOcean a colaborar en tus proyectos. Este es el método recomendado para conceder acceso de gestión a tu servidor de Outline si lo alojas en su plataforma.

#### 1. Concede acceso a tu equipo

La manera más eficaz de compartir la gestión de un servidor de Outline alojado en DigitalOcean es usar su función **Teams**.

- Inicia sesión en tu cuenta de DigitalOcean.

- Ve a la sección **Teams** (Equipos).

- Crea un equipo si aún no lo has hecho o invita a usuarios de DigitalOcean a que se incorporen a tu equipo.

- Cuando invitas a miembros, puedes asignarles roles concretos y concederles acceso a determinados recursos, como los Droplets que ejecutan Outline.

#### 2. Controla los permisos

Ten cuidado con los permisos que concedes a los miembros del equipo. Si quieres que gestionen el servidor de Outline, puedes concederles acceso de lectura y escritura al Droplet en cuestión para que puedan hacer lo siguiente:

- Ver los detalles del Droplet (dirección IP, estado, etc.).

- Acceder a la consola del Droplet (si es necesario para solucionar problemas).

- Realizar ciertas acciones, como reiniciar el Droplet, en función de los permisos concedidos.

Los usuarios que conecten Administrador de Outline a su cuenta de DigitalOcean podrán ver y gestionar todos los servidores de Outline vinculados con esa cuenta.

## Instalaciones manuales

Si has instalado Outline manualmente en tu propio servidor con la [secuencia de comandos de instalación](../getting-started/server-setup-advanced), el método principal para conceder acceso de gestión es compartir la **configuración de acceso**.

La aplicación Administrador de Outline necesita una cadena de configuración específica para conectarse al servidor de Outline y gestionarlo. Esa cadena incluye toda la información obligatoria, como la dirección del servidor, el puerto y una clave secreta de autenticación.

### 1. Busca el archivo `access.txt`

En el servidor donde hayas instalado Outline, ve al directorio Outline. La ubicación exacta puede variar ligeramente en función del método de instalación, pero estas son algunas de las más habituales:

- `/opt/outline/access.txt`

- `/etc/outline/access.txt`

- Dentro del volumen de Docker que usa el contenedor del servidor de Outline

### 2. Obtén la configuración del acceso

Cuando encuentres el archivo `access.txt`, conviértelo a JSON, que es el formato que espera Administrador de Outline en el paso siguiente.

La salida incluirá la huella digital de certificado autofirmada (`certSha256`) y el endpoint de la API de gestión del servidor (`apiUrl`):

### 3. Comparte la configuración del acceso de forma segura

Copia la salida y compártela con el nuevo administrador de Outline mediante un procedimiento seguro. Intenta no enviarla por canales que no estén cifrados, como el correo normal o una aplicación de mensajería instantánea.
Te recomendamos que uses una función para compartir de forma segura del Gestor de contraseñas u otro método de comunicación cifrado.

En cuanto el nuevo administrador pegue la **configuración de acceso** proporcionada en Administrador de Outline, podrá añadir y gestionar el servidor de Outline en la interfaz de la aplicación. Si necesitas más ayuda para usar Administrador de Outline, visita el [Centro de Ayuda de Outline](https://support.google.com/outline).
