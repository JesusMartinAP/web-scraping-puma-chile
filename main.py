from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def main():
    # 1. Pedir el código por consola
    codigo = input("Ingresa el código del producto (por ejemplo 107943+01): ")

    # 2. Construir la URL
    base_url = "https://cl.puma.com/search?q="
    url_completa = base_url + codigo
    
    # 3. Iniciar el navegador con Selenium
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url_completa)

    # 4. Extraer los datos:  
    #    a) Nombre del primer producto
    #    b) Precio del primer producto
    
    try:
        # Asegúrate de que el contenido de la página cargue antes de buscar los elementos
        # (puedes usar time.sleep(2) o WebDriverWait si deseas mayor robustez)
        
        # Primer recuadro
        primer_recuadro_xpath = '//*[@id="sgmfs-content"]/div[5]/div/div[1]'
        
        # Verificamos que exista
        primer_recuadro = driver.find_element(By.XPATH, primer_recuadro_xpath)

        # Nombre del producto
        nombre_xpath = '//*[@id="sgmfs-content"]/div[5]/div/div[1]/div/div[2]/div[2]/div[1]/a'
        nombre_producto = driver.find_element(By.XPATH, nombre_xpath).text

        # Precio del producto
        precio_xpath = '//*[@id="sgmfs-content"]/div[5]/div/div[1]/div/div[2]/div[2]/div[2]/div'
        precio_producto = driver.find_element(By.XPATH, precio_xpath).text

        # 5. Imprimir en pantalla
        print(f"Código ingresado: {codigo}")
        print(f"Nombre del producto: {nombre_producto}")
        print(f"Precio del producto: {precio_producto}")
        
    except Exception as e:
        print("Ocurrió un error al extraer la información:", e)
    finally:
        # Cerrar el navegador
        driver.quit()

if __name__ == "__main__":
    main()
