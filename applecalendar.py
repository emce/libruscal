from current_week import CurrentWeek


class AppleCalendar:

    key_format = "%Y%m%d%H%M"
    current_week = CurrentWeek()

    def __init__(self, client, name):
        self.client = client
        self.name = name

    def get_current_week(self):
        events = []
        for event in self.client.calendar(self.name).search(
                start=self.current_week.monday, end=self.current_week.friday, event=True, expand=True):
            for component in event.icalendar_instance.walk():
                if component.name != "VEVENT":
                    continue
                events.append(self.fill_event(component))
        return self.events_to_date_dict(events)

    def clear_current_week(self):
        calendar = self.client.calendar(self.name)
        for event in calendar.events():
            for component in event.icalendar_instance.walk():
                if component.name != "VEVENT":
                    continue
                calendar.event(component.get("uid")).delete()
        return { "result": "success" }


    def add_event(self, start, end, summary, description, location):
        calendar = self.client.calendar(self.name)
        calendar.save_event(
            dtstart=start,
            dtend=end,
            summary=summary,
            description=description,
            location=location,
        )

    def process_schedule(self, schedule):
        self.clear_current_week()
        added = 0
        for entry in schedule:
            if entry['subject']:
                self.add_event(entry['start'], entry['end'], entry['subject'], entry['teacher'], entry['teacher'])
                added+=1
        return {
            "added": added,
        }

    def events_to_date_dict(self, events):
        date_dict = {}
        for event in events:
            start = event['start']
            date_dict[start.strftime(self.key_format)] = event
        return date_dict

    @staticmethod
    def fill_event(component):
        cur = {
            "uid": component.get("uid"),
            "summary": component.get("summary").to_ical().decode("utf-8"),
            "description": component.get("description").to_ical().decode("utf-8"),
            "start": component.get("dtstart").dt,
            "location": component.get("location").to_ical().decode("utf-8"),
        }
        end_date = component.get("dtend")
        if end_date and end_date.dt:
            cur["end"] = end_date.dt
        cur["datestamp"] = component.get("dtstamp").dt
        return cur