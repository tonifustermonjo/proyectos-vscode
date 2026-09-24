import os
from dotenv import load_dotenv
from google import genai

# Esta línea es la que lee el archivo .env e inyecta GEMINI_API_KEY en os.environ
load_dotenv()

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Responde solo: 'Conexión OK con Gemini 3.6'",
)

print(response.text)