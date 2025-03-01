from datetime import datetime, timedelta


class CurrentWeek:
    def __init__(self):
        now = datetime.now()
        if now.weekday() > 4:
            days_to_monday = 7 - now.weekday()
            monday = now + timedelta(days=days_to_monday)
            self.monday = monday.replace(hour=0, minute=0)
        else:
            days_since_monday = now.weekday()
            monday = now - timedelta(days=days_since_monday)
            self.monday = monday.replace(hour=0, minute=0)
        self.tuesday = self.monday + timedelta(days=1)
        self.wednesday = self.monday + timedelta(days=2)
        self.thursday = self.monday + timedelta(days=3)
        friday = self.monday + timedelta(days=4)
        self.friday = friday.replace(hour=23, minute=00)
