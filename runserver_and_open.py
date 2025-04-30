import os
import webbrowser
import threading
import time

def open_browser():
    time.sleep(1)  # Подождать, чтобы сервер успел запуститься
    webbrowser.open('http://127.0.0.1:8000/')

if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    os.system('python manage.py runserver')
