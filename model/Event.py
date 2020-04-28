class Event:

    def __init__(self, type, process_id, size):
        self.type = type
        self.process_id = process_id
        self.size = size

    def __init__(self, type, process_id):
        self.type = type
        self.process_id = process_id
