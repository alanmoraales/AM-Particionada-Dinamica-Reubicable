class FreeAreasTable:

    def __init__(self):
        self.noColumn = []
        self.baseDirColumn = []
        self.limitColumn = []
        self.stateColumn = []

    def free_area(self):
        free_area = 0
        for size in self.limitColumn:
            free_area += size
        return free_area

    def add_element(self, baseDir, limit):
        self.noColumn.append(len(self.noColumn + 1))
        self.baseDirColumn.append(baseDir)
        self.limitColumn.append(limit)
        self.stateColumn.append("DISPONIBLE")

    def remove_element(self, index):
        self.noColumn.pop(index)
        self.baseDirColumn.pop(index)
        self.limitColumn.pop(index)
        self.stateColumn.pop(index)
