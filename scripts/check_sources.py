#!/usr/bin/env python3
"""Radar editorial gratuito. Solo publica registros oficiales recuperados y con URL verificable."""
import json, os, re, html, urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from xml.etree import ElementTree as ET

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,"data","radar.json")
TZ=ZoneInfo("America/Tijuana")
BASE="https://sidof.segob.gob.mx/dof/sidof"
SJF="https://sjf.scjn.gob.mx/sjfsem/Servicios/Semanario.asmx"
NS={"s":"http://schemas.xmlsoap.org/soap/envelope/","d":"http://sjf.scjn.gob.mx/"}
TOPICS={
 "Fiscal":["SAT","Código Fiscal de la Federación","contribuciones","impuesto sobre la renta","IVA","ISR","facultades de comprobación","crédito fiscal","devolución","compensación","multa","recargos","prescripción","caducidad","certificado de sello digital"],
 "Administrativo":["procedimiento administrativo","juicio contencioso","Tribunal Federal de Justicia Administrativa","TFJA","nulidad","competencia","fundamentación y motivación","responsabilidad administrativa","sanción administrativa","acto administrativo"],
 "Seguridad social y aduanas":["IMSS","INFONAVIT","cuotas obrero patronales","seguridad social","aduana","comercio exterior","pedimento","arancel"],
 "Litigio y amparo":["amparo","suspensión","recurso de revocación","ejecución de sentencia","cumplimiento de sentencia","interés jurídico","interés legítimo"]
}
def request(url, data=None, headers=None):
    req=urllib.request.Request(url,data=data,headers={"User-Agent":"RadarFiscalAdministrativo/1.0","Accept":"application/json, text/xml, */*",**(headers or {})})
    with urllib.request.urlopen(req,timeout=45) as r:
        b=r.read()
        if r.status!=200: raise RuntimeError("HTTP "+str(r.status))
        return b
def clean(v):
    v=html.unescape(re.sub(r"<[^>]+>"," ",str(v or "")))
    return re.sub(r"\\s+"," ",v).strip()
def walk(obj):
    if isinstance(obj,dict):
        yield obj
        for v in obj.values(): yield from walk(v)
    elif isinstance(obj,list):
        for v in obj: yield from walk(v)
def matches(text):
    t=text.casefold()
    return [k for k,terms in TOPICS.items() if any(x.casefold() in t for x in terms)]
def date_fmt(d): return d.strftime("%d-%m-%Y")
def load():
    try:
        with open(OUT,encoding="utf-8") as f: return json.load(f)
    except Exception: return {"period":"Sin cortes procesados","updated_at":None,"dof":[],"sjf":[]}
def dof_cut(day):
    payload=json.loads(request(f"{BASE}/notas/{date_fmt(day)}").decode("utf-8-sig"))
    if str(payload.get("messageCode","200")) not in ("200","OK") or str(payload.get("response","OK")).lower() not in ("ok","success","200"):
        raise RuntimeError("SIDOF reportó error: "+str(payload.get("response")))
    candidates=[]
    for obj in walk(payload):
        code=obj.get("codNota") or obj.get("codigo") or obj.get("codNotaId")
        title=obj.get("titulo") or obj.get("tituloNota") or obj.get("nombre") or obj.get("descripcion")
        if code and title:
            candidates.append((str(code),clean(title),obj))
    # El endpoint de notas es la fuente primaria; si el esquema cambia, no se declara un corte vacío.
    if not candidates and payload.get("ListaNotas") not in ([],None):
        raise RuntimeError("Respuesta SIDOF sin campos de nota reconocibles; se conserva el último corte.")
    out=[]
    seen=set()
    for code,title,obj in candidates:
        if code in seen: continue
        seen.add(code)
        detail=json.loads(request(f"{BASE}/notas/nota/{code}").decode("utf-8-sig"))
        details=list(walk(detail))
        body=""
        for x in details:
            for key in ("texto","contenido","contenidoNota","html","descripcion"):
                if x.get(key) and len(clean(x[key]))>len(body): body=clean(x[key])
        whole=title+" "+body
        cats=matches(whole)
        if not cats: continue
        url=f"https://sidof.segob.gob.mx/dof/sidof/notas/nota/{code}"
        out.append({"id":"dof-"+code,"title":title,"headline":title,"summary":(body[:650] if body else "Publicación oficial identificada por materia: "+", ".join(cats)+". Consulta el texto íntegro en la fuente oficial."),"topics":cats,"date":day.isoformat(),"source":"DOF","url":url})
    return out
def soap_call(operation, inner):
    envelope=f'''<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns="http://sjf.scjn.gob.mx/"><soap:Body><{operation}>{inner}</{operation}></soap:Body></soap:Envelope>'''.encode()
    raw=request(SJF,data=envelope,headers={"Content-Type":"text/xml; charset=utf-8","SOAPAction":f'"http://sjf.scjn.gob.mx/{operation}"'})
    root=ET.fromstring(raw)
    fault=root.find(".//{http://schemas.xmlsoap.org/soap/envelope/}Fault")
    if fault is not None: raise RuntimeError("SOAP Fault: "+clean(ET.tostring(fault,encoding="unicode")))
    return root
def sjf_cut():
    # tipo_doc=1 corresponde al catálogo de tesis; validar por resultado y fallar cerrado.
    weeks=soap_call("ObtenerSemanas","<tipo_doc>1</tipo_doc>")
    week_nodes=weeks.findall(".//d:ObtenerSemanasResult/d:SemanarioBE",NS)
    if not week_nodes: raise RuntimeError("SJF no devolvió semanas para tipo_doc=1; no se presume que no existan tesis.")
    latest=max(week_nodes,key=lambda n:int(n.findtext("d:Id",default="0",namespaces=NS)))
    week_id=latest.findtext("d:Id",namespaces=NS)
    publication=latest.findtext("d:Publicacion",default="",namespaces=NS)
    if not week_id: raise RuntimeError("Semana SJF sin identificador.")
    tesis=soap_call("ObtenerTesisSemana",f"<SemanaId>{int(week_id)}</SemanaId>")
    records=tesis.findall(".//d:ObtenerTesisSemanaResult/*",NS)
    if not records: raise RuntimeError("SJF devolvió una semana sin registros reconocibles.")
    out=[]
    for node in records:
        fields={c.tag.split("}")[-1]:clean(c.text) for c in node.iter() if c is not node and c.text}
        title=fields.get("Rubro") or fields.get("Titulo") or fields.get("rubro")
        text= " ".join(fields.values())
        cats=matches(text)
        if not title or not cats: continue
        # Enlace directo oficial al buscador SJF con identificador cuando el servicio lo proporcione.
        ident=fields.get("Id") or fields.get("IdTesis") or fields.get("RegistroDigital")
        if not ident: raise RuntimeError("Tesis candidata sin identificador verificable; se cancela el corte.")
        url="https://sjf2.scjn.gob.mx/detalle/tesis/"+ident
        excerpt=fields.get("Texto") or fields.get("Precedente") or text
        out.append({"id":"sjf-"+ident,"title":title,"headline":title,"summary":excerpt[:650],"topics":cats,"date":publication,"source":"SJF","url":url})
    return out,publication
def main():
    now=datetime.now(TZ); data=load()
    status=data.get("source_status",{})
    errors=[]
    if os.environ.get("RADAR_SOURCE","both") in ("both","dof"):
        try:
            items=dof_cut(now.date())
            data["dof"]=items; status["dof"]="success"
            status["dof_checked_at"]=now.isoformat()
            status["dof_message"]="Consulta oficial completada; "+str(len(items))+" publicaciones relevantes."
        except Exception as e:
            status["dof"]="unavailable"; status["dof_message"]="Consulta no disponible; se conserva el último corte."
            errors.append("DOF: "+str(e))
    if os.environ.get("RADAR_SOURCE","both") in ("both","sjf") and now.weekday()==4 and now.hour>=12:
        try:
            items,period=sjf_cut()
            data["sjf"]=items; status["sjf"]="success"
            status["sjf_checked_at"]=now.isoformat()
            status["sjf_message"]="Semana oficial consultada: "+period+". "+str(len(items))+" tesis candidatas."
        except Exception as e:
            status["sjf"]="unavailable"; status["sjf_message"]="Consulta no disponible; se conserva el último corte."
            errors.append("SJF: "+str(e))
    data["source_status"]=status
    data["source_errors"]=errors
    data["checked_at"]=now.isoformat()
    data["updated_at"]=now.isoformat()
    data["period"]="Corte "+now.strftime("%d/%m/%Y %H:%M")+" (hora de Tijuana)"
    with open(OUT,"w",encoding="utf-8") as f: json.dump(data,f,ensure_ascii=False,indent=2); f.write("\n")
    print(json.dumps({"status":status,"errors":errors,"counts":{"dof":len(data.get("dof",[])),"sjf":len(data.get("sjf",[]))}},ensure_ascii=False))
    if errors: raise SystemExit(1)
if __name__=="__main__": main()
