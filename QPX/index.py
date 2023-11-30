#ACTIVIDAD A REALIZAR
#Se dispone de un documento de excel que contiene el nombre de 10 países. 
#El bot debe buscar en Google la capital de cada uno de los países y escribir el resultado de la consulta en el excel.
#Requisitos 
#-Leer el nombre del país del archivo de excel 
#-Consultar la capital del país en Google 
#-Extraer el resultado de Google y almacenarlo en la columna “Capital” 
#-El archivo original debe permanecer sin modificaciones 
#-Los resultados deben quedar registrados en un nuevo archivo de excel 
#-En caso que no aparezca la capital indicar resultado como “No encontrado”



#IMPORTAMOS LAS LIBRERIAS QUE VAMOS A NECESITAR
import pandas as pd
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec

#CREAMOS UN DATAFRAME Y UTILIZANDO PANDAS LO LEEMOS COMO FORMATO XLSX
df = pd.read_excel("paises.xlsx")

#CREAMOS UNA NUEVA COLUMNA PARA ALMACENAR LOS RESULTADOS DE LAS BUSQUEDAS
df["Capital"] = ""

#CON EL WEBDRIVER ABRIMOS EL NAVEGADOR CHROME
driver = wd.Chrome()

#NAVEGAR EN GOOGLE
driver.get("https://www.google.com")

#FUNCIÓN PARA MAXIMIZAR LA PANTALLA
driver.maximize_window()


#ITERACIONES DE TODOS LOS PAISES PRESENTES EN EL EXCEL
for index, row in df.iterrows():

    #ENCONTRAR LA CAPITAL DEL PAIS
    input_busqueda = driver.find_element(By.NAME, "q")

    #ELIMINAR EL CONTENIDO DE LA BARRA DE BUSQUEDAD
    input_busqueda.clear()

    #REALIZAR LA OTRA CONSULTA
    input_busqueda.send_keys("capital de " + row["País"])#AL IR ITERANDO PODEMOS UTILIZAR EL MISMO STRING Y SOLO CAMBIARARÁ EL PAIS    
    
    #BUSCAR
    input_busqueda.submit()
    
    #XPATH DEL ELEMENTO AL CUAL QUEREMOS CONSEGUIR LA INFORMACIÓN
    resultado_busqueda = "//*[@id='rso']/div[1]/div/block-component/div/div[1]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/a"

    #ESPERAR QUE EL ELEMENTO CON EL XPATH SE CARGUE AL COMPLETO
    try:
        wdw(driver, 3).until(ec.visibility_of_element_located((By.XPATH, resultado_busqueda)))
        capital = driver.find_element(By.XPATH, resultado_busqueda).text
    except:
        capital = "No encontrado"

    #COLOCAR LA INFORMACIÓN OBTENIDA A LA COLUMNA DE CAPITAL
    df.loc[index, "Capital"] = capital

#NUEVO EXCEL CON PAISES Y CAPITALES
df.to_excel("paises_con_capitales.xlsx")
