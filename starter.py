from src import app
from dotenv import load_dotenv
from pyngrok import ngrok
import os

load_dotenv()

port = 8080

#ToDo Make README
#ToDo applet for broken
#ToDo config ngrok
#ToDo build docker

if __name__ == "__main__":
    print('CRM: https://b24-nvmjfa.bitrix24.ru/crm/catalog/')
    app.run(host='0.0.0.0', debug=True, port=port)