from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

#Chrome Options
options = webdriver.ChromeOptions()

options.add_experimental_option("excludeSwitches", ["enable-automation"])

options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--window-size=1920,1080")
options.add_argument("start-maximized")
options.add_argument("headless")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)

# Avoid detection
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
"source": """

Object.defineProperty(navigator, 'webdriver', {

get: () => undefined

})

"""

})
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.121 Safari/537.36")




def a():
    driver.get("https://br.1xbet.com/live/football")
    driver.implicitly_wait(10)
    #driver.find_element(By.XPATH, "/html/body/div[5]/div/div[1]").click()
    #driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[2]").click()



    SCROLL_PAUSE_TIME = 0.5

    while False:

        # Get scroll height
        ### This is the difference. Moving this *inside* the loop
        ### means that it checks if scrollTo is still scrolling
        last_height = driver.execute_script("return document.body.scrollHeight")

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:

            # try again (can be removed)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")

            # check if the page height has remained the same
            if new_height == last_height:
                # if so, you are done
                break
            # if not, move on to the next loop
            else:
                last_height = new_height
                continue


    elements = driver.find_elements(By.CLASS_NAME, "c-events-scoreboard__item")
    #links = driver.find_element(By.CSS_SELECTOR, "hm-ProductHeaderNarrow_Container ")
    #teamnames = [t.text for t in teamnames]
    #links.click()
    #time.sleep(600)



    print(len(elements))
    for element in elements:
        print(element.text, '\n\n')
    elements[0].click()
   # elements[0].click()
    time.sleep(600)

a()