from tabulate import tabulate


class PartitionsTable:

    def __init__(self):
        self.baseDirColumn = []
        self.limitColumn = []
        self.processColumn = []

    def add_partition(self, process_id, base_dir, limit):
        self.baseDirColumn.append(base_dir)
        self.limitColumn.append(limit)
        self.processColumn.append(process_id)

    def delete_partition(self, index):
        self.baseDirColumn.pop(index)
        self.limitColumn.pop(index)
        self.processColumn.pop(index)

    def generate_data(self):
        data = []
        for index, base_dir in enumerate(self.baseDirColumn):
            limit = self.limitColumn[index]
            process_id = self.processColumn[index]

            data.append([index + 1, process_id, base_dir, limit])

        return data

    def print(self):
        data = self.generate_data()
        print("")
        print("Tabla de Particiones")
        print(tabulate(data, headers=['No', 'Proceso', 'Localidad', 'Tamaño']))
