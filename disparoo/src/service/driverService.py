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
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=0")

    os.makedirs("/var/tmp/ttech", exist_ok=True)

    tmp_profile = tempfile.mkdtemp(prefix="ttech_", dir="/var/tmp/ttech")

    options.add_argument(f"--user-data-dir={tmp_profile}")
    options.add_argument("--disk-cache-dir=/var/tmp/ttech")

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    options.add_argument("--disable-blink-features=AutomationControlled")

    chrome_bin = os.getenv("CHROME_BIN")

    if chrome_bin and os.path.isfile(chrome_bin):
        options.binary_location = chrome_bin

    elif os.name == "nt":
        possiveis_chromes = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome--.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome--.exe",
        ]

        for chrome_exe in possiveis_chromes:
            if os.path.isfile(chrome_exe):
                options.binary_location = chrome_exe
                break

    else:
        possiveis_chromes = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
        ]

        for chrome_exe in possiveis_chromes:
            if os.path.isfile(chrome_exe):
                options.binary_location = chrome_exe
                break

    chromedriver_path = os.getenv("CHROMEDRIVER_PATH")

    if chromedriver_path and os.path.isfile(chromedriver_path):
        service = Service(chromedriver_path)
    else:
        service = Service()

    driver = webdriver.Chrome(service=service, options=options)

    return driver, tmp_profile