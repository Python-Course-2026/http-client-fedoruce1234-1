"""
Практика: HTTP-клиент для чата с AI
====================================
Цель: написать консольный чат, который общается с DeepSeek через API.

Запуск:
    pip install requests
    python chat.py

Документация DeepSeek API:
    https://platform.deepseek.com/api-docs
    (совместим с OpenAI - формат запросов одинаковый)
"""
from sys import prefix

import requests
import os
from dotenv import load_do

# --- Настройки ---
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"
HISTORY_LIMIT = 20

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

SYSTEM_PROMPT = {
    "role": "sistem",
    "content": (
        "Ты дружелюбный помощник для изучения Python. "
        "Объясняй просто, приводи короткие примеры кода. "
        "Отвечай на русском. "
    ),

}
# ---------------------------------------------------------------
# ЗАДАНИЕ 1: Функция отправки одного сообщения
# ---------------------------------------------------------------
# Принимает список сообщений (история), возвращает ответ модели (строку).
#
# Что отправляем (тело POST-запроса):
# {
#     "model": "deepseek-chat",
#     "messages": [
#         {"role": "user", "content": "Привет!"}
#     ]
# }
#
# Что приходит в ответ (response.json()):
# {
#     "choices": [
#         {
#             "message": {
#                 "role": "assistant",
#                 "content": "Привет! Чем могу помочь?"
#             }
#         }
#     ]
# }
#
# Нам нужно: response.json()["choices"][0]["message"]["content"]

def send_message(messages: list[dict]) -> str:

    """Отправить историю сообщений в API, вернуть текст ответа."""

    # Шаг 1: сформируй тело запроса
    body = {
        "model": MODEL,
        "messages": messages,
        # TODO: добавь "model" и "messages"
    }
    response = requests.post(API_URL, headers=HEADERS, json=body, timeout=30)
    response.raise_for_status()


    # Шаг 2: отправь POST-запрос
    # response = requests.post(API_URL, headers=HEADERS, json=body, timeout=30)

    # Шаг 3: проверь что запрос успешный (бросит исключение если 4xx/5xx)
    # response.raise_for_status()

    # Шаг 4: достань текст ответа и верни его
    # Подсказка: response.json()["choices"][0]["message"]["content"]
    return response.json()["choices"][0]["message"]["content"]



# ---------------------------------------------------------------
# ЗАДАНИЕ 2: Основной цикл чата
# ---------------------------------------------------------------
# История - это обычный список словарей.
# Каждое сообщение: {"role": "user" или "assistant", "content": "текст"}
#
# Пример как выглядит history после двух реплик:
# [
#     {"role": "user",      "content": "Что такое список?"},
#     {"role": "assistant", "content": "Список - это..."},
#     {"role": "user",      "content": "А словарь?"},
# ]
#
# Именно этот список ты передаёшь в send_message() -
# модель видит всю историю и отвечает с учётом контекста.
#
# Алгоритм:
# 1. Создай пустой список history = []
# 2. В бесконечном цикле:
#    а) user_input = input("Вы: ")
#    б) Если user_input == "exit" - break
#    в) Добавь {"role": "user", "content": user_input} в history
#    г) reply = send_message(history)
#    д) Добавь {"role": "assistant", "content": reply} в history
#    е) print(f"DeepSeek: {reply}")

def main():
    print("Чат с DeepSeek. Введите 'exit' для выхода.\n")
 history = []  # список сообщений - история диалога

    while True:
        # TODO: реализуй цикл диалога по алгоритму выше
        try:
            user_input = input("Вы: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nПока!")
            break
        if not user_input:
            continue
        if users_input.lower() == "exit":
            print("Пока!")
            break

        try:
            user_input.encode("utf-8").decode("utf-8")
        except UnicodeError:
            print("[Ошибка]: введенный текст содержит недопустимые символы.")
            continue
        history.append({"role": "user", "content": user_input})
        try:
            # system-сообщение всегда первое, история ограничена
            messages = [SYSTEM_PROMPT] + history[-HISTORY_LIMIT:]
            reply = send_message(messages)
        except requests.HTTPError as e:
            print(f"[Ошибка API]: {e.response.status_code} - {e.response.text}")
            history.pop()
            continue
        except requests.RequestException as e:
            print(f"[Сетевая ошибка]: {e}")
            history.pop()
            continue
        history.append({"role": "assistant", "content": reply})

        print(f"\nDeepseek: {reply}\n")
        with open("chat_log.txt", "a", encoding="utf-8") as f:
            f.write(f"Вы: {user_input}\n")
            f.write(f"Deepseek: {reply}\n")
            f.write("_" * 40 + "\n")

        # ---------------------------------------------------------------
        # БОНУС (если успеваешь):
        # ---------------------------------------------------------------
        # 1. Добавь system-сообщение ПЕРЕД history при отправке:
        #    system = {"role": "system", "content": "Ты помощник для изучения Python. Отвечай кратко."}
        #    messages = [system] + history
        #
        # 2. Ограничь историю последними 10 сообщениями (иначе растёт бесконечно):
        #    messages = [system] + history[-10:]
        #
        # 3. Сохраняй диалог в файл chat_log.txt после каждого ответа.
        #
        # 4. Обработай ошибки через try/except requests.RequestException

        if __name__ == "__main__":
            main()
