#!/usr/bin/env python3
"""Consulta de fuentes oficiales. Falla de forma cerrada: nunca convierte errores en cero."""
import json, os, re, sys, urllib.request, urllib.error
from datetime import datetime
from zoneinfo import ZoneInfo
from xml.etree import ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "radar.json")
TZ = ZoneInfo("America/Tijuana")
TERMS = {
 "fiscal": ["SAT","Código Fiscal","contribución","impuesto","ISR","IVA","facultades de comprobación","crédito fiscal","devolución","compensación","multa","recargos","prescripción","caducidad"],
 "administrativo": ["procedimiento administrativo","juicio contencioso","TFJA","nulidad","competencia","fundamentación y motivación","responsabilidad administrativa","sanción administrativa","acto administrativo"],
 "seguridad social y aduanas": ["IMSS","INFONAVIT","cuotas obrero patronales","seguridad social","aduana","comercio exterior","pedimento","arancel"],
 "litigio y amparo": ["amparo","suspensión","recurso de revocación","ejecución de sentencia","cumplimiento de sentencia","interés jurídico","interés legítimo"]
}

def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent":"RadarFiscalAdministrativo/1.0 contact: public repository", **(headers or {})})
    with urllib.request.urlopen(req, timeout=35) as r:
        if r.status != 200: raise RuntimeError(f"HTTP {r.status}: {url}")
        return r.read()

def norm(s):
    return re.sub(r"\\s+", " ", str(s or "")).strip()

def find_terms(text):
    low = text.casefold()
    return [name for name, words in TERMS.items() if any(w.casefold() in low for w in words)]

def main():
    now = datetime.now(TZ)
    date = now.strftime("%d-%m-%Y")
    status = {"dof":"pending","sjf":"pending"}
    errors = []
    # Endpoint documentado en el monitor oficial del SIDOF: /diarios/porFecha/DD-MM-AAAA.
    try:
        raw = get(f"https://sidof.segob.gob.mx/diarios/porFecha/{date}", {"Accept":"application/json"})
        payload = json.loads(raw.decode("utf-8-sig"))
        if not isinstance(payload, (dict,list)): raise RuntimeError("Formato inesperado en respuesta DOF")
        # No se publica cero ni elementos hasta confirmar la estructura documental del servicio.
        status["dof"] = "reachable_unparsed"
        status["dof_message"] = "El servicio respondió; falta validar campos de documentos y enlaces individuales."
        status["dof_response_keys"] = list(payload.keys())[:30] if isinstance(payload,dict) else ["array"]
    except Exception as e:
        status["dof"] = "unavailable"
        errors.append("DOF: " + str(e))
    # Verifica disponibilidad del servicio SOAP y enumera su contrato WSDL sin asumir la firma de tesis.
    try:
        wsdl = get("https://sjf.scjn.gob.mx/sjfsem/Servicios/Semanario.asmx?WSDL")
        root = ET.fromstring(wsdl)
        ops = sorted({el.attrib.get("name") for el in root.iter() if el.tag.endswith("operation") and el.attrib.get("name")})
        if "ObtenerTesisSemana" not in ops: raise RuntimeError("WSDL accesible pero no enumera ObtenerTesisSemana")
        status["sjf"] = "reachable_unparsed"
        status["sjf_message"] = "WSDL accesible; falta validar parámetros y estructura de ObtenerTesisSemana."
        status["sjf_operations"] = ops
    except Exception as e:
        status["sjf"] = "unavailable"
        errors.append("SJF: " + str(e))
    # Mantiene cualquier contenido previamente publicado; el chequeo técnico nunca inventa publicaciones.
    try:
        with open(OUT, encoding="utf-8") as f: data = json.load(f)
    except Exception:
        data = {"period":"Sin cortes procesados","updated_at":None,"dof":[],"sjf":[]}
    data["source_status"] = status
    data["checked_at"] = now.isoformat()
    data["source_errors"] = errors
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(json.dumps(status, ensure_ascii=False, indent=2))
    # Una fuente sin parsear no es una consulta editorial exitosa; marca el job como diagnóstico, no como publicación.
    if errors: print("Una o más fuentes no respondieron; no se alteraron los resultados editoriales.")

if __name__ == "__main__":
    main()
