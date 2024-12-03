import random
import time
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

TICKET_URL = 'https://www.ticketmaster.ie/fontaines-dc-dublin-06-12-2024/event/1800608AAFFF287C'

def check_tickets(driver):
    try:
        driver.get(TICKET_URL)
        random_sleep(3, 6)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        random_sleep(1, 3)
        driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")
        random_sleep(1, 2)

        wait = WebDriverWait(driver, 3)

        standing_elements = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//dd[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'standing')]"))
        )

        if standing_elements:
            return True

    except TimeoutException:
        print("Nothing found.")
    except NoSuchElementException:
        print("Nothing found.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

    return False

def open_link():
    webbrowser.open(TICKET_URL)

def random_sleep(min_seconds, max_seconds):
    sleep_time = random.uniform(min_seconds, max_seconds)
    time.sleep(sleep_time)

def main():
    print("Beginning hunt!")

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        while True:
            print("Hunting for standing tickets...")
            if check_tickets(driver):
                print("Standing tickets found!")
                open_link()
            else:
                print("No standing tickets available. We'll get them next time...")

            random_sleep(60, 90)
    finally:
        driver.quit()  

if __name__ == "__main__":
    main()
