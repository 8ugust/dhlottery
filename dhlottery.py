from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

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
form_pw.send_keys('')
form_id.send_keys('')
button.click()
time.sleep(1)






# =================== =================== ===================
# Close Popup & Open Lotto Game
# =================== =================== ===================
parent = driver.current_window_handle
uselessWindows = driver.window_handles
for window in uselessWindows:
    if window != parent:
        driver.switch_to.window(window)
        driver.close()
        
driver.switch_to.window(parent)
driver.get(url='https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LO40')





# =================== =================== ===================
# Change Iframe
# =================== =================== ===================



