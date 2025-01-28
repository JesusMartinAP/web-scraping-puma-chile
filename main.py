from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def main():
    # 1. Pedir el código por consola
    codigo = input("Ingresa el código del producto (por ejemplo '107931 01'): ")

    # 2. Reemplazar el espacio por '+'
    #    "107931 01" -> "107931+01"
    codigo_formateado = codigo.replace(" ", "+")

    # Concatenar con la URL base
    base_url = "https://cl.puma.com/search?q="
    url_completa = base_url + codigo_formateado
    print(f"Buscando en: {url_completa}")

    # 3. Inicializar Chrome con webdriver_manager y la clase Service
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url_completa)

    # 4. Extraer la información
    # Esperamos un poco para que cargue el contenido
    time.sleep(3)

    try:
        # XPaths de los elementos que quieres extraer
        # Recuadro principal
        primer_recuadro_xpath = '//*[@id="sgmfs-content"]/div[5]/div/div[1]'

        # Nombre del producto
        nombre_xpath = '//*[@id="sgmfs-content"]/div[5]/div/div[1]/div/div[2]/div[2]/div[1]/a'
        
        # Precio del producto
        precio_xpath = '//*[@id="sgmfs-content"]/div[5]/div/div[1]/div/div[2]/div[2]/div[2]/div'
        
        # Verificar que el primer recuadro exista (aunque no siempre es obligatorio)
        primer_recuadro = driver.find_element(By.XPATH, primer_recuadro_xpath)

        nombre_producto = driver.find_element(By.XPATH, nombre_xpath).text
        precio_producto = driver.find_element(By.XPATH, precio_xpath).text

        # 5. Imprimir resultados
        print(f"\nCódigo ingresado: {codigo}")
        print(f"Nombre del producto: {nombre_producto}")
        print(f"Precio del producto: {precio_producto}")

    except Exception as e:
        print("Ocurrió un error al extraer la información:", e)
    finally:
        # Cerrar el navegador
        driver.quit()

if __name__ == "__main__":
    main()
