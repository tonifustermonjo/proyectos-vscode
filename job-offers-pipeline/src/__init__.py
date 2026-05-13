"""
src - Package principal del pipeline
"""

__version__ = "0.1.0"
__author__ = "Data Engineer Student"

# Validar config al importar el paquete
try:
    import config
except EnvironmentError as e:
    print(f"⚠️ Config error: {e}")
