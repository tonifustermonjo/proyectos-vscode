# Job Offers Pipeline - Automatización de Análisis de Ofertas de Empleo

## 🎯 Objetivo

Crear un pipeline automatizado que:
1. ✅ Se autentica con **Gmail OAuth 2.0** de forma segura
2. 📧 Extrae correos de ofertas de **LinkedIn**
3. 🔧 Procesa HTML → texto limpio y extrae campos estructurados
4. 🤖 Analiza ofertas con **Gemini 1.5 Pro** (puntuación + resumen)
5. 📊 Genera reportes en **JSON y CSV**

---

## 🚀 Quick Start

### Prerequisitos
- Python 3.13+
- Conda (ya instalado en tu sistema)
- Cuenta Google con acceso a Gmail
- API Key de Gemini (gratuita en Google AI Studio)

### 1. Setup Inicial (5 minutos)

```bash
# Navega a la carpeta del proyecto
cd job-offers-pipeline

# Activa el entorno
conda activate job-offers

# Verifica que las dependencias estén instaladas
pip list | grep -E "google|gemini|pandas|beautifulsoup"
```

### 2. Configurar Credenciales (.env)

Edita el archivo `.env` en la raíz y rellena:

```env
# Gmail OAuth (obtén de Google Cloud Console)
GMAIL_CLIENT_ID=tu_client_id_aqui.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=tu_client_secret_aqui
GMAIL_REDIRECT_URI=http://localhost:8080

# Gemini API (obtén de Google AI Studio)
GEMINI_API_KEY=tu_api_key_aqui

# Configuración del pipeline
JOB_KEYWORDS=["Data Engineer", "Python", "ETL"]
MIN_SCORE_THRESHOLD=7
OUTPUT_FORMAT=json
```

### 3. Ejecutar el Notebook

```bash
# Desde la raíz del proyecto
jupyter notebook notebooks/01_job_pipeline_dev.ipynb
```

O en VS Code:
- Abre el notebook en VS Code
- Selecciona kernel `job-offers`
- Ejecuta celdas en orden

---

## 📁 Estructura del Proyecto

```
job-offers-pipeline/
├── .env                      # Secretos (NO commitear)
├── .gitignore               # Ignora .env, credenciales, datos
├── config.py                # Configuración centralizada + validación
├── requirements.txt         # Dependencias pip
│
├── src/                     # Módulos del pipeline
│   ├── auth.py             # OAuth 2.0 Gmail
│   ├── extractor.py        # Descarga emails
│   ├── processor.py        # HTML → texto limpio
│   ├── ai_analyzer.py      # Gemini API
│   ├── report_generator.py # Exporta reportes
│   └── utils.py            # Helpers
│
├── notebooks/
│   └── 01_job_pipeline_dev.ipynb  # Desarrollo interactivo
│
├── data/
│   ├── raw/                 # Emails brutos
│   ├── processed/           # Datos procesados
│   └── reports/             # Reportes JSON/CSV
│
└── credentials/             # Token OAuth (git-ignored)
```

---

## 🔐 Obtener Credenciales

### Gmail OAuth 2.0

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto
3. Habilita **Gmail API**
4. Ve a **Credenciales** → **+ Crear credencial**
5. Selecciona **OAuth 2.0** → **Aplicación de escritorio**
6. Descarga el JSON y guárdalo como `credentials.json` en la raíz del proyecto
7. Copia `client_id` y `client_secret` a `.env`

### Gemini API Key

1. Ve a [Google AI Studio](https://aistudio.google.com/)
2. Haz clic en **Get API Key**
3. Copia la key a `.env`

---

## 📊 Flujo del Pipeline

```
┌─────────────────────┐
│  Gmail OAuth 2.0    │ ← Autentica 1 vez, reutiliza token
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ Extraer Emails      │ ← Busca de LinkedIn
└──────────┬──────────┘
           │ (body HTML + metadatos)
┌──────────▼──────────┐
│ Procesar Contenido  │ ← HTML→texto, regex campos
└──────────┬──────────┘
           │ (empresa, puesto, salario, requisitos)
┌──────────▼──────────┐
│  Gemini 1.5 Pro     │ ← Score 0-10, resumen, red_flags
└──────────┬──────────┘
           │ (análisis estructurado JSON)
┌──────────▼──────────┐
│ Generar Reportes    │ ← JSON + CSV, resumen ejecutivo
└─────────────────────┘
```

---

## 🎓 Decisiones Técnicas (Trade-offs)

| Aspecto | Decisión | Alternativa | Por qué | Costo |
|--------|----------|-------------|--------|-------|
| **Seguridad** | OAuth 2.0 | Contraseña | No expones credencial | Setup Google Cloud |
| **Parsing HTML** | BeautifulSoup | Regex puro | Robusto ante variantes HTML | Overhead mínimo |
| **IA** | Gemini API | LLM local | Inteligencia superior | Latencia + costo API |
| **Arquitectura** | Modular (6 módulos) | Monolito | Testeable, escalable | Más archivos |
| **Config** | .env file | Hardcode | Seguridad, reproducible | Setup local |
| **Dev** | Notebook primero | Script directo | Prototipado rápido | Refactor a script después |

---

## 🛠️ Troubleshooting

### Error: "Faltan variables en .env"
```
❌ Faltan configurar estas variables en .env:
   GMAIL_CLIENT_ID, GEMINI_API_KEY
```
**Solución**: Rellena todas las variables en `.env` con valores reales (no dejes "aqui")

### Error: "No hay token OAuth válido"
```
❌ No hay token OAuth válido.
```
**Solución**: 
1. Descarga `credentials.json` de Google Cloud Console
2. Guárdalo en la raíz del proyecto
3. Descomenta y ejecuta la celda de autenticación

### Error: "GEMINI_API_KEY inválida"
```
❌ Error en análisis: APIError
```
**Solución**: Valida que tu key funcione en [Google AI Studio](https://aistudio.google.com/)

---

## 📈 Próximas Mejoras

- [ ] Scheduling diario con APScheduler o cron
- [ ] Integración Slack para notificaciones
- [ ] Base de datos SQLite para historial
- [ ] Web UI con Streamlit
- [ ] Filtros por ubicación, salario mínimo
- [ ] Tracking de aplicaciones enviadas

---

## 📚 Referencias

- [Google Gmail API Docs](https://developers.google.com/gmail/api)
- [Gemini API Docs](https://ai.google.dev/gemini-api/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)

---

## ⚖️ Licencia

MIT - Siéntete libre de usar y modificar para tus proyectos personales

---

## 📝 Notas

- **Seguridad**: Nunca commitees `.env` a Git. Está en `.gitignore`
- **Desarrollo**: Este es un proyecto educativo para practicar con LangChain + APIs
- **Evolución**: Puedes convertir el notebook a script (`main.py`) para scheduling después

¡Éxito en tu carrera como Data Engineer! 🚀
