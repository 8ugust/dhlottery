from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from configparser import ConfigParser
from selenium import webdriver
import datetime
import time

# =================== =================== =================== ===================
# =================== =================== =================== ===================
# =================== =================== ===================
# Set Selenium Options
# =================== =================== ===================

chrome_options = Options()
# chrome_options.add_argument("headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--log-level=3')
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument('--blink-settings=imagesEnabled=false')

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"

driver = webdriver.Chrome(options=chrome_options)
driver.get(url='https://www.dhlottery.co.kr/user.do?method=login&returnUrl=')





# =================== =================== ===================
# Login
# =================== =================== ===================
wait = WebDriverWait(driver, 5)
login_form = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'form')))
form_pw = wait.until(EC.visibility_of_element_located((By.NAME, 'password')))
form_id = wait.until(EC.visibility_of_element_located((By.NAME, 'userId')))
button = login_form.find_element(By.TAG_NAME, 'a')

config = ConfigParser()
config.read('./conf.ini')
id = config['lottery']['id']
pw = config['lottery']['pw']

form_id.send_keys(id)
form_pw.send_keys(pw)
button.click()
time.sleep(1)





# =================== =================== ===================
# Close Popup
# =================== =================== ===================
parent = driver.current_window_handle
uselessWindows = driver.window_handles
for window in uselessWindows:
    if window != parent:
        driver.switch_to.window(window)
        driver.close()

driver.switch_to.window(parent)




# =================== =================== ===================
# Check Remain Money
# =================== =================== ===================
# cMoney = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'money')))
# money = cMoney.find_element(By.TAG_NAME, 'strong')






        

driver.get(url='https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LO40')





# =================== =================== ===================
# Change Iframe
# =================== =================== ===================
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
nums = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'nums')))
spans = nums.find_elements(By.TAG_NAME, 'span')

number = '[Log][' + now + '] Number : '
for span in spans:
    print(span.get_attribute('innerHTML'))
    number += span.get_attribute('innerHTML') + "\t"

print(number)