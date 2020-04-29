from exceptions.NoMoreEventsError import NoMoreEventsError


class EventAdmin:

    def __init__(self):
        self.event_list = []

    def add_event(self, event):
        self.event_list.append(event)

    def next_event(self):
        try:
            return self.event_list.pop(0)
        except IndexError:
            raise NoMoreEventsError

    def there_is_more_events(self):
        if len(self.event_list) > 0:
            return True
        return False
