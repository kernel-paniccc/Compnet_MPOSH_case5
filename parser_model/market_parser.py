import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def get_products_links(item_name):
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    driver.get(url='https://ozon.ru')
    time.sleep(2)

    find_input = driver.find_element(By.NAME, 'text')
    find_input.clear()
    find_input.send_keys(item_name)
    time.sleep(2)

    find_input.send_keys(Keys.ENTER)
    time.sleep(2)

    # current_url = f'{driver.current_url}&sorting=rating'
    # driver.get(url=current_url)
    time.sleep(2)

    try:
        products_links = driver.find_elements(By.CLASS_NAME, 'tile-clickable-element')
        products_links = [product.get_attribute('href') for product in products_links]

        print('[+] Ссылки на товары собраны!')
    except:
        print('[!] Что-то сломалось при сборе ссылок на товары!')

    driver.close()
    driver.quit()
    return products_links