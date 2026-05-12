import subprocess
from datetime import datetime
from pathlib import Path

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def kill_chrome_by_profile(tmp_profile):
    if not tmp_profile:
        return

    subprocess.run(
        ["pkill", "-f", f"--user-data-dir={tmp_profile}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def salvar_print_debug(driver, base_dir=None):
    try:
        if base_dir:
            root = Path(base_dir)
        else:
            root = Path(__file__).resolve().parent

        pasta = root / "prints_debug"
        pasta.mkdir(parents=True, exist_ok=True)

        data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_arquivo = pasta / f"debug_{data_hora}.png"

        driver.save_screenshot(str(nome_arquivo))

        return str(nome_arquivo)

    except Exception:
        return None


def esperar_loading_sumir(driver, timeout=30):
    wait_loading = WebDriverWait(driver, timeout)

    possiveis_loadings = [
        (By.CSS_SELECTOR, ".dataTables_processing"),
        (By.CSS_SELECTOR, ".loading"),
        (By.CSS_SELECTOR, ".loader"),
        (By.CSS_SELECTOR, ".overlay"),
        (By.CSS_SELECTOR, ".blockUI"),
        (By.XPATH, "//*[contains(@class,'loading')]"),
        (By.XPATH, "//*[contains(@class,'loader')]"),
        (By.XPATH, "//*[contains(@class,'overlay')]"),
        (By.XPATH, "//*[contains(@style,'display: block') and (contains(@class,'loading') or contains(@class,'loader'))]"),
    ]

    for locator in possiveis_loadings:
        try:
            wait_loading.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            pass
        except NoSuchElementException:
            pass