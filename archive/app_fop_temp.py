from flask import Flask, jsonify, request, make_response,render_template, send_file
from selenium import webdriver
import threading
import time
import json
app = Flask(__name__)
import re
def has_non_digit(inputString):
    return bool(re.search(r'\D', inputString))


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import warnings
warnings.filterwarnings('ignore')
import time
import os
# get the current working directory
current_working_directory = os.getcwd()
from bs4 import BeautifulSoup
global port,login,password
port= 5050


# Global variables
last_scrape_time = None
is_scrapping_in_progress=False


# Your profile path
profile_directory = current_working_directory  +  "/profile_dir"  # Change this to your directory path
if not os.path.exists(profile_directory):
    os.makedirs(profile_directory)

def start_browser():
    global driver
    
    # Set up Chrome options
    chrome_options = Options()

    # Disable JavaScript completely
    chrome_options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.javascript": 2
    })

    # Enable Incognito mode
    chrome_options.add_argument("--incognito")

    # Additional options for a more 'IE-like' experience
    chrome_options.add_argument("--disable-extensions")  # Disables all extensions
    chrome_options.add_argument("--disable-popup-blocking")  # Disables the popup blocker
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration
    chrome_options.add_argument("--no-sandbox")  # Disables the sandbox for the Chrome process
    #chrome_options.add_argument("--headless")

 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)


# This function keeps the browser session alive
def keep_browser_session_alive():
    global driver,is_scrapping_in_progress
    while True:

        time.sleep(3600)
        is_scrapping_in_progress=True  
        driver.close()
        start_browser()
        is_scrapping_in_progress=False
        


@app.route('/scrape', methods=['GET'])
def scrape_data():
    global driver, is_scrapping_in_progress, last_scrape_time
    if is_scrapping_in_progress:
        return jsonify({'Error':'Scrapping in progress'}), 503
    is_scrapping_in_progress=True
    # Get parameters from the GET request
    id = str(request.args.get('id'))
    if len(id)!=10 or has_non_digit(id):
        is_scrapping_in_progress=False
        return jsonify({'Error': 'Invalid length or symbol'}), 400
  


    current_time = time.time()
    # If last_scrape_time is set, calculate the difference
    if last_scrape_time is not None:
        time_since_last_scrape = current_time - last_scrape_time

        # If it's less than 8 seconds since the last scrape, wait the remainder
        if time_since_last_scrape < 8:
            time.sleep(8 - time_since_last_scrape)


    url = f'https://opendatabot.ua/check-fop/{id}'  
    driver.get(url)
      
    try:

        
        
        
        


        try:
            WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, '//p[@class="lead"]')))
            last_scrape_time = time.time()
            is_scrapping_in_progress=False
            return jsonify({'Error': 'Id was not found'}), 404
        
        except:
            try:
                WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, '//button[@class="purchase-button btn btn-primary btn-lg m-1"]')))
            except:
                driver.close()
                start_browser()
                last_scrape_time = time.time()
                is_scrapping_in_progress=False
                return jsonify({'Error': 'Opendatabot is not avalible'}), 504 




        # try:
        #     WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-lg btn-primary"]')))
        # except:
        #     try:
        #         WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH, '//p[@class="lead"]')))
        #         last_scrape_time = time.time()
        #         is_scrapping_in_progress=False
        #         return jsonify({'Error': 'Id was not found'}), 404
                
        #     except:
        #         last_scrape_time = time.time()
        #         is_scrapping_in_progress=False
        #         return jsonify({'Error': 'Opendatabot is not avalible'}), 504 

        






        screen_boolean=str(request.args.get('screen'))
        if screen_boolean=='True' or screen_boolean=='1':


            
            


            def take_full_page_screenshot(driver=driver, filename="./static/screen.png"):
                # Store the original size
                original_size = driver.get_window_size()

                # Calculate total height of the page
                total_height = driver.execute_script("return document.body.parentNode.scrollHeight")

                # Resize window to capture the full page
                driver.set_window_size(1920, total_height)

                # Take a screenshot
                driver.save_screenshot(filename)

                # Revert to the original window size
                driver.set_window_size(original_size['width'], original_size['height'])

                # Scroll to the top
                driver.execute_script("window.scrollTo(0,0);")
            take_full_page_screenshot()
            last_scrape_time = time.time()
        
            is_scrapping_in_progress=False


            screen_boolean=str(request.args.get('download'))
            if screen_boolean=='True' or screen_boolean=='1':
                return send_file('./static/screen.png', mimetype='image/png',as_attachment=True)
            


            return render_template("index.html", image_url='./static/screen.png')
            
            






        # Get the HTML content of the page
        soup = BeautifulSoup(driver.page_source, 'html.parser')



        
        try:
            name = soup.find(text='ПІБ').find_next('p').text
        except:
            name = soup.find(text='ПІБ').find_next('div').text
        

        try:
            vat = soup.find('span',text=re.compile('Єдиний податок')).text
        except:
            vat = None

        try:
            VAT_certificate = soup.find(text='Анульоване свідоцтво ПДВ').find_next('p').text
        except:
            try:
                VAT_certificate = soup.find(text='Платник ПДВ').find_next('p').text
            except:
                VAT_certificate = None

        try:
            debt = soup.find(text='Податковий борг').find_next('p').text
        except:
            debt = None

        try:
            address = soup.find(text='Адреса').find_next('p').text
        except:
            address = soup.find(text='Адреса').find_next('div').text
        

       
        try:
            status = soup.find(text='Статус').find_next('div').text
            if 'вид' in status:
                status = soup.find(text='Статус').find_next('p').text
        except:
            status = soup.find(text='Статус').find_next('p').text
       
           

        
        data={'id':id, 
                       'name':name,
                        'address':address, 
                        'status':status,
                        'vat':vat
                        ,'VAT_certificate':VAT_certificate
                        ,'debt':debt}
        


        # Use json.dumps to convert the dictionary to a JSON string with indentation
        json_str = json.dumps(data, ensure_ascii=False, indent=4)
        # Use jsonify to create a response object from the JSON string
        response = make_response(json_str)
        # Set the content-type to 'application/json'
        response.mimetype = 'application/json'




        current_time = time.time()
        # If last_scrape_time is set, calculate the difference
        if last_scrape_time is not None:
            time_since_last_scrape = current_time - last_scrape_time

            # If it's less than 8 seconds since the last scrape, wait the remainder
            if time_since_last_scrape < 20:
                time.sleep(20 - time_since_last_scrape)



        last_scrape_time = time.time()
        
        is_scrapping_in_progress=False
        return response



    except:
        driver.save_screenshot('./problem_fop.png')
        last_scrape_time = time.time()
        is_scrapping_in_progress=False
        
        return jsonify({'Error': 'Try again, error on API side'}), 500

if __name__ == '__main__':
    start_browser()
    # Start the thread that keeps the browser session alive
    threading.Thread(target=keep_browser_session_alive, daemon=True).start()
    app.run(host='0.0.0.0', port=port,use_reloader=False,debug=False)
