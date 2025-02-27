import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import os

# Конфигурация
link = 'https://freelance.habr.com/tasks'
telegram_bot_token = '7563837199:AAEuTG4uC0BvYzAWiHK0ZpY2KUR_27tE4NE'  # Замените на токен вашего бота
telegram_chat_id = '7482542861'  # Замените на ID вашего чата
history_file = 'orders_history.txt'  # Файл для хранения ссылок на заказы
polling_interval = 60  # Интервал опроса в секундах

def send_telegram_message(message):
    """Отправляет сообщение в Telegram."""
    utc_offset = timedelta(hours=0)  # Смещение Московского времени относительно UTC
    current_time_msk = datetime.now() + utc_offset

    # Формирование сообщения для отправки в Telegram
    message_text = (
        f"Новый заказ: {message['title']}\n"
        f"URL: {message['url']}\n"
        f"Время входа: {current_time_msk.strftime('%Y-%m-%d %H:%M:%S')}\n"
    )

    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    
    data = {
        "chat_id": telegram_chat_id,
        "text": message_text,
    }

    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(f"Сообщение успешно отправлено: {message_text}")
        else:
            print(f"Ошибка отправки сообщения в Telegram: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

def load_history():
    """Загружает историю обработанных заказов из файла."""
    if not os.path.exists(history_file):
        # Создаем файл, если его нет
        with open(history_file, 'w'):
            pass
    try:
        with open(history_file, 'r') as file:
            return set(file.read().splitlines())
    except Exception as e:
        print(f"Ошибка при загрузке истории: {e}")
        return set()

def save_to_history(href):
    """Сохраняет ссылку на заказ в файл."""
    try:
        with open(history_file, 'a') as file:
            file.write(href + '\n')
    except Exception as e:
        print(f"Ошибка при сохранении истории: {e}")

def fetch_new_orders():
    """Получает новые заказы с сайта."""
    try:
        response = requests.get(link)
        if response.status_code != 200:
            print(f"Ошибка запроса: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        content_list_items = soup.find_all(class_='content-list__item')
        new_orders = []

        for item in content_list_items:
            task_title = item.find(class_='task__title')
            if task_title:
                task_link = task_title.find('a')
                if task_link:
                    href = task_link.get('href')
                    full_link = 'https://freelance.habr.com' + href
                    title = task_title.get_text(strip=True)
                    new_orders.append((full_link, title))
                    
        return new_orders
    except Exception as e:
        print(f"Ошибка при получении заказов: {e}")
        return []

def main():
    print("Бот запущен...")
    processed_links = load_history()

    while True:
        new_orders = fetch_new_orders()

        for full_link, title in new_orders:
            if full_link not in processed_links:
                message = {
                    'title': title,
                    'url': full_link
                }
                send_telegram_message(message)

                # Добавляем в историю
                save_to_history(full_link)
                processed_links.add(full_link)

        # Задержка между запросами
        time.sleep(polling_interval)

if __name__ == '__main__':
    main()
