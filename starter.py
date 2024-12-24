from src import app

print('http://127.0.0.1:8080')
if __name__ == "__main__":
    app.run(use_reloader=True, port=8080)
