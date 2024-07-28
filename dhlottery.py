from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from configparser import ConfigParser
from selenium import webdriver
from PIL import Image
import pytesseract
import datetime
import requests
import time
import re
import io


# =================== =================== =================== ===================
# =================== =================== =================== ===================
# =================== =================== ===================
# Set Selenium Options
# =================== =================== ===================

chrome_options = Options()
chrome_options.add_argument("headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--log-level=3')
chrome_options.add_experimental_option("detach", True)

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"

driver = webdriver.Chrome(options=chrome_options)
driver.get(url='https://dhlottery.co.kr/user.do?method=login&returnUrl=/payment.do?method=payment&returnFlag=N')





# =================== =================== ===================
# Login
# =================== =================== ===================
wait = WebDriverWait(driver, 10)
login_form = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'form')))
form_pw = wait.until(EC.visibility_of_element_located((By.NAME, 'password')))
form_id = wait.until(EC.visibility_of_element_located((By.NAME, 'userId')))
button = login_form.find_element(By.TAG_NAME, 'a')

config = ConfigParser()
config.read('./conf.ini')
id = config['lottery']['id']
pw = config['lottery']['pw']
fa = config['lottery']['fa']

form_id.send_keys(id)
form_pw.send_keys(pw)
button.click()
time.sleep(1)





# =================== =================== ===================
# Close Popup
# Deprecated : Not Used in Payment Method View.
# =================== =================== ===================
# parent = driver.current_window_handle
# uselessWindows = driver.window_handles
# for window in uselessWindows:
#     if window != parent:
#         driver.switch_to.window(window)
#         driver.close()
# driver.switch_to.window(parent)





# =================== =================== ===================
# Check Remain Money
# =================== =================== ===================
cMoney = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'money')))
money = cMoney.find_element(By.TAG_NAME, 'strong').get_attribute('innerHTML')
money = money.replace(',', '').replace('원', '')

if money == "32000":
    Select(wait.until(EC.visibility_of_element_located((By.ID, 'EcAmt')))).select_by_value('5000')
    btnWrap = wait.until(EC.visibility_of_element_located((By.ID, 'btn2')))
    btn = btnWrap.find_element(By.TAG_NAME, 'button')
    btn.click()
    time.sleep(1)

    # Switch Current Window to Popup
    parent = driver.current_window_handle
    for window in driver.window_handles:
        if window != parent:
            driver.switch_to.window(window)

    # Get Password Keypad Image
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\gks83\AppData\Local\tesseract.exe'
    kpdImg = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'kpd-image-button')))
    keypad = wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, 'kpd-data')))
    response = requests.get(kpdImg.get_attribute('src'))
    img = Image.open(io.BytesIO(response.content))

    # Keypad to Array
    txt = pytesseract.image_to_string(img, config='--psm 6')
    txtArr = re.findall(r'\d', txt)
    numbers = sorted(set(txtArr), key=txtArr.index)

    keypad = list(filter(lambda pad: pad.get_attribute('data-action').split(":")[0] == 'data', keypad))
    for factor in fa:
        for idx, num in enumerate(numbers):
            if factor == num:
                keypad[idx].click()
    
    time.sleep(1)
    Alert(driver).accept()
    driver.switch_to.window(parent)





# =================== =================== ===================
# Change Iframe
# =================== =================== ===================
driver.get(url='https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LO40')
iframe = wait.until(EC.visibility_of_element_located((By.ID, 'ifrm_tab')))
driver.switch_to.frame(iframe)





# =================== =================== ===================
# Auto Check & Buy Game
# =================== =================== ===================
ticket  = wait.until(EC.visibility_of_element_located((By.ID, 'divWay2Buy1')))
setNum  = wait.until(EC.visibility_of_element_located((By.ID, 'btnSelectNum')))
buyBtn  = wait.until(EC.visibility_of_element_located((By.ID, 'btnBuy')))
btnWrap = ticket.find_element(By.CLASS_NAME, 'action')
label = btnWrap.find_element(By.TAG_NAME, 'label')

label.click()
setNum.click()
buyBtn.click()

confirm = wait.until(EC.visibility_of_element_located((By.ID, 'popupLayerConfirm')))
confirm.find_elements(By.TAG_NAME, 'input')[0].click()





# =================== =================== ===================
# Record Lotto Number
# =================== =================== ===================
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
report = wait.until(EC.visibility_of_element_located((By.ID, 'reportRow')))
spans = report.find_element(By.CLASS_NAME, 'nums').find_elements(By.TAG_NAME, 'span')

number = '[Log][' + now + '] Number : '
for span in spans:
    print(span.get_attribute('innerHTML'))
    number += span.get_attribute('innerHTML') + " "

print(number)