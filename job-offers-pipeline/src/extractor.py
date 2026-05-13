"""
src/extractor.py
----------------
Descarga emails de ofertas de empleo desde Gmail.
Busca emails de LinkedIn y guarda contenido en data/raw/.
"""

import os
import json
import base64
from datetime import datetime
import config


# Remitente real típico de alertas de LinkedIn en Gmail.
DEFAULT_LINKEDIN_QUERY = (
    'from:jobalerts-noreply@linkedin.com '
    '(subject:"job alert" OR subject:"empleo" OR subject:"oferta")'
)


def buscar_ofertas_emails(service, query=DEFAULT_LINKEDIN_QUERY, max_results=10):
    """
    Busca emails de ofertas en Gmail según query.
    
    Args:
        service: Servicio Gmail autenticado
        query (str): Query de búsqueda en Gmail.
            Por defecto usa remitente real de LinkedIn Alerts.
        max_results (int): Límite de emails a descargar
    
    Returns:
        list: Lista de dicts con {message_id, subject, from, body_html}
    
    Notas:
        - Gmail API pagina resultados, por eso max_results es local
        - Guardamos el body en HTML para procesamiento posterior
    """
    try:
        # Ejecutar búsqueda
        results = service.users().messages().list(
            userId="me",
            q=query,
            maxResults=max_results
        ).execute()
        
        messages = results.get("messages", [])
        if not messages:
            print(f"⚠️ No se encontraron emails con query: {query}")
            return []
        
        ofertas = []
        for msg in messages:
            msg_id = msg["id"]
            # Obtener contenido completo del email
            full_msg = service.users().messages().get(
                userId="me",
                id=msg_id,
                format="full"
            ).execute()
            
            headers = full_msg["payload"]["headers"]
            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "Sin asunto")
            from_addr = next((h["value"] for h in headers if h["name"] == "From"), "Desconocido")
            
            # Extraer body (puede estar en parts si es multipart)
            body = extract_body(full_msg["payload"])
            
            ofertas.append({
                "message_id": msg_id,
                "subject": subject,
                "from": from_addr,
                "body_html": body,
                "timestamp": datetime.now().isoformat()
            })
        
        return ofertas
    
    except Exception as e:
        print(f"❌ Error extrayendo emails: {e}")
        return []


def extract_body(payload):
    """Extrae body HTML del payload del email (maneja multipart)"""
    if "parts" in payload:
        # Multipart: buscar HTML o plaintext
        for part in payload["parts"]:
            if part["mimeType"] == "text/html":
                data = part["body"].get("data", "")
                return base64.urlsafe_b64decode(data).decode("utf-8")
            elif part["mimeType"] == "text/plain":
                data = part["body"].get("data", "")
                return base64.urlsafe_b64decode(data).decode("utf-8")
    else:
        # Simple: body directo
        data = payload["body"].get("data", "")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8")
    return ""


def guardar_ofertas_raw(ofertas, filename=None):
    """
    Guarda ofertas brutos en data/raw/ como JSON.
    
    Args:
        ofertas (list): Lista de dicts con ofertas
        filename (str, optional): Nombre archivo. Default: timestamp.json
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"emails_{timestamp}.json"
    
    filepath = os.path.join(config.DATA_RAW_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(ofertas, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {len(ofertas)} ofertas guardadas en {filepath}")
    return filepath


if __name__ == "__main__":
    print("📧 Extractor de ofertas de empleo")
    print("Query por defecto:")
    print(f"  {DEFAULT_LINKEDIN_QUERY}")
