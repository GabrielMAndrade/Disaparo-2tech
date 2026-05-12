import os
import tempfile

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def criar_driver(headless: bool = True):
    options = Options()

    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    os.makedirs("/var/tmp/ttech", exist_ok=True)
    os.makedirs("/var/tmp/ttech", exist_ok=True)

    tmp_profile = tempfile.mkdtemp(prefix="ttech", dir="/var/tmp/ttech")
    options.add_argument(f"--user-data-dir={tmp_profile}")
    options.add_argument("--disk-cache-dir=/var/tmp/ttech")

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    options.add_argument("--disable-blink-features=AutomationControlled")

    if os.name == "nt":
        chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome--.exe"
        if not os.path.isfile(chrome_exe):
            chrome_exe = r"C:\Program Files (x86)\Google\Chrome\Application\chrome--.exe"
        if os.path.isfile(chrome_exe):
            options.binary_location = chrome_exe

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    return driver, tmp_profile