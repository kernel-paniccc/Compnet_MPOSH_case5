import requests
from dotenv import load_dotenv
import os

def create_order_in_bitrix(product_name, price, quantity, supplier):

    load_dotenv()

    bitrix_webhook_url = os.getenv('BITRIX')

    order_data = {
        "fields": {
            "NAME": product_name,
            "QUANTITY": quantity,
            "DESCRIPTION": f'товар: {product_name}\n цена: {price}\n  количество: {quantity}\n  поставщик: {supplier}',
            "PRICE": price,
            "CREATED_BY": supplier,
        }
    }

    response = requests.post(
        f"{bitrix_webhook_url}/crm.product.add.json",
        json=order_data
    )

    return response.status_code