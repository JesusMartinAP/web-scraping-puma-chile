from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def main():
    # 1. Pedir el código por consola
    codigo = input("Ingresa el código del producto (por ejemplo '107931 01'): ")

    # 2. Reemplazar el espacio por '+'
    codigo_formateado = codigo.replace(" ", "+")
    url_completa = "https://cl.puma.com/search?q=" + codigo_formateado
    print(f"Buscando en: {url_completa}")

    # 3. Inicializar el navegador
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url_completa)

    # 4. Esperamos un poco que cargue la página
    time.sleep(3)

    try:
        # XPaths
        # Recuadro principal del primer resultado
        primer_recuadro_xpath = '//*[@id="sgmfs-content"]/div[5]/div/div[1]'

        # Nombre del producto
        nombre_xpath = '//*[@id="sgmfs-content"]/div[5]/div/div[1]/div/div[2]/div[2]/div[1]/a'
        
        # Contenedor de precios
        contenedor_precio_xpath = '//*[@id="sgmfs-content"]/div[5]/div/div[1]/div/div[2]/div[2]/div[2]/div'
        
        # Dentro del contenedor, pueden haber dos tipos de precios:
        #  - .//span[contains(@class, 'special-price')] // precio en oferta
        #  - .//span[contains(@class, 'old-price')]     // precio normal cuando hay oferta
        #  - Si no hay oferta, se suele mostrar un solo precio.

        # Verificar que el primer recuadro exista
        primer_recuadro = driver.find_element(By.XPATH, primer_recuadro_xpath)
        
        # Obtener nombre de producto
        nombre_producto = driver.find_element(By.XPATH, nombre_xpath).text
        
        # Contenedor de precios
        contenedor_precio = driver.find_element(By.XPATH, contenedor_precio_xpath)

        # Intentar obtener precio de oferta (special-price)
        try:
            precio_oferta_element = contenedor_precio.find_element(
                By.XPATH, './/span[contains(@class,"special-price")]//span[@class="price"]'
            )
            precio_oferta = precio_oferta_element.text
        except:
            precio_oferta = None

        # Intentar obtener precio normal (old-price) cuando hay oferta
        try:
            precio_normal_descuento_element = contenedor_precio.find_element(
                By.XPATH, './/span[contains(@class,"old-price")]//span[@class="price"]'
            )
            precio_normal_descuento = precio_normal_descuento_element.text
        except:
            precio_normal_descuento = None

        # Si no existe precio_oferta, significa que no hay descuento,
        # entonces tomamos el precio normal principal (sin oferta)
        if not precio_oferta:
            # Buscar el precio normal (sin oferta)
            precio_normal_sin_oferta_element = contenedor_precio.find_element(
                By.XPATH, './/span[@class="price"]'
            )
            precio_normal_sin_oferta = precio_normal_sin_oferta_element.text
        else:
            precio_normal_sin_oferta = None

        # Imprimir resultados
        print(f"\nCódigo ingresado: {codigo}")
        print(f"Nombre del producto: {nombre_producto}")
        
        # Si existe oferta (precio_oferta) y old_price (precio_normal_descuento)
        if precio_oferta and precio_normal_descuento:
            print(f"Precio con descuento: {precio_oferta}")
            print(f"Precio normal anterior: {precio_normal_descuento}")
        else:
            # Si no hay oferta, imprimimos el normal sin oferta
            print(f"Precio: {precio_normal_sin_oferta}")

    except Exception as e:
        print("Ocurrió un error al extraer la información:", e)
    finally:
        # Cerrar el navegador
        driver.quit()

if __name__ == "__main__":
    main()
