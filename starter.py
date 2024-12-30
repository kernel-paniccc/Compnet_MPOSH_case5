from ngrok import ngrok
from src import app
from dotenv import load_dotenv
import logging

load_dotenv()

#ToDo build docker

def ngrok_run():
    logging.basicConfig(level=logging.INFO)
    listener = ngrok.werkzeug_develop()
    return listener


if __name__ == "__main__":
    #ngrok_run()
    print('CRM: https://b24-nvmjfa.bitrix24.ru/crm/catalog/')
    app.run(debug=True, use_reloader=True, port=8080)