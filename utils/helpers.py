"""
utils/helpers.py - Funciones auxiliares reutilizables para los tests de automatización.
Centraliza la lógica repetitiva para mantener los tests limpios y legibles.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ──────────────────────────────────────────────
# Constantes del sitio
# ──────────────────────────────────────────────

BASE_URL = "https://www.saucedemo.com"
VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"
INVENTORY_URL = f"{BASE_URL}/inventory.html"


# ──────────────────────────────────────────────
# Funciones de navegación
# ──────────────────────────────────────────────

def navigate_to_login(driver):
    """Navega a la página de login de saucedemo.com."""
    driver.get(BASE_URL)


def perform_login(driver, username=VALID_USERNAME, password=VALID_PASSWORD):
    """
    Realiza el proceso de login con las credenciales indicadas.
    Por defecto usa las credenciales válidas del usuario estándar.
    """
    navigate_to_login(driver)

    wait = WebDriverWait(driver, 10)
    username_field = wait.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    username_field.clear()
    username_field.send_keys(username)

    password_field = driver.find_element(By.ID, "password")
    password_field.clear()
    password_field.send_keys(password)

    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()


# ──────────────────────────────────────────────
# Funciones de espera explícita
# ──────────────────────────────────────────────

def wait_for_url_contains(driver, partial_url, timeout=10):
    """
    Espera explícita hasta que la URL actual contenga el fragmento indicado.
    Lanza TimeoutException si no se cumple dentro del tiempo límite.
    """
    WebDriverWait(driver, timeout).until(
        EC.url_contains(partial_url)
    )


def wait_for_element_visible(driver, by, locator, timeout=10):
    """
    Espera explícita hasta que un elemento sea visible en el DOM.
    Retorna el elemento una vez visible.
    """
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, locator))
    )


def wait_for_elements_present(driver, by, locator, timeout=10):
    """
    Espera explícita hasta que al menos un elemento con el locator dado esté presente.
    Retorna la lista de elementos encontrados.
    """
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((by, locator))
    )


# ──────────────────────────────────────────────
# Funciones del inventario
# ──────────────────────────────────────────────

def get_product_elements(driver):
    """
    Retorna la lista de elementos de producto en la página de inventario.
    Requiere que el driver ya esté en /inventory.html.
    """
    return driver.find_elements(By.CLASS_NAME, "inventory_item")


def get_first_product_info(driver):
    """
    Obtiene el nombre y precio del primer producto listado en el inventario.
    Retorna un diccionario con claves 'nombre' y 'precio'.
    """
    products = get_product_elements(driver)
    if not products:
        return None

    first_product = products[0]
    nombre = first_product.find_element(By.CLASS_NAME, "inventory_item_name").text
    precio = first_product.find_element(By.CLASS_NAME, "inventory_item_price").text

    return {"nombre": nombre, "precio": precio}


# ──────────────────────────────────────────────
# Funciones del carrito
# ──────────────────────────────────────────────

def add_first_product_to_cart(driver):
    """
    Hace clic en el botón 'Add to cart' del primer producto del inventario.
    Retorna el nombre del producto agregado.
    """
    products = get_product_elements(driver)
    first_product = products[0]

    product_name = first_product.find_element(By.CLASS_NAME, "inventory_item_name").text
    add_button = first_product.find_element(By.TAG_NAME, "button")
    add_button.click()

    # Espera explícita a que el badge del carrito aparezca tras el clic
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )

    return product_name


def get_cart_item_count(driver):
    """
    Retorna el número de ítems en el carrito según el badge del ícono.
    Retorna 0 si el badge no está visible (carrito vacío).
    """
    badges = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    if badges:
        return int(badges[0].text)
    return 0


def navigate_to_cart(driver):
    """Hace clic en el ícono del carrito para navegar a la página de carrito."""
    cart_icon = wait_for_element_visible(driver, By.CLASS_NAME, "shopping_cart_link")
    cart_icon.click()