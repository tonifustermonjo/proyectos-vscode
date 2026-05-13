"""
src/ai_analyzer.py
------------------
Analiza ofertas con Gemini 1.5 Pro.
Puntúa (0-10) y resume según perfil de usuario.
"""

import json
import google.generativeai as genai
import config


def inicializar_gemini():
    """Configura cliente de Gemini"""
    genai.configure(api_key=config.GEMINI_API_KEY)
    return genai


def construir_prompt(oferta, perfil_usuario):
    """
    Construye prompt para Gemini analizando la oferta.
    
    Args:
        oferta (dict): Oferta procesada con {empresa, puesto, salario, requisitos...}
        perfil_usuario (str): Descripción del perfil buscado
    
    Returns:
        str: Prompt listo para enviar a Gemini
    """
    prompt = f"""
Eres un reclutador senior con 10 años de experiencia en tecnología.
Tu tarea es evaluar esta oferta de empleo.

## Perfil objetivo del candidato:
{perfil_usuario}

## Oferta de empleo:
- Empresa: {oferta.get('empresa', 'No especificada')}
- Puesto: {oferta.get('puesto', 'No especificado')}
- Salario: {oferta.get('salario', 'No especificado')}
- Requisitos: {', '.join(oferta.get('requisitos', []))}
- URL: {oferta.get('url', 'No disponible')}
- Resumen: {oferta.get('texto_original', '')[:200]}

## Tarea:
Analiza esta oferta y devuelve un JSON válido con:
1. "score": puntuación 0-10 (10=match perfecto, 0=no apto)
2. "match_percentage": % de coincidencia con el perfil
3. "summary": resumen de 2-3 líneas
4. "strengths": lista de puntos fuertes de la oferta
5. "red_flags": lista de posibles problemas o riesgos
6. "recommendation": "apply", "consider", o "skip"

Devuelve SOLO el JSON válido, sin markdown, sin explicaciones adicionales.
"""
    return prompt


def analizar_oferta(oferta, perfil_usuario="Data Engineer con 5+ años, Python, ETL, SQL"):
    """
    Analiza oferta individual con Gemini.
    
    Args:
        oferta (dict): Oferta procesada
        perfil_usuario (str): Descripción del perfil buscado
    
    Returns:
        dict: Análisis con {score, summary, red_flags, strengths}
    """
    try:
        genai.configure(api_key=config.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-pro")
        
        prompt = construir_prompt(oferta, perfil_usuario)
        response = model.generate_content(prompt)
        
        # Parsear respuesta
        respuesta_texto = response.text.strip()
        if respuesta_texto.startswith("```json"):
            respuesta_texto = respuesta_texto[7:-3]
        
        analisis = json.loads(respuesta_texto)
        
        return {
            "message_id": oferta["message_id"],
            "subject": oferta["subject"],
            **analisis
        }
    
    except json.JSONDecodeError:
        print(f"⚠️ Error parseando respuesta Gemini para: {oferta.get('subject')}")
        return {
            "message_id": oferta["message_id"],
            "subject": oferta["subject"],
            "score": 0,
            "summary": "Error en análisis",
            "error": "JSON parsing failed"
        }
    
    except Exception as e:
        print(f"❌ Error analizando oferta: {e}")
        return {
            "message_id": oferta["message_id"],
            "subject": oferta["subject"],
            "score": 0,
            "summary": "Error en análisis",
            "error": str(e)
        }


def analizar_lote_ofertas(ofertas, perfil_usuario="Data Engineer con 5+ años, Python, ETL, SQL"):
    """
    Analiza múltiples ofertas.
    
    Args:
        ofertas (list): Lista de ofertas procesadas
        perfil_usuario (str): Descripción del perfil
    
    Returns:
        list: Ofertas con análisis Gemini, ordenadas por score descendente
    """
    print(f"🤖 Analizando {len(ofertas)} ofertas con Gemini 1.5 Pro...")
    
    analisis_list = []
    for i, oferta in enumerate(ofertas, 1):
        print(f"   [{i}/{len(ofertas)}] {oferta.get('subject', 'Sin asunto')[:60]}")
        analisis = analizar_oferta(oferta, perfil_usuario)
        analisis_list.append(analisis)
    
    # Ordenar por score
    analisis_list.sort(key=lambda x: x.get("score", 0), reverse=True)
    
    print(f"✅ Análisis completado. Top 3:")
    for i, anal in enumerate(analisis_list[:3], 1):
        print(f"   {i}. {anal.get('subject', 'N/A')} - Score: {anal.get('score', '?')}/10")
    
    return analisis_list


if __name__ == "__main__":
    print("🤖 Analizador IA con Gemini")
    print("Esto se ejecutará desde el notebook principal")
