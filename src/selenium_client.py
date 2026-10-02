import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select


driver = webdriver.Chrome()

driver.get('http://localhost:8000/dynamic')

button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.TAG_NAME, 'button'))
)

button.click()

WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, '#items tr')
    )
)

mode = input(
    'Введите режим (all - все записи, category - фильтр по категории): '
)

if mode == 'category':
    category = input('Введите категорию: ')
    category_select = Select(
        driver.find_element(By.ID, 'category')
    )
    category_select.select_by_value(category)
    button.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '#items tr')
        )
    )


rows = driver.find_elements(
    By.CSS_SELECTOR,
    '#items tr'
)

data = []
for row in rows:
    cells = row.find_elements(By.TAG_NAME, 'td')

    if len(cells) == 5:
        item = {
            'id': int(cells[0].text),
            'name': cells[1].text,
            'category': cells[2].text,
            'value': float(cells[3].text.replace(',', '.')),
            'active': cells[4].text.strip().lower() == 'true'
        }

        data.append(item)


data = pd.DataFrame(data)
data.to_csv(
    'results/selenium_items.csv',
    index=False
)

driver.quit()

print('Данные сохранены в results/selenium_items.csv')
print(data.head())