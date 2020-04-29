from tabulate import tabulate


class FreeAreasTable:

    def __init__(self):
        self.baseDirColumn = []
        self.limitColumn = []

    def free_area(self):
        free_area = 0
        for size in self.limitColumn:
            free_area += size
        return free_area

    def add_element(self, base_dir, limit):
        self.baseDirColumn.append(base_dir)
        self.limitColumn.append(limit)

    def remove_element(self, index):
        self.baseDirColumn.pop(index)
        self.limitColumn.pop(index)

    def get_last_index(self):
        return len(self.baseDirColumn) - 1

    def generate_data(self):
        data = []
        for index, base_dir in enumerate(self.baseDirColumn):
            limit = self.limitColumn[index]
            data.append([index + 1, base_dir, limit])

        return data

    def print(self):
        data = self.generate_data()
        print("")
        print("Tabla de Áreas Libres")
        print(tabulate(data, headers=['No', 'Localidad', 'Tamaño']))
