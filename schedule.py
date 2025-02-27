from datetime import datetime, timedelta

from librus_apix.client import Client, new_client, Token
from librus_apix.timetable import get_timetable

from applecalendar import CurrentWeek


class Schedule:

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.client: Client = new_client()
        _token: Token = self.client.get_token(login, password)
        key = self.client.token.API_Key
        token = Token(API_Key=key)
        self.client = new_client(token=token)

    def get_current_week(self):
        current_week = CurrentWeek()
        events = []
        for weekday in get_timetable(self.client, current_week.monday):
            for period in weekday:
                events.append({
                    "subject": period.subject,
                    "start": period.date_from,
                    "end": period.date_to,
                    "weekday": period.weekday,
                    "number": period.number,
                    "info": period.info,
                    "teacher": period.teacher_and_classroom,
                    "next_from": period.next_recess_from,
                    "next_to": period.next_recess_to
                })
        return events
