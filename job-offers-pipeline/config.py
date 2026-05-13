"""
config.py
---------
Centraliza la configuración del pipeline.
Carga variables de .env y valida que existan las críticas.
"""

import os
from dotenv import load_dotenv

# Cargar variables de .env
load_dotenv()

# Variables críticas que deben estar definidas
REQUIRED_VARS = ["GMAIL_CLIENT_ID", "GMAIL_CLIENT_SECRET", "GEMINI_API_KEY"]

# Validar que todas las variables críticas existan
missing_vars = [var for var in REQUIRED_VARS if not os.getenv(var) or "aqui" in os.getenv(var, "")]
if missing_vars:
    raise EnvironmentError(
        f"❌ Faltan configurar estas variables en .env:\n"
        f"   {', '.join(missing_vars)}\n\n"
        f"Instrucciones:\n"
        f"1. Copia .env.example a .env (si existe)\n"
        f"2. Rellena con tus valores reales de Google Cloud Console\n"
        f"3. Nunca commitees .env a git"
    )

# Gmail OAuth 2.0
GMAIL_CLIENT_ID = os.getenv("GMAIL_CLIENT_ID")
GMAIL_CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET")
GMAIL_REDIRECT_URI = os.getenv("GMAIL_REDIRECT_URI", "http://localhost:8080")

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configuración del pipeline
JOB_KEYWORDS = os.getenv("JOB_KEYWORDS", '["Data Engineer", "Python", "ETL"]')
MIN_SCORE_THRESHOLD = int(os.getenv("MIN_SCORE_THRESHOLD", "7"))
OUTPUT_FORMAT = os.getenv("OUTPUT_FORMAT", "json")

# Rutas del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
DATA_REPORTS_DIR = os.path.join(BASE_DIR, "data", "reports")
CREDENTIALS_DIR = os.path.join(BASE_DIR, "credentials")
GMAIL_TOKEN_PATH = os.path.join(CREDENTIALS_DIR, "gmail_oauth.json")

# Crear directorios si no existen
for directory in [DATA_RAW_DIR, DATA_PROCESSED_DIR, DATA_REPORTS_DIR, CREDENTIALS_DIR]:
    os.makedirs(directory, exist_ok=True)

if __name__ == "__main__":
    print("✅ Configuración validada correctamente")
    print(f"   GMAIL_CLIENT_ID: {GMAIL_CLIENT_ID[:20]}...")
    print(f"   GEMINI_API_KEY: {GEMINI_API_KEY[:20]}...")
    print(f"   MIN_SCORE_THRESHOLD: {MIN_SCORE_THRESHOLD}")
    print(f"   DATA_REPORTS_DIR: {DATA_REPORTS_DIR}")
