import random
import time
import smtplib
import os
import platform
from email.message import EmailMessage

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

TICKET_URL = "https://www.ticketmaster.ie/fontaines-dc-dublin-06-12-2024/event/1800608AAFFF287C"
FIRST_RUN_MARKER = ".first_run_complete"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-app-password-here"  # Gmail App Password, NOT regular password
RECIPIENT_EMAIL = "your-email@gmail.com"


def send_email(subject="Tickets available!", body=None):
    if body is None:
        body = f"Standing or General Admission tickets were found!\n\nGet them here:\n{TICKET_URL}\n"
    
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL

    msg.set_content(body)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"Email sent successfully! Subject: {subject}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def send_test_email():
    print("Sending test email to confirm configuration...")
    
    test_subject = "Ticket Monitor - Test Email"
    test_body = (
        "This is a test email from your ticket monitoring script.\n\n"
        "If you receive this email, your email configuration is working correctly!\n\n"
        f"Monitoring URL: {TICKET_URL}\n"
        f"Recipient: {RECIPIENT_EMAIL}\n\n"
        "The script will now begin monitoring for tickets."
    )
    
    success = send_email(subject=test_subject, body=test_body)

    if success:
        with open(FIRST_RUN_MARKER, 'w') as f:
            f.write(str(time.time()))
        print("✅ Test email sent successfully! Email configuration is working.")
        return True
    else:
        print("❌ Test email failed. Please check your email configuration.")
        return False


def is_first_run():
    return not os.path.exists(FIRST_RUN_MARKER)


def check_tickets(driver):
    try:
        driver.get(TICKET_URL)
        random_sleep(1, 3)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        random_sleep(1, 2)
        driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")
        random_sleep(1, 2)

        wait = WebDriverWait(driver, 3)

        standing_elements = driver.find_elements(
            By.XPATH,
            "//dd[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'standing')]"
        )

        general_admission_elements = driver.find_elements(
            By.XPATH,
            "//dd[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'general admission')]"
        )

        found_tickets = []
        if standing_elements:
            found_tickets.append("standing")
        if general_admission_elements:
            found_tickets.append("general admission")
            
        if found_tickets:
            print(f"Found ticket types: {', '.join(found_tickets)}")
            return True
        
        return False

    except (TimeoutException, NoSuchElementException):
        print("Nothing found.")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return False


def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")

    system = platform.system()
    machine = platform.machine().lower()
    is_arm64 = machine in ['aarch64', 'arm64']

    chromium_paths = []

    if system == 'Linux':
        chromium_paths = [
            '/usr/bin/chromium-browser',
            '/usr/bin/chromium',
            '/snap/bin/chromium'
        ]
        chromedriver_paths = ['/usr/bin/chromedriver']
    elif system == 'Darwin':
        chromium_paths = [
            '/Applications/Chromium.app/Contents/MacOS/Chromium',
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            os.path.expanduser('~/Applications/Chromium.app/Contents/MacOS/Chromium')
        ]
        chromedriver_paths = [
            '/usr/local/bin/chromedriver',
            '/opt/homebrew/bin/chromedriver'
        ]
    elif system == 'Windows':
        chromium_paths = [
            os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 'Google\\Chrome\\Application\\chrome.exe'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'), 'Google\\Chrome\\Application\\chrome.exe'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google\\Chrome\\Application\\chrome.exe')
        ]
        chromedriver_paths = [
            os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 'chromedriver.exe'),
            'chromedriver.exe'
        ]

    if is_arm64:
        print(f"ARM64 architecture detected on {system} - setting up driver...")

        chromium_path = None
        for path in chromium_paths:
            if os.path.exists(path):
                chromium_path = path
                break

        if chromium_path:
            options.binary_location = chromium_path
            print(f"Found browser at: {chromium_path}")

        try:
            driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            return webdriver.Chrome(service=Service(driver_path), options=options)
        except Exception as e:
            print(f"ChromeType.CHROMIUM failed: {e}")

            try:
                for chromedriver_path in chromedriver_paths:
                    if os.path.exists(chromedriver_path):
                        print(f"Using system chromedriver: {chromedriver_path}")
                        return webdriver.Chrome(service=Service(chromedriver_path), options=options)
            except Exception as e2:
                print(f"System chromedriver failed: {e2}")

            try:
                print("Attempting fallback method...")
                driver_path = ChromeDriverManager().install()
                return webdriver.Chrome(service=Service(driver_path), options=options)
            except Exception as e3:
                print(f"Fallback failed: {e3}")
                raise Exception("All driver setup methods failed on ARM64")

    else:
        print(f"Setting up Chrome driver on {system}...")
        driver_path = ChromeDriverManager().install()
        return webdriver.Chrome(service=Service(driver_path), options=options)


def random_sleep(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))


def main():
    print("Beginning hunt!")

    if is_first_run():
        print("🔍 First run detected - testing email configuration...")
        if not send_test_email():
            print("❌ Email test failed. Please fix your email configuration before continuing.")
            print("Check your SENDER_EMAIL, SENDER_PASSWORD, and RECIPIENT_EMAIL settings.")
            return
        
        print("\n" + "="*50)
        print("Email test completed successfully!")
        print("Starting ticket monitoring...")
        print("="*50 + "\n")
    else:
        print("Email configuration already tested. Starting monitoring...")

    try:
        driver = setup_driver()
        print("✅ Browser driver initialized successfully!")
    except Exception as e:
        print(f"Failed to setup browser driver: {e}")
        print("\nTroubleshooting suggestions:")

        system = platform.system()
        if system == 'Linux':
            print("1. Install system chromedriver: sudo apt install chromium-chromedriver chromium-browser")
            print("2. Or install Google Chrome from: https://www.google.com/chrome/")
        elif system == 'Darwin':
            print("1. Install via Homebrew: brew install --cask google-chrome")
            print("2. Or download from: https://www.google.com/chrome/")
        elif system == 'Windows':
            print("1. Install Google Chrome from: https://www.google.com/chrome/")
            print("2. Make sure Chrome is installed in the default location")

        return

    try:
        last_email_time = 0
        email_cooldown = 300

        while True:
            print("Hunting for tickets...")
            if check_tickets(driver):
                print("Tickets found!")
                current_time = time.time()
                if current_time - last_email_time > email_cooldown:
                    send_email()
                    last_email_time = current_time
                else:
                    remaining_cooldown = int(email_cooldown - (current_time - last_email_time))
                    print(f"Email cooldown active. Next email in {remaining_cooldown} seconds.")
            else:
                print("No tickets available.")

            random_sleep(30, 40)
    
    except KeyboardInterrupt:
        print("\n⏹️  Monitoring stopped by user.")
    finally:
        driver.quit()
        print("Browser closed.")


if __name__ == "__main__":
    main()