from model.FreeAreasTable import FreeAreasTable
from model.PartitionsTable import PartitionsTable
from model.Event import Event


class MemoryAdmin:
    def __init__(self, memory_size, so_size, event_admin):
        self.memory_size = memory_size
        self.event_admin = event_admin

        self.partitions_table = PartitionsTable()
        self.free_areas_table = FreeAreasTable()

        self.free_areas_table.add_element(so_size, memory_size - so_size)

    def assing_memory(self, process):
        index = self.request_memory(process.size)
        if index != -1:
            self.partitions_table.add_partition(process.id, self.free_areas_table.baseDirColumn[index], process.size)
            self.update_free_areas_table(index, process.size)
        elif self.free_areas_table.free_area() >= process.size:
            self.reubicate_partitions()
            self.assing_memory(process)
        else:
            self.event_admin.add_even(Event("LLEGA", process.id, process.size))

    def reubicate_partitions(self):
        print("reubicando")

    def free_memory(self, process_id):
        for index, id in enumerate(self.partitions_table.processColumn):
            if id == process_id:
                baseDir = self.partitions_table.baseDirColumn[index]
                limit = self.partitions_table.limitColumn[index]
                self.free_areas_table.add_element(baseDir, limit)

                self.partitions_table.delete_partition(index)
                self.compact_free_areas()

    def compact_free_areas(self):
        print("compactando")

    def update_free_areas_table(self, index, size):
        self.free_areas_table.limitColumn[index] -= size
        self.free_areas_table.baseDirColumn[index] += size

        if self.free_areas_table.limitColumn[index] == 0:
            self.free_areas_table.remove_element(index)

    def request_memory(self, size):
        for index, state in enumerate(self.free_areas_table.stateColumn):
            if state == "DISPONIBLE" and self.free_areas_table.limitColumn[index] >= size:
                return index
        return -1
