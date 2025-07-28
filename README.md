# 🧠 Proyectos VSCode

Entorno organizado en Visual Studio Code con Jupyter, Python (Anaconda), Conda y Git. Ideal para trabajar en proyectos de **Data Engineering**, **Databricks** y **AI con LangChain / OpenAI**.

---

## 📁 Estructura del Proyecto

```
ProyectosVSCode/
│
├── notebooks_anaconda/     # Notebooks Jupyter de pruebas o prototipos
│   ├── prueba.ipynb
│   └── test.ipynb
│
├── scripts/                # Módulos y funciones reutilizables
│   └── __init__.py
│
├── .vscode/                # Configuración de Visual Studio Code
├── .gitignore              # Archivos a ignorar por Git
├── requirements.txt        # Dependencias clave del proyecto
├── installed.txt           # Lista congelada de paquetes instalados
├── README.md               # Este archivo
└── LICENSE                 # Licencia MIT
```

---

## 🔧 Tecnologías utilizadas

### 🐍 Python y Entorno
- Python 3.13.5 (entorno `py313`)
- Jupyter Notebook / Lab
- Anaconda

### 🏗️ Data Engineering
- `pandas`, `numpy`, `openpyxl`
- `azure-storage-blob`, `azure-identity`
- `pyspark`, `databricks-cli` *(opcional)*

### 🤖 IA / LLMs
- `langchain`, `openai`, `chromadb`
- `sentence-transformers`, `tiktoken`

### 🧰 Utilidades
- `tqdm`, `python-dotenv`

## 💻 Instalación del entorno

1. Clona el repositorio:

    ```bash
    git clone https://github.com/tonifustermonjo/proyectos-vscode.git
    cd proyectos-vscode
    ```

2. Crea el entorno con Conda:

    ```bash
    conda create --name py313 python=3.13.5
    conda activate py313
    ```

3. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4. (Opcional) Congela las dependencias instaladas:

    ```bash
    pip freeze > installed.txt
    ```

---

## 🧾 Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.  
Consulta el archivo [`LICENSE`](./LICENSE) para más detalles.
