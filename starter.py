from ngrok import ngrok
from src import app
from dotenv import load_dotenv
import logging

load_dotenv()

def ngrok_run():
    logging.basicConfig(level=logging.INFO)
    listener = ngrok.werkzeug_develop()
    return listener


if __name__ == "__main__":
    #ngrok_run()
    print('CRM: https://b24-nvmjfa.bitrix24.ru/crm/catalog/')
    app.run(port=8081, host='0.0.0.0') #use_reloader=True, debug=True