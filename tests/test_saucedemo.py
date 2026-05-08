"""
tests/test_saucedemo.py - Suite de pruebas automatizadas para saucedemo.com.

Casos de prueba:
    1. test_login_exitoso         - Automatización del flujo de login
    2. test_navegacion_inventario - Validación de la página de inventario
    3. test_agregar_al_carrito    - Flujo de agregar producto al carrito
"""

import pytest
from selenium.webdriver.common.by import By

from utils.helpers import (
    perform_login,
    wait_for_url_contains,
    wait_for_element_visible,
    wait_for_elements_present,
    get_product_elements,
    get_first_product_info,
    add_first_product_to_cart,
    get_cart_item_count,
    navigate_to_cart,
    INVENTORY_URL,
)


# ══════════════════════════════════════════════════════════════════════════════
# TEST 1: Automatización de Login
# ══════════════════════════════════════════════════════════════════════════════

class TestLogin:
    """
    Verifica que el proceso de login con credenciales válidas
    redirige correctamente a la página de inventario.
    """

    def test_login_exitoso(self, driver):
        """
        DADO que el usuario ingresa credenciales válidas (standard_user / secret_sauce),
        CUANDO hace clic en el botón de login,
        ENTONCES debe ser redirigido a /inventory.html y ver el título 'Products'.
        """
        # Paso 1: Realizar login con credenciales válidas
        perform_login(driver)

        # Paso 2: Espera explícita - confirmar redirección a /inventory.html
        wait_for_url_contains(driver, "inventory.html")

        # Paso 3: Validar que la URL contiene el fragmento esperado
        assert "inventory.html" in driver.current_url, (
            f"Se esperaba redirección a /inventory.html, pero la URL actual es: {driver.current_url}"
        )

        # Paso 4: Validar que el título de la página muestra 'Products' o 'Swag Labs'
        page_title = wait_for_element_visible(driver, By.CLASS_NAME, "title")
        assert "Products" in page_title.text or "Swag Labs" in driver.title, (
            f"Título de página inesperado: '{page_title.text}'"
        )

        print(f"\n✅ Login exitoso. URL actual: {driver.current_url}")
        print(f"   Título de la sección: {page_title.text}")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 2: Caso de Prueba de Navegación
# ══════════════════════════════════════════════════════════════════════════════

class TestNavegacion:
    """
    Verifica que la página de inventario carga correctamente
    con título, productos y elementos de interfaz visibles.
    """

    def test_navegacion_inventario(self, driver):
        """
        DADO que el usuario realizó login exitosamente,
        CUANDO está en la página de inventario,
        ENTONCES debe ver el título correcto, al menos un producto,
        y los elementos principales de la interfaz (menú, filtros).
        """
        # Paso 1: Login previo necesario para acceder al inventario
        perform_login(driver)
        wait_for_url_contains(driver, "inventory.html")

        # Paso 2: Validar título de la página de inventario
        page_title = wait_for_element_visible(driver, By.CLASS_NAME, "title")
        assert page_title.text == "Products", (
            f"Título esperado 'Products', obtenido: '{page_title.text}'"
        )
        print(f"\n✅ Título validado: '{page_title.text}'")

        # Paso 3: Validar que existen productos visibles en la página
        products = wait_for_elements_present(driver, By.CLASS_NAME, "inventory_item")
        assert len(products) >= 1, (
            f"Se esperaba al menos 1 producto, se encontraron: {len(products)}"
        )
        print(f"   Productos encontrados: {len(products)}")

        # Paso 4: Obtener y mostrar nombre y precio del primer producto
        first_product = get_first_product_info(driver)
        assert first_product is not None, "No se pudo obtener información del primer producto"
        print(f"   Primer producto → Nombre: '{first_product['nombre']}' | Precio: {first_product['precio']}")

        # Paso 5: Validar presencia del menú hamburguesa
        menu_button = wait_for_element_visible(driver, By.ID, "react-burger-menu-btn")
        assert menu_button.is_displayed(), "El botón de menú no está visible"
        print(f"   Menú hamburguesa: visible ✅")

        # Paso 6: Validar presencia del filtro de ordenamiento
        sort_filter = wait_for_element_visible(driver, By.CLASS_NAME, "product_sort_container")
        assert sort_filter.is_displayed(), "El filtro de productos no está visible"
        print(f"   Filtro de ordenamiento: visible ✅")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 3: Caso de Prueba de Carrito
# ══════════════════════════════════════════════════════════════════════════════

class TestCarrito:
    """
    Verifica el flujo completo de agregar un producto al carrito
    y confirmar que aparece correctamente en la vista del carrito.
    """

    def test_agregar_al_carrito(self, driver):
        """
        DADO que el usuario está en la página de inventario,
        CUANDO agrega el primer producto al carrito,
        ENTONCES el contador del carrito debe incrementarse a 1
        y el producto debe aparecer en la página del carrito.
        """
        # Paso 1: Login para acceder al inventario
        perform_login(driver)
        wait_for_url_contains(driver, "inventory.html")

        # Paso 2: Verificar que el carrito comienza vacío (contador = 0)
        initial_count = get_cart_item_count(driver)
        assert initial_count == 0, (
            f"Se esperaba carrito vacío (0), pero tiene {initial_count} ítems"
        )
        print(f"\n✅ Carrito inicial vacío: {initial_count} ítems")

        # Paso 3: Agregar el primer producto al carrito
        product_name = add_first_product_to_cart(driver)
        print(f"   Producto agregado: '{product_name}'")

        # Paso 4: Verificar que el contador del carrito se incrementó a 1
        updated_count = get_cart_item_count(driver)
        assert updated_count == 1, (
            f"Se esperaba contador = 1, pero el valor es: {updated_count}"
        )
        print(f"   Contador del carrito: {updated_count} ✅")

        # Paso 5: Navegar al carrito de compras
        navigate_to_cart(driver)
        wait_for_url_contains(driver, "cart.html")
        assert "cart.html" in driver.current_url, (
            f"No se redirigió al carrito. URL actual: {driver.current_url}"
        )
        print(f"   Navegación al carrito exitosa: {driver.current_url} ✅")

        # Paso 6: Verificar que el producto agregado aparece en el carrito
        cart_items = wait_for_elements_present(driver, By.CLASS_NAME, "cart_item")
        assert len(cart_items) == 1, (
            f"Se esperaba 1 ítem en el carrito, se encontraron: {len(cart_items)}"
        )

        # Paso 7: Verificar que el nombre del ítem en el carrito coincide
        cart_item_name = cart_items[0].find_element(By.CLASS_NAME, "inventory_item_name").text
        assert cart_item_name == product_name, (
            f"Nombre esperado: '{product_name}', nombre en carrito: '{cart_item_name}'"
        )
        print(f"   Producto en carrito verificado: '{cart_item_name}' ✅")
