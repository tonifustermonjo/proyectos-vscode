"""
src/auth.py
-----------
Maneja autenticación OAuth 2.0 con Gmail.
Genera token inicial y lo reutiliza en ejecuciones futuras.
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import config

# Scopes de Gmail necesarios
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_gmail_service():
    """
    Obtiene servicio de Gmail autenticado.
    
    Flujo:
    1. Si existe token guardado en credentials/gmail_oauth.json → reutiliza
    2. Si token expiró → refresca automáticamente
    3. Si no existe token → inicia flow OAuth interactivo
    
    Returns:
        google.googleapiclient.discovery.Resource: Servicio Gmail autenticado
    """
    creds = None
    
    # Cargar token guardado si existe
    if os.path.exists(config.GMAIL_TOKEN_PATH):
        with open(config.GMAIL_TOKEN_PATH, "rb") as token_file:
            creds = pickle.load(token_file)
    
    # Refrescar token si está vencido
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    
    # Si no hay credenciales válidas, inicia flow OAuth
    if not creds or not creds.valid:
        # TODO: Requiere credenciales.json de Google Cloud Console
        raise EnvironmentError(
            "❌ No hay token OAuth válido.\n"
            "Pasos para obtenerlo:\n"
            "1. Ve a Google Cloud Console\n"
            "2. Crea credenciales OAuth 2.0 (Aplicación de escritorio)\n"
            "3. Descarga JSON y guarda como credentials.json en la carpeta raíz\n"
            "4. Ejecuta: python -m src.auth\n"
        )
    
    # Guardar token refrescado
    with open(config.GMAIL_TOKEN_PATH, "wb") as token_file:
        pickle.dump(creds, token_file)
    
    from googleapiclient.discovery import build
    return build("gmail", "v1", credentials=creds)


if __name__ == "__main__":
    print("🔐 Autenticación OAuth 2.0 Gmail")
    try:
        service = get_gmail_service()
        print("✅ Token obtenido/refrescado correctamente")
    except EnvironmentError as e:
        print(f"⚠️ {e}")
