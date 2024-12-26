from src import app

if __name__ == "__main__":
    print('http://127.0.0.1:7777\nCRM: https://b24-nvmjfa.bitrix24.ru/crm/catalog/')
    app.run(use_reloader=True, port=7777)
