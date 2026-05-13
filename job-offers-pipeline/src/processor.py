"""
src/processor.py
----------------
Procesa emails crudos: HTML → texto limpio, extrae campos estructurados.
Convierte contenido desordenado en JSON estructurado.
"""

import re
from bs4 import BeautifulSoup
import html2text
import json


def limpiar_html(html_content):
    """
    Convierte HTML → texto limpio.
    
    Args:
        html_content (str): Contenido HTML del email
    
    Returns:
        str: Texto limpio y legible
    """
    # Parse HTML con BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Convertir a markdown/texto con html2text
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.body_width = 0  # No romper líneas
    
    texto_limpio = h.handle(str(soup))
    return texto_limpio.strip()


def extraer_campos(texto_oferta):
    """
    Extrae campos clave de oferta de texto limpio.
    
    Busca patrones como:
    - Empresa: LinkedIn, Tech Corp, etc
    - Puesto: Data Engineer, Senior Python Developer
    - Salario: €45000, $50000, 45k-55k
    - Requisitos: Python, SQL, ETL
    
    Args:
        texto_oferta (str): Texto limpio de la oferta
    
    Returns:
        dict: {empresa, puesto, salario, requisitos, ubicacion, url}
    """
    campos = {
        "empresa": None,
        "puesto": None,
        "salario": None,
        "requisitos": [],
        "ubicacion": None,
        "url": None,
        "urls_detectadas": [],
        "texto_original": texto_oferta[:500]  # Primeros 500 chars como referencia
    }
    
    # Buscar puesto (suele estar en línea 1-2)
    lineas = texto_oferta.split("\n")
    if lineas:
        # Heurística: linea 1-3 puede contener puesto
        campos["puesto"] = lineas[0][:100] if lineas[0] else None
    
    # Buscar salario (patrones: €45000, $50000, 45k, 45000-55000)
    patron_salario = r'(€|\$)?(\d+[.,]\d+|\d+)\s*(k|€|\$)?|(\d+)\s*-\s*(\d+)\s*€'
    match_salario = re.search(patron_salario, texto_oferta)
    if match_salario:
        campos["salario"] = match_salario.group(0)
    
    # Buscar requisitos (palabras clave técnicas)
    keywords = ["Python", "SQL", "ETL", "Spark", "Pandas", "AWS", "Azure", "GCP", 
                "Docker", "Kubernetes", "Git", "Java", "Scala", "R", "API"]
    campos["requisitos"] = [kw for kw in keywords if kw.lower() in texto_oferta.lower()]
    
    # Buscar URLs (enlaces a postulación)
    patron_url = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(patron_url, texto_oferta)
    campos["urls_detectadas"] = urls
    if urls:
        # Si el correo es corto, suele traer solo enlaces; priorizamos URL de empleo LinkedIn.
        linkedin_job_urls = [
            u for u in urls
            if "linkedin.com/jobs" in u or "linkedin.com/job" in u
        ]
        campos["url"] = linkedin_job_urls[0] if linkedin_job_urls else urls[0]
    
    return campos


def procesar_ofertas(ofertas_raw):
    """
    Procesa lote de ofertas brutas → ofertas estructuradas.
    
    Args:
        ofertas_raw (list): Ofertas del extractor (con body_html)
    
    Returns:
        list: Ofertas procesadas con campos estructurados
    """
    ofertas_procesadas = []
    
    for oferta in ofertas_raw:
        try:
            # Limpiar HTML
            texto = limpiar_html(oferta["body_html"])
            
            # Extraer campos
            campos = extraer_campos(texto)
            
            # Combinar
            oferta_procesada = {
                "message_id": oferta["message_id"],
                "subject": oferta["subject"],
                "from": oferta["from"],
                "timestamp": oferta["timestamp"],
                **campos  # Spread de campos extraídos
            }
            
            ofertas_procesadas.append(oferta_procesada)
        
        except Exception as e:
            print(f"⚠️ Error procesando oferta {oferta.get('subject', 'Unknown')}: {e}")
            continue
    
    return ofertas_procesadas


if __name__ == "__main__":
    print("🔧 Processor de ofertas")
    print("Esto se ejecutará desde el notebook principal")
