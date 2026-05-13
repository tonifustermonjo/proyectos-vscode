"""
src/utils.py
------------
Funciones de utilidad compartidas.
"""

import os
import json
from pathlib import Path


def crear_directorios_si_no_existen(directorios):
    """Crea directorios si no existen"""
    for dir_path in directorios:
        os.makedirs(dir_path, exist_ok=True)


def cargar_json(filepath):
    """Carga JSON desde archivo"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Error cargando {filepath}: {e}")
        return None


def guardar_json(data, filepath):
    """Guarda datos como JSON"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Guardado: {filepath}")
        return True
    except Exception as e:
        print(f"❌ Error guardando {filepath}: {e}")
        return False


def listar_archivos_en_directorio(dirpath, extension=None):
    """Lista archivos en directorio, opcionalmente filtrando por extensión"""
    try:
        archivos = []
        for archivo in os.listdir(dirpath):
            if extension and not archivo.endswith(extension):
                continue
            ruta_completa = os.path.join(dirpath, archivo)
            if os.path.isfile(ruta_completa):
                archivos.append(archivo)
        return sorted(archivos, reverse=True)  # Más recientes primero
    except Exception as e:
        print(f"⚠️ Error listando {dirpath}: {e}")
        return []


if __name__ == "__main__":
    print("🛠️ Utilidades")
    print("Esto se ejecutará desde otros módulos")
