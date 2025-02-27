from datetime import datetime, timedelta

import caldav


class AppleCalendar:

    url = "https://caldav.icloud.com"

    def __init__(self, login, password, name):
        self.name = name
        self._client = caldav.DAVClient(url=self.url, username=login, password=password)
        self._principal = self._client.principal()


    def get_current_week(self):
        current_week = CurrentWeek()
        events = []
        for event in self._principal.search(
            start=current_week.monday, end=current_week.friday, event=True, expand=True):
            for component in event.icalendar_instance.walk():
                if component.name != "VEVENT":
                    continue
                events.append(self.fill_event(component))
        return events


    def add_event(self, start, end, summary, description):
        calendar = self._principal.calendar(self.name)
        calendar.save_event(
            dtstart=start,
            dtend=end,
            summary=summary,
            description=description
        )


    def clear_day(self, events, year, month, day):
        calendar = self._principal.calendar(self.name)
        for event in events:
            if event.start.date <= datetime.date(year, month, day) <= event.end.date:
                event.delete()


    def get_events(self):
        events = []
        for event in self._principal.calendar(self.name).events():
            for component in event.icalendar_instance.walk():
                if component.name != "VEVENT":
                    continue
                events.append(self.fill_event(component))
        return events


    @staticmethod
    def fill_event(component) -> dict[str, str]:
        cur = {
            "summary": component.get("summary"),
            "description": component.get("description"),
            "start": component.get("dtstart").dt.strftime("%m/%d/%Y %H:%M"),

        }
        end_date = component.get("dtend")
        if end_date and end_date.dt:
            cur["end"] = end_date.dt.strftime("%m/%d/%Y %H:%M")
        cur["datestamp"] = component.get("dtstamp").dt.strftime("%m/%d/%Y %H:%M")
        return cur


class CurrentWeek:
    def __init__(self):
        now = datetime.now()
        days_since_monday = now.weekday()
        if days_since_monday > 4:
            self.monday = now + timedelta(days=6 - days_since_monday)
            days_until_friday = (6 - days_since_monday) + 6
            self.friday = now + timedelta(days=days_until_friday)
        else:
            self.monday = now - timedelta(days=days_since_monday)
            days_until_friday = 4 - now.weekday()  # Friday is 4 in weekday() (0-indexed)
            if days_until_friday < 0:
                days_until_friday += 7
            self.friday = now + timedelta(days=days_until_friday)