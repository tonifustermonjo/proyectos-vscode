"""
src/report_generator.py
-----------------------
Genera reportes finales de análisis en JSON y CSV.
Crea resúmenes ejecutivos con top ofertas recomendadas.
"""

import os
import json
import csv
from datetime import datetime
import pandas as pd
import config


def generar_reporte_json(ofertas_analizadas, filename=None):
    """
    Guarda análisis completo en JSON.
    
    Args:
        ofertas_analizadas (list): Ofertas con análisis Gemini
        filename (str, optional): Nombre archivo. Default: report_{timestamp}.json
    
    Returns:
        str: Ruta del archivo creado
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{timestamp}.json"
    
    filepath = os.path.join(config.DATA_REPORTS_DIR, filename)
    
    reporte = {
        "timestamp": datetime.now().isoformat(),
        "total_ofertas": len(ofertas_analizadas),
        "ofertas": ofertas_analizadas,
        "resumen": {
            "score_promedio": sum(o.get("score", 0) for o in ofertas_analizadas) / len(ofertas_analizadas) if ofertas_analizadas else 0,
            "recomendadas": len([o for o in ofertas_analizadas if o.get("recommendation") == "apply"]),
            "considerar": len([o for o in ofertas_analizadas if o.get("recommendation") == "consider"]),
            "descartar": len([o for o in ofertas_analizadas if o.get("recommendation") == "skip"])
        }
    }
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Reporte JSON: {filepath}")
    return filepath


def generar_reporte_csv(ofertas_analizadas, filename=None):
    """
    Guarda análisis en CSV para Excel/Sheets.
    
    Args:
        ofertas_analizadas (list): Ofertas con análisis
        filename (str, optional): Default: report_{timestamp}.csv
    
    Returns:
        str: Ruta del archivo
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{timestamp}.csv"
    
    filepath = os.path.join(config.DATA_REPORTS_DIR, filename)
    
    # Extraer campos para CSV
    rows = []
    for oferta in ofertas_analizadas:
        rows.append({
            "puesto": oferta.get("puesto", "N/A")[:50],
            "empresa": oferta.get("empresa", "N/A")[:30],
            "salario": oferta.get("salario", "N/A"),
            "score": oferta.get("score", 0),
            "match_%": oferta.get("match_percentage", 0),
            "recommendation": oferta.get("recommendation", "N/A"),
            "resumen": oferta.get("summary", "N/A")[:100],
            "red_flags": "; ".join(oferta.get("red_flags", [])),
            "fortalezas": "; ".join(oferta.get("strengths", []))
        })
    
    # Guardar CSV
    if rows:
        df = pd.DataFrame(rows)
        df.to_csv(filepath, index=False, encoding="utf-8")
        print(f"✅ Reporte CSV: {filepath}")
    
    return filepath


def generar_resumen_ejecutivo(ofertas_analizadas):
    """
    Imprime resumen ejecutivo en consola.
    
    Args:
        ofertas_analizadas (list): Ofertas analizadas
    """
    print("\n" + "=" * 70)
    print("📊 RESUMEN EJECUTIVO - ANÁLISIS DE OFERTAS")
    print("=" * 70)
    
    if not ofertas_analizadas:
        print("⚠️ No hay ofertas para mostrar")
        return
    
    # Estadísticas generales
    total = len(ofertas_analizadas)
    scores = [o.get("score", 0) for o in ofertas_analizadas]
    score_promedio = sum(scores) / total if total > 0 else 0
    
    print(f"\n📈 Estadísticas:")
    print(f"   Total ofertas analizadas: {total}")
    print(f"   Score promedio: {score_promedio:.1f}/10")
    print(f"   Score máximo: {max(scores):.1f}/10")
    print(f"   Score mínimo: {min(scores):.1f}/10")
    
    # Top 5 recomendadas
    print(f"\n🏆 Top 5 Ofertas Recomendadas:")
    top5 = ofertas_analizadas[:5]
    for i, oferta in enumerate(top5, 1):
        print(f"\n   {i}. {oferta.get('subject', 'N/A')[:60]}")
        print(f"      Empresa: {oferta.get('empresa', 'N/A')}")
        print(f"      Score: {oferta.get('score', 0)}/10")
        print(f"      Resumen: {oferta.get('summary', 'N/A')}")
        print(f"      Recomendación: {oferta.get('recommendation', 'N/A').upper()}")
    
    print(f"\n" + "=" * 70)


if __name__ == "__main__":
    print("📊 Generador de reportes")
    print("Esto se ejecutará desde el notebook principal")
