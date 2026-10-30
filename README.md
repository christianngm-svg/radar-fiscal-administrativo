# Radar Fiscal Administrativo — GMD Abogados

Panel público de seguimiento de publicaciones del DOF y criterios del Semanario Judicial de la Federación.

## Objetivo
- DOF: revisar publicaciones de cada día hábil y seleccionar disposiciones fiscales y administrativas relevantes.
- SJF: revisar individualmente los criterios nuevos del corte semanal de los viernes después de las 12:00, hora de Tijuana.
- Cada resultado debe incluir encabezado editorial original, síntesis práctica y enlace oficial exacto.
- Solo mostrar cero confirmado cuando la consulta oficial concluya correctamente y no existan resultados relevantes.
- Si falla una fuente o no se valida su respuesta, mostrar «Consulta no disponible», nunca un cero inventado.

## Clasificación temática inicial
La selección gratuita por reglas considera materias fiscal, administrativa, seguridad social, aduanera, litigio contencioso y amparo administrativo. Incluye términos como SAT, CFF, ISR, IVA, facultades de comprobación, créditos fiscales, devoluciones, multas, TFJA, nulidad, competencia, fundamentación y motivación, responsabilidades administrativas, IMSS, INFONAVIT, cuotas, aduanas, comercio exterior, suspensión y ejecución de sentencias.

Las palabras clave son un filtro inicial, no un criterio jurídico definitivo. La relevancia requiere revisar el documento completo; los resúmenes sin IA serán extractivos y no se presentarán como análisis jurídico experto.

## Estructura
- index.html: interfaz del radar.
- data/radar.json: datos que consume el panel.
- .github/workflows/: ejecuciones programadas.
- config/topics.json: catálogo inicial de materias y términos.
- docs/: notas técnicas y criterios de integridad.

## Estado real
- Interfaz pública y estructura JSON creadas.
- Repositorio público. La publicación efectiva de GitHub Pages debe verificarse en GitHub.
- La consulta automatizada y validada al DOF y al SJF todavía no está activa.
- No hay resultados publicados porque aún no existe un corte oficial procesado.
- Los workflows no deben operar como automatización productiva hasta probar los adaptadores oficiales de extremo a extremo.

## Costos
Diseñado para utilizar GitHub Pages, GitHub Actions y fuentes oficiales públicas, sin OpenAI API, Cloudflare ni servicios de pago. El uso de GitHub Actions está sujeto a los límites gratuitos de GitHub.

## Seguridad
El repositorio y el panel son públicos por decisión del propietario. No almacenar claves, contraseñas ni datos personales aquí.
