# SmartGastro Web - Sistema de Gestión - Joaquin Hidalgo

Este proyecto es una aplicación web desarrollada con Flask para la gestión centralizada de inventario y optimización operativa de un Foodtruck. Integra persistencia relacional, seguridad criptográfica y consumo de APIs climáticas externas.

## Características Técnicas

* **Arquitectura Decoplada:** Backend estructurado en Flask con endpoints API que responden en formato JSON y Frontend dinámico basado en plantillas Jinja2 con peticiones asíncronas (`fetch`).
* **Persistencia Relacional (ORM):** Modelado de datos implementado con SQLAlchemy para entidades de Usuarios, Productos y Ventas, incluyendo lógica integrada de control defensivo de stock.
* **Seguridad:** Autenticación basada en sesiones de servidor firmadas criptográficamente y almacenamiento de contraseñas mediante hashing con Werkzeug.
* **Integración Externa:** Conexión resiliente a API meteorológica mediante la librería `requests`, incorporando políticas de timeout estricto y manejo de excepciones de red para mitigar caídas de servicios externos.

## Instalación y Configuración

1. **Clonar el repositorio:**
    ```bash
   git clone [https://github.com/Hidalgooo1/SmartGastro-Web-Joaquin-Hidalgo.git](https://github.com/Hidalgooo1/SmartGastro-Web-Joaquin-Hidalgo.git)
   cd SmartGastro-Web-Joaquin-Hidalgo

2. **Configurar el entorno virtual**
    ```bash
    python -m venv .venv
    En Windows (PowerShell):
    .\.venv\Scripts\Activate.ps1
    En Windows (CMD):
    .\.venv\Scripts\activate.bat
   
3. **Instalar dependencias**
    ```bash
   pip install -r requirements.txt

4. **Variables de entorno**
    ##### Crear un archivo .env en la raíz del proyecto basándose en el archivo .env.example provisto, configurando las siguientes claves:
    ```bash
   FLASK_DEBUG=True
    DATABASE_URL=sqlite:///smartgastro.db
    SECRET_KEY=tu_clave_secreta_aleatoria
   
5. **Ejecución**
    ```bash
   python app.py

##### El sistema inicializará automáticamente la base de datos relacional (smartgastro.db) y estará disponible en http://127.0.0.1:5000/.
##### Utilice el formulario de registrar nuevo usuario para crear una cuenta de prueba o en su defecto utilice user:joaquin / password:12345

