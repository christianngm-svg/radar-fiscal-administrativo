# Publicación privada

## Arquitectura prevista
- Repositorio GitHub privado como fuente de código y datos.
- Cloudflare Pages conectado al repositorio para despliegue.
- Cloudflare Access delante del dominio del panel, con una política que permita únicamente el correo autorizado.

Documentación:
- Git integration: https://developers.cloudflare.com/pages/configuration/git-integration/
- Cloudflare Access: https://developers.cloudflare.com/cloudflare-one/applications/configure-apps/

## Importante
No activar GitHub Pages. Un repositorio privado no vuelve privada una URL publicada. Tampoco debe guardarse información confidencial en el frontend ni en variables visibles al navegador.

## Configuración que requiere al titular de la cuenta
1. Iniciar sesión/crear cuenta en Cloudflare.
2. Autorizar la integración de Cloudflare con GitHub y seleccionar solo `christianngm-svg/radar-fiscal-administrativo`.
3. Crear un proyecto Pages desde el repositorio, rama `main`, directorio raíz `/`.
4. Configurar Cloudflare Access para proteger el hostname y permitir únicamente el correo electrónico del titular.
5. Probar la URL en una ventana privada: sin sesión debe bloquearse; con el correo autorizado debe permitir el acceso.

La conexión a Cloudflare y la política de acceso no pueden completarse desde el conector GitHub; requieren autorización en la cuenta Cloudflare del titular.
