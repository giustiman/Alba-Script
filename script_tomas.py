from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import re
from flask import Flask, jsonify
import threading
import os
from datetime import datetime, timedelta

app = Flask(__name__)

latest_verification_code = None  # Variable para almacenar el último código de verificación

def extract_verification_code(message):
    # Implementa la lógica para extraer el número de verificación del mensaje
    # En este ejemplo, se utiliza una expresión regular para buscar un número de 6 dígitos
    match = re.search(r'\d{6}', message)
    if match:
        return match.group(0)
    return None

def parse_date_time(date_time_str):
    # Reemplazar el carácter \xa0 con un espacio en blanco
    date_time_str = date_time_str.replace('\xa0', '')
    date_time_str = date_time_str.replace('m.', 'm.,')


    # Dividir la cadena en tiempo y fechaz
    time_date_parts = date_time_str.split(',')

    # Obtener la hora y la fecha
    time_str = time_date_parts[0].strip()
    date_str = time_date_parts[1].strip()
    
 # Verificar si "p.m." o "a.m." están presentes y ajustar la hora si es necesario
    if 'p.m.' in time_str:
        time_str = time_str.replace('p.m.', 'PM')
    elif 'a.m.' in time_str:
        time_str = time_str.replace('a.m.', 'AM')

    # Convertir la cadena de fecha y hora en un objeto de fecha y hora
    date_time_obj = datetime.strptime(time_str + ' ' + date_str, "%I:%M %p %d/%m/%Y")
    return date_time_obj

# Definir una ruta en Flask para obtener el último código de verificación
@app.route('/get_latest_code', methods=['GET'])
def get_latest_code():
    global latest_verification_code
    if latest_verification_code:
        return jsonify({'code': latest_verification_code})
    else:
        return jsonify({'code': 'No code available'})

def process_contact_messages(driver, contact_name):
    inp_xpath_search = "//input[@title='Search or start new chat']"
    inp_xpath_search = '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]/p' # <p class="selectable-text copyable-text iq0m558w g0rxnol2"><br></p>
    input_box_search = WebDriverWait(driver, 50).until(lambda driver: driver.find_element(By.XPATH, inp_xpath_search))
    input_box_search.click()
    time.sleep(2)
    input_box_search.send_keys(contact_name)
    time.sleep(2)
    input_box_search.send_keys(Keys.RETURN)
    if contact_name == "2436":
        contact_name = "ComparaOnline Support"
    if contact_name == "4750":
        contact_name = "Verify"
    if contact_name == "6123":
        contact_name = "Verify"
        
    selected_contact = driver.find_element(By.XPATH, "//span[@title='"+contact_name+"']")
    selected_contact.click()

    # Definir el XPath del elemento que deseas extraer
    xpath = '//*[@id="main"]'

    # Encontrar el elemento utilizando el XPath
    elemento = driver.find_element(By.XPATH, xpath)

    # Obtener el HTML del elemento
    elemento_html = elemento.get_attribute('outerHTML')

    # Crear un objeto BeautifulSoup para el HTML del elemento
    soup_elemento = BeautifulSoup(elemento_html, 'html.parser')

    # Encontrar todos los elementos de mensajes dentro del elemento encontrado
    mensajes = soup_elemento.find_all('div', class_=lambda x: x and ('message-out' in x or 'message-in' in x))

    # Inicializar listas para mensajes enviados y recibidos
    mensajes_enviados = []
    mensajes_recibidos = []

    # Recorrer los mensajes y extraer el contenido de texto correctamente
    for mensaje in mensajes:
        mensaje_texto = ''
        for span in mensaje.find_all('span', class_='selectable-text'):
            mensaje_texto += span.get_text() + ' '
        if 'message-in' in mensaje['class']:
            mensajes_recibidos.append(mensaje_texto.strip())
        else:
            mensajes_enviados.append(mensaje_texto.strip())

        # Extract the date and time from the 'data-pre-plain-text' attribute
        date_time = mensaje.find('div', class_='copyable-text').get('data-pre-plain-text')
        print(date_time)

        # Parse the date and time from the string
        date_time = date_time.strip('[]').split(',')[0] + date_time.strip('[]').split(',')[1].split(']')[0]
        if 'm' in date_time:
            date_time_obj = parse_date_time(date_time)
        else:
            date_time = date_time.replace('24:', '00:')
            date_time_obj = datetime.strptime(date_time, "%H:%M %d/%m/%Y")
        

        # Calculate the difference in seconds from the current time
        current_time = datetime.now()
        time_difference = current_time - date_time_obj
        seconds_difference = int(time_difference.total_seconds())

        #print(seconds_difference)

    # Procesar el último mensaje recibido (si lo hay)
    if mensajes_recibidos:
        latest_message_received = mensajes_recibidos[-1]  # Obtener el último mensaje recibido
        verification_code = extract_verification_code(latest_message_received)
        if verification_code:
            latest_verification_code_ = verification_code

    # ... Más código de Selenium aquí ...

    inp_xpath_search = '//*[@id="side"]/div[1]/div/div[2]/span/button'
    input_box_search = WebDriverWait(driver, 5).until(lambda driver: driver.find_element(By.XPATH, inp_xpath_search))
    input_box_search.click()

    return latest_verification_code_, seconds_difference
        
if __name__ == '__main__':
    contact_name = "Verify"  # Cambia esto al nombre del contacto que deseas monitorear
    #contact_name = "+1"  # Cambia esto al nombre del contacto que deseas monitorear

    # Configuración de Selenium
    chrome_options = webdriver.ChromeOptions()
    #chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--proxy-server=http://10.8.0.25:3130")

    chromedriver = "../chromedriver"
    chrome_options.add_argument("--user-data-dir=/home/virtual/bciseguros/core/scrappers/compara/data_whatsapp")
    #chrome_options.add_argument("--user-data-dir=C:/Users/usuario/Desktop/Compara/chrome-data")

    #chrome_options.add_argument('--headless')
    #chrome_options.add_experimental_option("debuggerAddress","localhost:9222");
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("-disable-gpu")
    #chrome_options.add_argument("--incognito")
    #chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.2987.133 Safari/537.36")-----------
    #chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(executable_path=chromedriver, options=chrome_options)
    driver.get("https://web.whatsapp.com")
    print("Scan QR Code, And then Enter")
    for i in range(20):
        try:
            if i > 0:
                print(f"Waiting {i} seconds, press Enter to continue...")
            input()
            break
        except Exception:
            time.sleep(1)
    print("Logged In")

    flask_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 8080})

    # Iniciar el hilo de Flask en segundo plano
    flask_thread.start()
    
    while True:
        try:
            time.sleep(1)
            #latest_verification_code1, seconds_difference1 = process_contact_messages(driver, "4750") # Verify
            #latest_verification_code1, seconds_difference1 = process_contact_messages(driver, "6123") # Verify
            #latest_verification_code1, seconds_difference1 = process_contact_messages(driver, "6123") # Verify
            latest_verification_code2, seconds_difference2 = process_contact_messages(driver, "2436") # ComparaOnline Support
            seconds_difference1 = 10000000
            # Define the global latest_verification_code as the one with the least minutes
            # if seconds_difference1 < seconds_difference2:
            #     latest_verification_code = latest_verification_code1
            # else:
            #     latest_verification_code = latest_verification_code2
            latest_verification_code = latest_verification_code2
            print(latest_verification_code)    
        except:
            print("ERRORRRRR")
            break 
        
        
        

    # Ejecutar Flask en cualquier IP