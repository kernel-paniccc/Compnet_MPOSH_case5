import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.parser_model.func import collect_product_info
import time


def get_products_links(item_name, price) -> list:
    price = int(price)
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

    driver.get(url=driver.current_url)
    time.sleep(2)

    try:
        products_links = driver.find_elements(By.CLASS_NAME, 'tile-clickable-element')
        products_links = [product.get_attribute('href') for product in products_links]
        if None in products_links:
            products_links = []

        print('[+] Ссылки на товары собраны!')
    except:
        print('[!] Что-то сломалось при сборе ссылок на товары!')

    clear_links = []

    for link in products_links:
        data = collect_product_info(driver=driver, url=link)
        prise = data['product_discount_price']
        clear_prise = str(prise).replace('\u2009', '').replace('₽', '').strip()
        if int(clear_prise) < price:
            clear_links.append(link)
        if len(clear_links) == 1:
            break

    driver.close()
    driver.quit()
    return clear_links

if __name__ == '__main__':
    data = get_products_links('iphone 12', 60000)
    print(data)
