#%%
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
import warnings
warnings.filterwarnings('ignore')

#%%
driver = webdriver.Firefox()

def get_site(url:str):
    driver.get(url)
    time.sleep(5)

def login(user:str, password:str):
    text_box = driver.find_element(by=By.ID, value="modlgn-username-16")
    pass_box = driver.find_element(by=By.ID, value="modlgn-passwd-16")
    submit_button = driver.find_element(by=By.NAME, value="Submit")

    actions = ActionChains(driver)
    actions.scroll_to_element(submit_button)

    text_box.send_keys(user)
    pass_box.send_keys(password)
    submit_button.click()

def get_total_pages():
    # indo para a ultima página
    end_next_button = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div/main/form/div[2]/table/tfoot/tr/td/div/div/nav/ul/li[14]/a")
    time.sleep(1)

    driver.execute_script("arguments[0].click();", end_next_button)
    time.sleep(5)

    # pegando o total de páginas para o loop
    total_pages_element = driver.find_element(by=By.CSS_SELECTOR, value="div.col:nth-child(3) > p:nth-child(1)")
    total_pages_text = total_pages_element.text
    total_pages_number = int(total_pages_text.split()[1])
    
    print(f'Total de páginas: {total_pages_number}')

def get_start_page():
    # voltando para o inicio
    start_button = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div/main/form/div[2]/table/tfoot/tr/td/div/div/nav/ul/li[1]/a")
    driver.execute_script("arguments[0].scrollIntoView();", start_button)
    time.sleep(1)

    driver.execute_script("arguments[0].click();", start_button)
    time.sleep(10)
    print("De volta à página #1")

def get_tables(n_of_pages:int):
    
    dfs = []

    for page in range(1, n_of_pages + 1):

        next_button = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div/main/form/div[2]/table/tfoot/tr/td/div/div/nav/ul/li[13]/a")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table")

        if table:
            df = pd.read_html(str(table))[0]
            df = df.iloc[:-1, :-1]

        dfs.append(df)

        driver.execute_script("arguments[0].click();", next_button)

        print(f'Tabela #{page} raspada...')

        time.sleep(15)

    df_final = pd.concat(dfs)

def export_df(df:pd.DataFrame):
    df.to_csv("wtt-stats.csv")

#%%

# Executando as funções
get_site("https://results.ittf.link/")
login("*****","*****")
get_site("https://results.ittf.link/index.php/statistics/win-rate-all-events/")
get_total_pages()
get_start_page()
get_tables()
