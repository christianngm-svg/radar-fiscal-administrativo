# Radar Fiscal Administrativo — GMD Abogados

Panel privado de seguimiento de publicaciones del DOF y criterios del Semanario Judicial de la Federación.

## Estructura
- `index.html`: interfaz del radar (dos secciones: DOF y SJF).
- `data/radar.json`: datos que consume el panel.
- `.github/workflows/`: automatizaciones programadas (por implementar).

## Criterios editoriales
- DOF: revisar publicaciones de días hábiles y registrar solo disposiciones con relevancia fiscal o administrativa.
- SJF: revisar individualmente los nuevos criterios publicados; corte semanal los viernes después de las 12:00, hora de Tijuana.
- Cada registro debe incluir encabezado original, síntesis práctica y enlace a la fuente oficial.
- No crear registros si no existe evidencia verificable. Un arreglo vacío significa que todavía no se ha procesado el corte; no equivale a un resultado confirmado de cero publicaciones.

## Privacidad y despliegue
Este repositorio es privado. No activar GitHub Pages ni publicar el panel en un hosting público sin implementar antes autenticación. El repositorio privado por sí solo no convierte una página desplegada en privada.

## Estado
- Interfaz inicial y estructura de datos creadas.
- Workflows de DOF y SJF añadidos con ejecución manual de validación; cron intencionalmente desactivado hasta verificar los contratos de los servicios oficiales.
- Documentación de fuentes y despliegue privado añadida en `docs/`.
- La recolección, revisión sustantiva, generación de síntesis y actualización automática aún no están activas.
- La publicación privada requiere conectar Cloudflare Pages y proteger el hostname con Cloudflare Access.