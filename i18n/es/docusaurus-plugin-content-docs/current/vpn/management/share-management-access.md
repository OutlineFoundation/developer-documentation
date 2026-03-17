---
title: "Compartir el acceso de gestión con otros usuarios"
sidebar_label: "Compartir el acceso de gestión con otros usuarios"
---

A medida que amplíes tu servicio de Outline, quizá tengas que delegar tareas de gestión en otras personas de confianza. En esta página se describen los diversos métodos que hay para compartir el acceso de gestión con otros administradores.

El procedimiento adecuado depende de cómo hayas implementado tu servidor de Outline inicialmente.

## Implementaciones de proveedores de servicios en la nube {#cloud_provider_deployments}

Si implementas el servidor de Outline en plataformas en la nube, como DigitalOcean, AWS o Google Cloud, el acceso de gestión se suele administrar con las funciones de gestión de identidades y accesos del proveedor, ya que es un método más seguro y controlado que compartir la configuración manualmente.

### DigitalOcean {#digitalocean}

La función avanzada **Teams** de DigitalOcean te permite invitar a otros usuarios de DigitalOcean a colaborar en tus proyectos. Este es el método recomendado para conceder acceso de gestión a tu servidor de Outline si lo alojas en su plataforma.

#### 1. Concede acceso a tu equipo {#1_grant_team_access}

La manera más eficaz de compartir la gestión de un servidor de Outline alojado en DigitalOcean es usar su función **Teams**.

- Inicia sesión en tu cuenta de DigitalOcean.

- Ve a la sección **Teams** (Equipos).

- Crea un equipo si aún no lo has hecho o invita a usuarios de DigitalOcean a que se incorporen a tu equipo.

- Cuando invitas a miembros, puedes asignarles roles concretos y concederles acceso a determinados recursos, como los Droplets que ejecutan Outline.

#### 2. Controla los permisos {#2_control_permissions}

Ten cuidado con los permisos que concedes a los miembros del equipo. Si quieres que gestionen el servidor de Outline, puedes concederles acceso de lectura y escritura al Droplet en cuestión para que puedan hacer lo siguiente:

- Ver los detalles del Droplet (dirección IP, estado, etc.).

- Acceder a la consola del Droplet (si es necesario para solucionar problemas).

- Realizar ciertas acciones, como reiniciar el Droplet, en función de los permisos concedidos.

Los usuarios que conecten Administrador de Outline a su cuenta de DigitalOcean podrán ver y gestionar todos los servidores de Outline vinculados con esa cuenta.


:::tip
Recomienda a los nuevos administradores que habiliten la autenticación multifactor (MFA) en sus cuentas del proveedor de servicios en la nube para reforzar la seguridad.
:::

## Instalaciones manuales {#manual_installations}


:::caution
Si se comparte el acceso de gestión con instalaciones manuales, resulta difícil revocarlo. El método más directo es reinstalar de nuevo el servidor, lo que genera una configuración nueva, aunque también borra todas las claves de acceso.
:::

Si has instalado Outline manualmente en tu propio servidor con la [secuencia de comandos de instalación](../getting-started/server-setup-advanced), el método principal para conceder acceso de gestión es compartir la **configuración de acceso**.

La aplicación Administrador de Outline necesita una cadena de configuración específica para conectarse al servidor de Outline y gestionarlo. Esa cadena incluye toda la información obligatoria, como la dirección del servidor, el puerto y una clave secreta de autenticación.

### 1. Busca el archivo `access.txt` {#1_locate_the_accesstxt_file}

En el servidor donde hayas instalado Outline, ve al directorio Outline. La ubicación exacta puede variar ligeramente en función del método de instalación, pero estas son algunas de las más habituales:

- `/opt/outline/access.txt`

- `/etc/outline/access.txt`

- Dentro del volumen de Docker que usa el contenedor del servidor de Outline

### 2. Obtén la configuración del acceso {#2_retrieve_the_access_config}

Cuando encuentres el archivo `access.txt`, conviértelo a JSON, que es el formato que espera Administrador de Outline en el paso siguiente.

```sh
sed -n '2s/^apiUrl://p; 1s/^certSha256://p' /opt/outline/access.txt | paste -d'\n' -s | sed 'H;1h;$!d;x;s/\n/", \"apiUrl\": \"/g; s/^/{"certSha256": \"/; s/$/\"}/'
```

La salida incluirá la huella digital de certificado autofirmada (`certSha256`) y el endpoint de la API de gestión del servidor (`apiUrl`):

```json
{"certSha256": "1DCC18CC9F6C34EBBB639255F4D1BC6984C2F6A47B15F7A49AA8AFB69B7E4DDE", "apiUrl": "https://1.1.1.1:12345/Fw-CkWFNSN7Ml8LLM8Pduw"}
```


:::warning[Important]
Esta línea incluye información sensible. Compártela únicamente con personas de confianza que necesiten acceso de gestión.
:::

### 3. Comparte la configuración del acceso de forma segura {#3_share_the_access_config_securely}

Copia la salida y compártela con el nuevo administrador de Outline mediante un procedimiento seguro. Intenta no enviarla por canales que no estén cifrados, como el correo normal o una aplicación de mensajería instantánea.
Te recomendamos que uses una función para compartir de forma segura del Gestor de contraseñas u otro método de comunicación cifrado.

En cuanto el nuevo administrador pegue la **configuración de acceso** proporcionada en Administrador de Outline, podrá añadir y gestionar el servidor de Outline en la interfaz de la aplicación. Si necesitas más ayuda para usar Administrador de Outline, visita el [Centro de Ayuda de Outline](https://support.google.com/outline).
