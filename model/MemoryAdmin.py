from model.FreeAreasTable import FreeAreasTable
from model.PartitionsTable import PartitionsTable
from model.Event import Event
from model.Process import Process


class MemoryAdmin:
    def __init__(self, memory_size, so_size, event_admin):
        self.memory_size = memory_size
        self.so_size = so_size

        self.event_admin = event_admin

        self.partitions_table = PartitionsTable()
        self.free_areas_table = FreeAreasTable()

        self.free_areas_table.add_element(so_size, memory_size - so_size)

    def run(self):
        while self.event_admin.there_is_more_events():
            event = self.event_admin.next_event()
            if event.type == "LLEGA":
                self.assing_memory(Process(event.process_id, event.size))
            elif event.type == "TERMINA":
                self.free_memory(event.process_id)

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
        event_list = []
        for index, process_id in enumerate(self.partitions_table.processColumn):
            process_size = self.partitions_table.limitColumn[index]
            event_list.append(Event(process_id, process_size))

        self.clear_tables()
        self.free_areas_table.add_element(self.so_size, self.memory_size - self.so_size)

        for event in event_list:
            self.assing_memory(Process(event.process_id, event.size))

    def clear_tables(self):
        self.partitions_table.noColumn.clear()
        self.partitions_table.baseDirColumn.clear()
        self.partitions_table.limitColumn.clear()
        self.partitions_table.stateColumn.clear()
        self.partitions_table.processColumn.clear()

        self.free_areas_table.noColumn.clear()
        self.free_areas_table.baseDirColumn.clear()
        self.free_areas_table.limitColumn.clear()
        self.free_areas_table.stateColumn.clear()

    def free_memory(self, process_id):
        for index, id in enumerate(self.partitions_table.processColumn):
            if id == process_id:
                baseDir = self.partitions_table.baseDirColumn[index]
                limit = self.partitions_table.limitColumn[index]
                self.free_areas_table.add_element(baseDir, limit)

                self.partitions_table.delete_partition(index)
                self.compact_free_areas()

    def compact_free_areas(self):
        # looking for continuos memory after the new free area
        index = self.free_areas_table.get_last_index()
        last_dir = self.free_areas_table.baseDirColumn[index] + self.free_areas_table.limitColumn[index]

        for idx, base_dir in enumerate(self.free_areas_table.baseDirColumn):
            if base_dir == last_dir:
                size = self.free_areas_table.limitColumn[idx]
                self.free_areas_table.limitColumn[index] += size
                self.free_areas_table.remove_element(idx)
                break

        #looking for continuos memory before the new free area
        index = self.free_areas_table.get_last_index()
        base_dir = self.free_areas_table.baseDirColumn[index]

        for idx, base_dir_ in enumerate(self.free_areas_table.baseDirColumn):
            last_dir = base_dir + self.free_areas_table.limitColumn[idx]
            if last_dir == base_dir:
                size = self.free_areas_table.limitColumn[index]
                self.free_areas_table.limitColumn[idx] += size
                self.free_areas_table.remove_element(index)
                break

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
