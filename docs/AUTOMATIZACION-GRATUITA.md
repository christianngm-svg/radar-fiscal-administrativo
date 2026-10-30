# Criterios de automatización gratuita

## DOF
El portal oficial publica documentación de consumo de WebServices y una página de estado de servicios:
- https://sidof.segob.gob.mx/datos_abiertos
- https://sidof.segob.gob.mx/apiStatus

Antes de activar la programación diaria se debe confirmar el endpoint de consulta del diario, los parámetros requeridos, la estructura JSON y el enlace oficial individual de cada documento. No se deben inferir endpoints ni fabricar enlaces.

## SJF
El Semanario Judicial publica un Web Service SOAP. Su página oficial enumera operaciones como ObtenerSemanas y ObtenerTesisSemana:
- https://sjf.scjn.gob.mx/sjfsem/Servicios/Semanario.asmx
- https://sjf.scjn.gob.mx/sjfsem/Servicios/Semanario.asmx?op=ObtenerSemanas

La operación ObtenerSemanas documenta un parámetro tipo_doc y devuelve metadatos de semanas. Antes de activar la consulta semanal se debe validar la firma exacta de ObtenerTesisSemana, su respuesta y el formato de URL individual. No se deben publicar tesis sin validar esos campos.

## Clasificación sin IA
Se utilizará un catálogo local de términos por materia en config/topics.json. La coincidencia de términos es solo un filtro de candidatos: no equivale a una conclusión jurídica ni reemplaza la lectura del texto completo. Los encabezados y resúmenes deben describir fielmente el contenido oficial y no añadir consecuencias no sustentadas.

## Integridad
- Si la consulta falla, no actualizar updated_at como si hubiera sido exitosa.
- Si el documento no tiene URL oficial verificable, excluirlo.
- Un corte con cero relevantes solo se registra cuando la fuente respondió correctamente y el universo consultado fue revisado.
- Conservar fecha y hora del corte, fuente y estado de cada consulta.
- No incluir credenciales ni datos personales en el repositorio público.
