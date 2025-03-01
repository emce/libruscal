from datetime import datetime, timedelta

from dateutil import parser
from librus_apix.client import Client, new_client, Token
from librus_apix.timetable import get_timetable

from current_week import CurrentWeek


class Schedule:

    def __init__(self, client):
        self.client: Client = client

    """
        Represents a period of a class with relevant information.
        Attributes:
            subject (str): The subject of the class.
            teacher_and_classroom (str): Combined information of teacher and classroom.
            date (str): The date of the period.
            date_from (str): Starting time of the period.
            date_to (str): Ending time of the period.
            weekday (str): The day of the week of the period.
            info (Dict[str, str]): Additional information about the period.
            number (int): The number of the period within a day.
            next_recess_from (str | None): Starting time of the next recess, if any.
            next_recess_to (str | None): Ending time of the next recess, if any.
        """
    def get_current_week(self):
        current_week = CurrentWeek()
        events = []
        for weekday in get_timetable(self.client, current_week.monday):
            for period in weekday:
                events.append({
                    "subject": period.subject,
                    "start": self.get_proper_date(parser.parse(period.date_from), period.weekday),
                    "end": self.get_proper_date(parser.parse(period.date_to), period.weekday),
                    "weekday": period.weekday,
                    "number": period.number,
                    "info": period.info,
                    "teacher": period.teacher_and_classroom
                })
        return events

    @staticmethod
    def get_proper_date(date, day):
        current_week = CurrentWeek()
        if day == "Monday":
            return date.replace(
                year=current_week.monday.year,
                month=current_week.monday.month,
                day=current_week.monday.day)
        elif day == "Tuesday":
            return date.replace(
                year=current_week.tuesday.year,
                month=current_week.tuesday.month,
                day=current_week.tuesday.day
            )
        elif day == "Wednesday":
            return date.replace(
                year=current_week.wednesday.year,
                month=current_week.wednesday.month,
                day=current_week.wednesday.day
            )
        elif day == "Thursday":
            return date.replace(
                year=current_week.thursday.year,
                month=current_week.thursday.month,
                day=current_week.thursday.day
            )
        else:
            return date.replace(
                year=current_week.friday.year,
                month=current_week.friday.month,
                day=current_week.friday.day
            )
