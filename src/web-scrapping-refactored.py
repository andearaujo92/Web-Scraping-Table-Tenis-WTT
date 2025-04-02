import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
import warnings

warnings.filterwarnings('ignore')

def iniciar_driver():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # Executar em segundo plano (opcional)
    driver = webdriver.Firefox(options=options)
    return driver

def get_site(driver, url: str):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

def login(driver, user: str, password: str):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "modlgn-username-16")))
    
    text_box = driver.find_element(By.ID, "modlgn-username-16")
    pass_box = driver.find_element(By.ID, "modlgn-passwd-16")
    submit_button = driver.find_element(By.NAME, "Submit")
    
    text_box.send_keys(user)
    pass_box.send_keys(password)
    submit_button.click()

def get_total_pages(driver):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[last()-1]/a"))).click()
    
    total_pages_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.col:nth-child(3) > p:nth-child(1)"))
    )
    total_pages_number = int(total_pages_element.text.split()[1])
    print(f'Total de páginas: {total_pages_number}')
    return total_pages_number

def get_start_page(driver):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[1]/a"))).click()
    print("De volta à página #1")

def get_tables(driver, n_of_pages: int):
    dfs = []
    for page in range(1, n_of_pages + 1):
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table")
        
        if table:
            df = pd.read_html(str(table))[0].iloc[:-1, :-1]
            dfs.append(df)
        
        print(f'Tabela #{page} raspada...')
        
        try:
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[last()-1]/a")))
            next_button.click()
        except:
            print("Não foi possível avançar para a próxima página.")
            break
    
    return pd.concat(dfs) if dfs else None

def export_df(df: pd.DataFrame, filename: str = "wtt-stats.csv"):
    df.to_csv(filename, index=False)

def main():
    driver = iniciar_driver()
    try:
        get_site(driver, "https://results.ittf.link/")
        login(driver, "****", "****")
        get_site(driver, "https://results.ittf.link/index.php/statistics/win-rate-all-events/")
        total_pages = get_total_pages(driver)
        get_start_page(driver)
        df = get_tables(driver, total_pages)
        if df is not None:
            export_df(df)
            print("Dados exportados com sucesso!")
        else:
            print("Nenhuma tabela foi extraída.")
    finally:
        driver.quit()
        print("Driver fechado.")

if __name__ == "__main__":
    main()
