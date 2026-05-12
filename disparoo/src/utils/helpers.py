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
    
    # 1. Define diretório base
    if base_dir:
        root = Path(base_dir)
    else:
        # pega raiz do projeto automaticamente
        root = Path(__file__).resolve().parent

    # 2. Pasta de prints
    pasta = root / "prints_debug"
    pasta.mkdir(parents=True, exist_ok=True)

    # 3. Nome do arquivo
    data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = pasta / f"debug_{data_hora}.png"

    # 4. Salvar print
   

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