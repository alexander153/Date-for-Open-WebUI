"""
title: Date
author: alex chatgpt
version: 0.1
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta


class Filter:
    class Valves(BaseModel):
        pass

    def __init__(self):
        self.valves = self.Valves()

    def stream(self, event: dict) -> dict:
        print(event)  # Print each incoming chunk for inspection
        return event

    async def inlet(self, body: dict) -> dict:
        """Обрабатывает входящее сообщение и определяет, нужно ли отвечать датой/годом/днем недели"""
        # print(f"[LOG] Получено сообщение: {body}")
        last_message = body["messages"][-1]["content"]
        # print(f"[LOG] Получено сообщение: {last_message}")
        message = last_message.lower()
        # print(f"[LOG] Получено сообщение: {message}")

        response = None
        # print("1")
        if any(
            phrase in message
            for phrase in [
                "какое сегодня число",
                "какое число сегодня",
                "what is today's date",
            ]
        ):
            print("[LOG] Запрос на дату (сегодня)")
            response = self.get_date_response(0, message)
        elif any(
            phrase in message
            for phrase in ["какой сегодня день недели", "what day is it today"]
        ):
            print("[LOG] Запрос на день недели (сегодня)")
            response = self.get_day_of_week_response(0, message)
        elif any(
            phrase in message for phrase in ["какой сейчас год", "what year is it"]
        ):
            print("[LOG] Запрос на текущий год")
            response = self.get_year_response(message)
        elif any(
            phrase in message
            for phrase in ["который сейчас час", "what time is it", "который час"]
        ):
            print("[LOG] Запрос на текущее время")
            response = self.get_time_response(message)
        elif any(
            phrase in message
            for phrase in ["какое было число вчера", "what was yesterday's date"]
        ):
            print("[LOG] Запрос на дату (вчера)")
            response = self.get_date_response(-1, message)
        elif any(
            phrase in message
            for phrase in ["какой был день недели вчера", "what day was it yesterday"]
        ):
            print("[LOG] Запрос на день недели (вчера)")
            response = self.get_day_of_week_response(-1, message)
        elif any(
            phrase in message
            for phrase in [
                "какое будет число завтра",
                "какое число завтра",
                "какое завтра число",
                "what will be tomorrow's date",
            ]
        ):
            print("[LOG] Запрос на дату (завтра)")
            response = self.get_date_response(1, message)
        elif any(
            phrase in message
            for phrase in [
                "какой будет день недели завтра",
                "какой завтра день недели",
                "what day will it be tomorrow",
            ]
        ):
            print("[LOG] Запрос на день недели (завтра)")
            response = self.get_day_of_week_response(1, message)
        elif any(
            phrase in message
            for phrase in [
                "какое будет число послезавтра",
                "what will be the date after tomorrow",
            ]
        ):
            print("[LOG] Запрос на дату (послезавтра)")
            response = self.get_date_response(2, message)
        elif any(
            phrase in message
            for phrase in [
                "какой будет день недели послезавтра",
                "what day will it be the day after tomorrow",
            ]
        ):
            print("[LOG] Запрос на день недели (послезавтра)")
            response = self.get_day_of_week_response(2, message)
        # print("2")
        if response:
            print(f"[LOG] Ответ: {response}")
            body["messages"][-1]["content"] = response
        else:
            print("[LOG] Запрос не обработан. Оставляем body без изменений.")
        # print("3")

        return body

    def outlet(self, body: dict) -> None:
        """Обработка исходящего сообщения (если необходимо)"""
        pass

    def get_date_response(self, offset: int, message: str) -> str:
        """Возвращает дату с учетом смещения (вчера, завтра и т. д.), определяя язык запроса."""
        target_date = datetime.now() + timedelta(days=offset)
        date_str = target_date.strftime("%d.%m.%Y")
        print(f"[LOG] Вычисленная дата: {date_str}")

        if "what" in message:
            return f"The date is {date_str}"
        return f"Дата: {date_str}"

    def get_day_of_week_response(self, offset: int, message: str) -> str:
        """Возвращает день недели с учетом смещения, определяя язык запроса."""
        days_of_week = {
            "Monday": {"ru": "Понедельник", "en": "Monday"},
            "Tuesday": {"ru": "Вторник", "en": "Tuesday"},
            "Wednesday": {"ru": "Среда", "en": "Wednesday"},
            "Thursday": {"ru": "Четверг", "en": "Thursday"},
            "Friday": {"ru": "Пятница", "en": "Friday"},
            "Saturday": {"ru": "Суббота", "en": "Saturday"},
            "Sunday": {"ru": "Воскресенье", "en": "Sunday"},
        }

        target_date = datetime.now() + timedelta(days=offset)
        day_name = target_date.strftime("%A")
        lang = "en" if "what" in message else "ru"
        print(f"[LOG] Вычисленный день недели: {days_of_week[day_name][lang]}")

        return f"{days_of_week[day_name][lang]}"

    def get_year_response(self, message: str) -> str:
        """Возвращает текущий год, определяя язык запроса."""
        current_year = datetime.now().year
        print(f"[LOG] Вычисленный год: {current_year}")

        if "what" in message:
            return f"The year is {current_year}"
        return f"Год: {current_year}"

    def get_time_response(self, message: str) -> str:
        """Возвращает текущее время, определяя язык запроса."""
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"[LOG] Вычисленное время: {current_time}")

        if "what" in message:
            return f"The current time is {current_time}"
        return f"Текущее время: {current_time}"
