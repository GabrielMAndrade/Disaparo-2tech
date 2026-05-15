import json
import os
import shutil
import signal
import sys
from pathlib import Path
from time import sleep

from dotenv import load_dotenv

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.service.driverService import criar_driver
from src.utils.helpers import kill_chrome_by_profile, salvar_print_debug


BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env", override=False)


driver = None
tmp_profile = None


def carregar_config():
    username = os.getenv("2TECH_USUARIO")
    password = os.getenv("2TECH_SENHA")
    url = os.getenv("URL_2TECH")

    if not username or not password or not url:
        raise RuntimeError(
            "Ambiente não definido. Verifique 2TECH_USUARIO, 2TECH_SENHA e URL_2TECH no .env"
        )

    return {
        "username": username,
        "password": password,
        "url": url
    }


try:
    config = carregar_config()

    driver, tmp_profile = criar_driver(True)
    wait = WebDriverWait(driver, 30)

    driver.get(config["url"])

    campo_usuario = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "/html/body/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div[1]/input"
        ))
    )
    campo_usuario.clear()
    campo_usuario.send_keys(config["username"])

    campo_senha = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "/html/body/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div[2]/input"
        ))
    )
    campo_senha.clear()
    campo_senha.send_keys(config["password"])

    button_login = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "/html/body/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[2]/div/button"
        ))
    )
    button_login.click()

    sleep(10)

    elemento_qtd_pp = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "/html/body/div[6]/div[2]/section/div[2]/div/div/div[11]/div/div[2]/div/h3"
        ))
    )

    num_pp = elemento_qtd_pp.text.strip()

    print(json.dumps({
        "resultado": num_pp
    }, ensure_ascii=False))

except Exception as e:
    print_path = None

    if driver:
        print_path = salvar_print_debug(driver, BASE_DIR / "src" / "utils")

    print(json.dumps({
        "error": str(e),
        "type": type(e).__name__,
        "print_path": print_path
    }, ensure_ascii=False))

    sys.exit(1)

finally:
    if os.name != "nt":
        try:
            kill_chrome_by_profile(tmp_profile)
        except Exception:
            pass

    if driver:
        try:
            driver.quit()
        except Exception:
            pass

        try:
            p = getattr(getattr(driver, "service", None), "process", None)
            if p and p.poll() is None:
                try:
                    os.kill(p.pid, signal.SIGKILL)
                except Exception:
                    pass
        except Exception:
            pass

    if tmp_profile:
        try:
            shutil.rmtree(tmp_profile, ignore_errors=True)
        except Exception:
            pass