import mysql.connector
from selenium import webdriver
import os
from time import sleep

debug = True
project = 'betfury'

options = webdriver.ChromeOptions()
options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')

# prevent detection
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--ignore-certificate-errors')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36')

prefs = {'profile.default_content_setting_values.notifications': 2}
options.add_experimental_option('prefs', prefs)

browser = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), options=options)

browser.get('https://betfury.io/staking')
browser.implicitly_wait(10)
sleep(20)

popup_close_button = browser.find_elements_by_class_name('popup-btn-close')
if popup_close_button:
    popup_close_button[0].click()   

btc_pot_value = browser.find_element_by_xpath('//*[@id="app"]/div[3]/div[2]/div[1]/div/div[1]/ul/li[1]/div/ul/li[1]/div[1]').text
eth_pot_value = browser.find_element_by_xpath('//*[@id="app"]/div[3]/div[2]/div[1]/div/div[1]/ul/li[1]/div/ul/li[2]/span').text
bnb_pot_value = browser.find_element_by_xpath('//*[@id="app"]/div[3]/div[2]/div[1]/div/div[1]/ul/li[1]/div/ul/li[3]/span').text
trx_pot_value = browser.find_element_by_xpath('//*[@id="app"]/div[3]/div[2]/div[1]/div/div[1]/ul/li[1]/div/ul/li[4]/span').text
usdt_pot_value = browser.find_element_by_xpath('//*[@id="app"]/div[3]/div[2]/div[1]/div/div[1]/ul/li[1]/div/ul/li[5]/span').text
btt_pot_value = browser.find_element_by_xpath('//*[@id="app"]/div[3]/div[2]/div[1]/div/div[1]/ul/li[1]/div/ul/li[6]/span').text

btc_pot_value = btc_pot_value.replace("BTC", "")
eth_pot_value = eth_pot_value.replace("ETH", "")
bnb_pot_value = bnb_pot_value.replace("BNB", "") 
trx_pot_value = trx_pot_value.replace("TRX", "")
trx_pot_value = trx_pot_value.replace(" ", "")
usdt_pot_value = usdt_pot_value.replace("USDT", "")
usdt_pot_value = usdt_pot_value.replace(" ", "")
btt_pot_value = btt_pot_value.replace("BTT", "")
btt_pot_value = btt_pot_value.replace(" ", "")

mydb = mysql.connector.connect(
    host=os.environ.get('DB_HOST'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASS'),
    database=os.environ.get('DB')
)

mycursor = mydb.cursor()

sql = 'INSERT INTO ' + project + ' (btc_pot, eth_pot, bnb_pot, trx_pot, usdt_pot, btt_pot) VALUES (%s, %s, %s, %s, %s, %s)'
val = (btc_pot_value, eth_pot_value, bnb_pot_value, trx_pot_value, usdt_pot_value, btt_pot_value)
mycursor.execute(sql, val)
mydb.commit()
            
if debug:
    print(mycursor.rowcount, 'record inserted.')
    print(btc_pot_value)
    print(eth_pot_value)
    print(bnb_pot_value)
    print(trx_pot_value)
    print(usdt_pot_value)
    print(btt_pot_value)

mycursor.close()
mydb.close()
browser.quit()