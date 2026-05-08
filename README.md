# 🧪 pre-entrega-automation-testing-federico-tresen

Proyecto de automatización de pruebas para el sitio [saucedemo.com](https://www.saucedemo.com), desarrollado como pre-entrega del curso de **Testing Automation**.

---

## 📋 Propósito del Proyecto

Automatizar y validar los flujos principales del sitio saucedemo.com utilizando Selenium WebDriver y Pytest. El proyecto cubre tres escenarios críticos:

1. **Login automatizado** con validación de redirección y título de página
2. **Navegación en el inventario** con verificación de productos y elementos de interfaz
3. **Gestión del carrito** con verificación de contador y contenido

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.10.4 | Lenguaje principal |
| Selenium WebDriver | 4.18.1 | Automatización del navegador |
| Pytest | 8.1.1 | Framework de testing |
| pytest-html | 4.1.1 | Generación de reportes HTML |
| webdriver-manager | 4.0.1 | Gestión automática del ChromeDriver |

---

## 📁 Estructura del Proyecto

```
pre-entrega-automation-testing-federico-tresen/
│
├── tests/
│   ├── __init__.py
│   └── test_saucedemo.py       # Suite principal de pruebas (3 casos)
│
├── utils/
│   ├── __init__.py
│   └── helpers.py              # Funciones auxiliares reutilizables
│
├── reports/                    # Reportes HTML generados (se crea automáticamente)
│
├── conftest.py                 # Fixtures globales de Pytest (setup/teardown del driver)
├── pytest.ini                  # Configuración de Pytest
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Este archivo
```

---

## ⚙️ Instalación de Dependencias

### 1. Clonar el repositorio

```bash
git clone https://github.com/FedericoTresen/pre-entrega-automation-testing-federico-tresen.git
cd pre-entrega-automation-testing-federico-tresen
```

### 2. Crear y activar un entorno virtual (recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en Mac/Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

> ✅ `webdriver-manager` descarga automáticamente la versión correcta de ChromeDriver. No es necesario instalarlo manualmente.

---

## ▶️ Cómo Ejecutar las Pruebas

### Ejecutar todos los tests con salida detallada

```bash
pytest -v
```

### Ejecutar un test específico

```bash
pytest tests/test_saucedemo.py::TestLogin::test_login_exitoso -v
pytest tests/test_saucedemo.py::TestNavegacion::test_navegacion_inventario -v
pytest tests/test_saucedemo.py::TestCarrito::test_agregar_al_carrito -v
```

### Generar reporte HTML

```bash
pytest tests/test_saucedemo.py -v --html=reports/reporte.html
```

El reporte se genera en `reports/reporte.html` y puede abrirse directamente en el navegador.

---

## 🧪 Casos de Prueba

### Test 1: Login Exitoso (`TestLogin`)
- Navega a la página de login de saucedemo.com
- Ingresa credenciales válidas (`standard_user` / `secret_sauce`)
- Valida redirección a `/inventory.html`
- Valida que el título de la sección sea `"Products"` / `"Swag Labs"`

### Test 2: Navegación en Inventario (`TestNavegacion`)
- Verifica que el título de la página sea `"Products"`
- Comprueba que exista al menos un producto visible
- Muestra nombre y precio del primer producto
- Valida presencia del menú de navegación y filtro de ordenamiento

### Test 3: Carrito de Compras (`TestCarrito`)
- Verifica que el carrito comienza vacío
- Agrega el primer producto al carrito
- Verifica que el contador del carrito se incrementa a 1
- Navega al carrito y verifica que el producto agregado aparece correctamente

---

## 📌 Notas adicionales

- Los tests son **independientes entre sí**: cada uno realiza su propio login y no depende del estado de los demás.
- Se utilizan **esperas explícitas** (`WebDriverWait`) para garantizar estabilidad ante cargas lentas.
- Las credenciales y URLs están centralizadas en `utils/helpers.py` para fácil mantenimiento.
