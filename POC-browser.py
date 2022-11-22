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
parser.add_argument("--payment", help="payment : visa, klarna...", type=str, required=True)

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
    order(driver,args.env, args.site, args.delivery, args.payment, "moncefsbay@yopmail.com")


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
        driver.get('https://Storefront_EU_DEV:C5LWDKgI@shop-' + site + '-dev.lacoste.com/')

    elif environment == "STG":
        driver.get('https://Storefront_EU_STAGING:8Lfc5nMj@shop-' + site + '-staging.lacoste.com/')

    elif environment == "PROD":
        driver.get('https://www.lacoste.com/' + site )

    driver.maximize_window()
    consent = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button")))
    consent.click()
    if site != "nl":
        #poursuivre = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div/div[2]/div/div/div/button")))
        try:
            poursuivre = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//button[@class=\"js-geolocation-stay reverse-link\"]")))
            poursuivre.click()
        except:
            time.sleep(1)



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
    WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//ul[@id=\"main-menu\"]/li[3]/button"))).click()

    #polos = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//a[text()="Polos"]')))
    #polos = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//div[@class=\"header-submenu-level2-inner\"]/a[2]")
    #polos = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//li[@class=\"padding-mt-1\"]/div/div/a[2]")
    polos = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"/html/body/ul[2]/li[2]/div/div[2]/ul/li[2]/div/div/a[2]")))

    waitMainLoader(driver) 
    #ActionChains(driver).move_to_element(polos).click(polos).perform()
    polos.click()
    #driver.execute_script("arguments[0].click();", polos)

    sortFilter = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//span[@class="js-plp-filter-btn-label plp-filter-btn-label fs--medium ff-normal"]')))
    sortFilter.click()

    #color = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//*[@id=\"ada-filter-searchColorID\"]/div/li[1]/label")
    colorFilter = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//*[@id=\"ada-filter-searchColorID\"]/div/li[1]/label')))
    colorFilter.click()


    waitMainLoader(driver) 

    size = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"ada-filter-size\"]/div/li[4]/label")))
    size.click()

    waitMainLoader(driver)
    time.sleep(2)

    #filter = driver.find_element(By.XPATH,"//button[@class=\"btn-cta js-popin-close js-plp-filters-submit text-white fs--medium ff-normal \"]")
    filter = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//div[@class=\"bg-grey l-padding--small\"]/div[2]/button[2]")))
    filter.click()


    #l1212 = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//div[@data-sku='3570671739501']/div[3]/a")

    waitMainLoader(driver) 
    l1212 = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"/html/body/main/section/header/div[1]")))
    l1212.click()
    #ActionChains(driver).move_to_element(l1212).click(l1212).perform()
    #except:
    #driver.close()

    time.sleep(3)

    #sizesL1212 = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"/html/body/main/section/article/div[2]/div[4]/div/div[1]/button")
    sizesL1212 = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/article/div[2]/div[4]/div/div[1]/button")))
    sizesL1212.click()


    #selectM = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//button[text()=\"4 - M\"]")
    selectM = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//button[text()=\"4 - M\"]")))

    selectM.click()


    addToCart = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-tag-id=\"quickPanel.onAddToCart\"]')))
    #addToCart = driver.find_element("xpath","//button[@data-tag-id=\"quickPanel.onAddToCart\"]")
    addToCart.click()


    goTocheckOut = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//*[@id=\"top-minicart\"]/div/a")))
    goTocheckOut.click()

def checkout(driver,delivery,payment,site):
    quantity = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//select[@class=\"select-cta select-cta--small\"]")))
    Select(quantity).select_by_value("4")

    deliveryZipCode = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//input[@id=\"delivery-form-zipCodeOrCity\"]")))
    #ActionChains(driver).move_to_element(deliveryZipCode).click(deliveryZipCode).perform()
    if site == "fr":
        deliveryZipCode.send_keys("75016")
        driver.execute_script("document.getElementById('delivery-form-zipCodeOrCity').value='75016'")
    elif site == "gb":
        deliveryZipCode.send_keys("London")
        driver.execute_script("document.getElementById('delivery-form-zipCodeOrCity').value='London'")
    waitCheckoutLoader(driver)
    time.sleep(2)
    suggestion = driver.find_elements("xpath", "//div[@class=\"suggestion cursor-pointer \"]")

    suggestion[0].click()
    waitCheckoutLoader(driver)

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

    #time.sleep(2)
    waitCheckoutLoader(driver)
    emailSigninSignup = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//label[@for=\"signin_signup-email\"]")))
    emailSigninSignup.click()
    emailSigninSignup = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//input[@id=\"signin_signup-email\"]")))
    emailSigninSignup.send_keys("moncefsbay@gmail.com")

    emailContinue = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//input[@id=\"signin_signup-continue\"]")))
    emailContinue.click()

    waitCheckoutLoader(driver)

    passwordSigninSignup = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//input[@id=\"signin_signup-password\"]")))
    passwordSigninSignup.send_keys("Mesut1234,")

    emailConnect = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//input[@id=\"signin_signup-signin\"]")))
    emailConnect.click()

    #time.sleep(2)
    waitCheckoutLoader(driver)

    time.sleep(2)

    #goToPayment = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//section/div/div/div[1]/div[2]/div[3]/div[3]/input")
    goToPayment = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//section/div/div/div[1]/div[2]/div[3]/div[3]/input")))

    goToPayment.click()

    waitCheckoutLoader(driver)

    paymentMethod = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//div[@class=\"flex flex--basis-full fs--medium flex-mt--col flex--align-center grid text-black\"]")))
    paymentMethod = driver.find_elements("xpath", "//div[@class=\"flex flex--basis-full fs--medium flex-mt--col flex--align-center grid text-black\"]")

    time.sleep(2)
    if payment == "Visa":
        paymentMethod[0].click()
        creditCardNumber = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//input[@id=\"CREDIT_CARD-npm-card-number\"]")))
        #ActionChains(driver).move_to_element(creditCardNumber).click(creditCardNumber).perform()

        driver.execute_script("document.getElementById('CREDIT_CARD-npm-card-number').value='4111111111111111'")
        creditCardNumber.send_keys('4111111111111111')



        time.sleep(1)
        creditCardExp = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//input[@id=\"CREDIT_CARD-cc-exp\"]")))
        #ActionChains(driver).move_to_element(creditCardExp).click(creditCardExp).perform()

        driver.execute_script("document.getElementById('CREDIT_CARD-cc-exp').value='1223'")
        creditCardExp.send_keys('1223')



        time.sleep(1)
        creditCardCVC = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"//input[@id=\"CREDIT_CARD-npm-cryptogramme\"]")))
        #ActionChains(driver).move_to_element(creditCardCVC).click(creditCardCVC).perform()

        driver.execute_script("document.getElementById('CREDIT_CARD-npm-cryptogramme').value='123'")
        creditCardCVC.send_keys('123')


    elif payment == "Klarna":
        paymentMethod[1].click()

    elif payment == "Paypal":
        paymentMethod[2].click()

    time.sleep(3)

def checkemail(driver,email):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("http://yopmail.com")
    emailField = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//input[@class=\"ycptinput\"]")))
    emailField.send_keys(email)
    emailField.send_keys(Keys.ENTER)


def order(driver,environment,site,delivery,payment,email):
    setup(driver,environment, site)
    HomeplpPdp(driver)
    checkout(driver,delivery,payment,site)
    checkemail(driver,email)
