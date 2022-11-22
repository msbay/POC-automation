from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from threading import Thread
import time
from selenium.webdriver.support import expected_conditions as EC
import argparse
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

parser = argparse.ArgumentParser(description="POC example",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--env", help="environment : DEV, STG or PROD", type=str, required=True)
parser.add_argument("--site", help="site : fr, uk, us etc...", type=str, required=True)
parser.add_argument("--delivery", help="delivery : standard, express...", type=str, required=True)
#parser.add_argument("--payment", help="payment : visa, klarna...", type=str, required=True)

args = parser.parse_args()


load_dotenv()
BROWSERSTACK_USERNAME = os.environ.get("BROWSERSTACK_USERNAME") or "moncefsbay_hSCru5"
BROWSERSTACK_ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY") or "eoVZjqzY8JMTsGp2Sacc"
URL = os.environ.get("URL") or "https://hub.browserstack.com/wd/hub"
BUILD_NAME = "POC-Moncef"
capabilities = [
    {
        "browserName": "Chrome",
        "browserVersion": "107.0",
        "os": "OS X",
        "osVersion": "Big Sur",
        "sessionName": "Moncef POC Chrome", # test name
        "buildName": BUILD_NAME,  # Your tests will be organized within this build
    },
    # {
    #     "browserName": "Firefox",
    #     "browserVersion": "106.0",
    #     "os": "Windows",
    #     "osVersion": "10",
    #     "sessionName": "Moncef POC FireFox",
    #     "buildName": BUILD_NAME,
    # }
    # {
    #     "browserName": "Safari",
    #     "browserVersion": "14.1",
    #     "os": "OS X",
    #     "osVersion": "Big Sur",
    #     "sessionName": "BStack Python sample parallel",
    #     "buildName": BUILD_NAME,
    # }
]
def get_browser_option(browser):
    switcher = {
        "chrome": ChromeOptions(),
        "firefox": FirefoxOptions(),
        "edge": EdgeOptions(),
        "safari": SafariOptions(),
    }
    return switcher.get(browser, ChromeOptions())
def run_session(cap):
    bstack_options = {
        "osVersion" : cap["osVersion"],
        "buildName" : cap["buildName"],
        "sessionName" : cap["sessionName"],
        "userName": BROWSERSTACK_USERNAME,
        "accessKey": BROWSERSTACK_ACCESS_KEY
    }
    if "os" in cap:
      bstack_options["os"] = cap["os"]
    options = get_browser_option(cap["browserName"].lower())
    if "browserVersion" in cap:
      options.browser_version = cap["browserVersion"]
    options.set_capability('bstack:options', bstack_options)
    driver = webdriver.Remote(
        command_executor=URL,
        options=options)
   # try:
    order(driver,args.env, args.site, args.delivery, "moncefsbay@yopmail.com")


    # except NoSuchElementException:
    #     driver.execute_script(
    #         'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Some elements failed to load"}}')
    # except Exception:
    #     driver.execute_script(
    #         'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Some exception occurred"}}')
    # # Stop the driver
    driver.quit()

for cap in capabilities:
  Thread(target=run_session, args=(cap,)).start()

def setup(driver,environment,site):
    if environment == "DEV":
        driver.get('https://shop-' + site + '-dev.lacoste.com/connect/home')

    elif environment == "STG":
        driver.get('https://shop-' + site + '-staging.lacoste.com/connect/home')

    elif environment == "PROD":
        driver.get('https://www.lacoste.com/' + site +'/connect/home')

    driver.maximize_window()
    login = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//input[@id=\"login-form-login\"]")))
    login.send_keys("001")
    password = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//input[@id=\"login-form-password\"]")))
    password.send_keys("Mhj92hM%Nw")

    connect = WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id=\"login-form-loginStore\"]")))
    connect.click()
    select =WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div/div/section/div/div[4]/label[1]")))
    select.click()



def waitMainLoader(driver):
    try:
        loader = driver.find_elements("xpath", "//div[@class=\"js-main-loader croco-loader popin-wrapper popin--under-header is-opened\"]")
        while loader.__len__()!= 0 :
            #driver.implicitly_wait(2)
            WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH,"//div[@class=\"js-main-loader croco-loader popin-wrapper popin--under-header is-hidden\"]")))
            break
    except:
        time.sleep(1)

def waitPopInLoader(driver):
    loader = driver.find_elements("xpath","//div[@class=\"js-popin-loader croco-loader l-overlay flex flex--centered is-opened\"]")
    while loader.__len__()!= 0 :
        #driver.implicitly_wait(2)
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH,"//div[@class=\"js-popin-loader croco-loader l-overlay flex flex--centered is-hidden\"]")))


def waitCheckoutLoader(driver):
    try:
        loader = driver.find_elements("xpath", "//div[@class=\"overlay flex flex--centered is-visible\"]")
        while loader.__len__()!= 0 :
            #driver.implicitly_wait(2)
            #WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH,"//div[@class=\"overlay flex flex--centered \"]")))
            time.sleep(2)
            loader = driver.find_elements("xpath", "//div[@class=\"overlay flex flex--centered is-visible\"]")
    except:
        time.sleep(2)



def HomeplpPdp(driver):
    #WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//button[@aria-label=\"Homme\"]").click()
    WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"/html/body/main/div/div/section/div/div/div/a[2]/div[2]"))).click()


    categorie = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"/html/body/main/div/div/section/div/div/div[2]/a[2]")))
    categorie.click()

    polos = WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/main/div/div/section/div/div/div[2]/a[3]")))

    polos.click()
    #driver.execute_script("arguments[0].click();", polos)
    L1212 = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"/html/body/main/div/div/section/div/div[3]/div[4]/div[2]")))
    L1212.click()

    size = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//button[@id=\"4\"]")))
    size.click()

    addToCart = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"/html/body/main/div/div/section/div/div[2]/div[8]/p/input")))
    addToCart.click()

    html = driver.find_element(By.TAG_NAME, 'html')
    html.send_keys(Keys.END)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    gotocheckout = WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/main/div/div/div/div/div[3]/div[2]/div[2]/button")))
    gotocheckout.click()

def checkout(driver,delivery,site):
    time.sleep(5)
    quantity = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//select[@class=\"select-cta select-cta--small\"]")))
    Select(quantity).select_by_value("4")

    deliveryZipCode = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//input[@id=\"delivery-form-zipCodeOrCity\"]")))
    #ActionChains(driver).move_to_element(deliveryZipCode).click(deliveryZipCode).perform()
    # if site == "fr":
    #     deliveryZipCode.clear()
    #     deliveryZipCode.send_keys("75016")
    #     driver.execute_script("document.getElementById('delivery-form-zipCodeOrCity').value='75016'")
    # elif site == "gb":
    #     deliveryZipCode.send_keys("London")
    #     driver.execute_script("document.getElementById('delivery-form-zipCodeOrCity').value='London'")


    WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//div[@class=\"flex--basis-full text-black l-padding-around--medium\"]")))
    deliveryMethod = driver.find_elements("xpath", "//div[@class=\"flex--basis-full text-black l-padding-around--medium\"]")

    if delivery == "Express" :
        deliveryMethod[1].click()

    elif delivery == "Standard" :
        deliveryMethod[0].click()


    #deliveryMethod = driver.find_elements("xpath", "//div[@class=\"flex--basis-full text-black l-padding-around--medium\"]")[1].click()
    html = driver.find_element(By.TAG_NAME,'html')
    html.send_keys(Keys.END)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    #validate = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//input[@class=\"btn-cta btn--medium btn--validate l-vmargin--small l-m-fill-width btn--green fs--medium ff-normal\"]")
    validate = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//input[@class=\"btn-cta btn--medium btn--validate l-vmargin--small l-m-fill-width btn--green fs--medium ff-normal\"]")))
    validate.click()


    email = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//input[@id=\"Email-email\"]")))
    email.send_keys("moncefsbay@gmail.com")

    emailSearch = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//input[@id=\"Email-search\"]")))
    emailSearch.click()



    selectClient = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"/html/body/main/div/div/section/div/div/div[1]/div[2]/div[3]/div/div[2]/div[5]/div/button")))
    selectClient.click()

    waitCheckoutLoader(driver)

    time.sleep(2)


    address = WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id=\"create-shipping-address-form-street1\"]")))
    address.send_keys("16 rue de la pompe")

    time.sleep(2)
    WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//div[@class=\"suggestion cursor-pointer \"]")))

    suggestion = driver.find_elements("xpath", "//div[@class=\"suggestion cursor-pointer \"]")

    suggestion[0].click()

    next = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"create-shipping-address-form-addShippingAddress\"]")))
    next.click()

    goToPayment = WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/main/div/div/section/div/div/div[1]/div[2]/div[3]/div[3]/input")))
    goToPayment.click()

    waitCheckoutLoader(driver)

    payInCBR = WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id=\"CBRPayment-pay\"]")))
    payInCBR.click()


    time.sleep(3)

def checkemail(driver,email):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("http://yopmail.com")
    emailField = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//input[@class=\"ycptinput\"]")))
    emailField.send_keys(email)
    emailField.send_keys(Keys.ENTER)


def order(driver,environment,site,delivery,email):
    setup(driver,environment, site)
    HomeplpPdp(driver)
    checkout(driver,delivery,site)
    checkemail(driver,email)
