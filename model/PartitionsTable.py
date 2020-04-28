class PartitionsTable:

    def __init__(self):
        #self.noColumn = []
        self.baseDirColumn = []
        self.limitColumn = []
        self.stateColumn = []
        self.processColumn = []

    def add_partition(self, process_id, baseDir, limit):
        #self.noColumn.append(len(self.noColumn) + 1)
        self.baseDirColumn.append(baseDir)
        self.limitColumn.append(limit)
        self.stateColumn.append("ASIGNADO")
        self.processColumn.append(process_id)

    def delete_partition(self, index):
        #self.noColumn.pop(index)
        self.baseDirColumn.pop(index)
        self.limitColumn.pop(index)
        self.stateColumn.pop(index)
        self.processColumn.pop(index)
