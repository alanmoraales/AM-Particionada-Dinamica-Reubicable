class NoMoreEventsError(Exception):

    def __init__(self):
        self.message = "No quedan más eventos."
