# Fuentes oficiales y automatización

## DOF
Fuente oficial de datos abiertos: https://sidof.segob.gob.mx/datos_abiertos

La página oficial anuncia servicios web para:
- consultar el diario por fecha, año y edición;
- obtener documentos del diario;
- consultar notas e indicadores;
- obtener respuestas JSON.

Antes de activar la ejecución programada hay que validar los endpoints concretos, parámetros, esquema de respuesta y enlace canónico de cada publicación. La página de documentación pública consultada no expone esos detalles en el HTML visible, por lo que no se deben inventar rutas ni parámetros.

## SJF
Buscador oficial: https://sjf2.scjn.gob.mx/busqueda-principal-tesis
Servicio web oficial anunciado: https://sjf.scjn.gob.mx/sjfsem/Servicios/Semanario.asmx
El servicio anuncia, entre otras, las operaciones `ObtenerTesisSemana`, `ObtenerSemanas` y `ObtenerEjecutoriasSemana`.

El endpoint bloqueó la inspección automatizada de su WSDL durante la preparación inicial. Falta confirmar la firma SOAP, parámetros de semana/año, esquema de respuesta y URL oficial de detalle de cada tesis. No se deben inventar registros ni enlaces.

## Horarios previstos
GitHub Actions utiliza UTC:
- DOF: lunes a viernes, cron previsto 16:00 UTC (horario matutino de Tijuana; puede variar una hora por horario estacional).
- SJF: viernes, cron previsto 20:30 UTC. Este horario queda después de las 12:00 en Tijuana tanto en horario estándar como de verano.

GitHub puede retrasar ejecuciones programadas; no es un reloj garantizado.

## Regla de integridad
Un arreglo vacío en `data/radar.json` no significa que se verificó que no hubo novedades. El panel solo debe mostrar “Sin publicaciones/criterios relevantes” cuando exista una consulta exitosa y documentada del periodo. Si falla una fuente, debe indicarse que la consulta está pendiente o falló.

## Estado
Se añadieron los workflows con ejecución manual y los horarios previstos comentados. No se activa el cron hasta verificar los contratos oficiales y probar el proceso de punta a punta.
