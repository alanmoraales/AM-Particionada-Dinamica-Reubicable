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
                print("Llega: " + event.process_id)
                self.assing_memory(Process(event.process_id, event.size))
            elif event.type == "TERMINA":
                print("Termina: " + event.process_id)
                self.free_memory(event.process_id)

            self.print_tables()
            print("")

    def assing_memory(self, process):
        index = self.request_memory(process.size)
        if index != -1:
            print("Asignando " + str(process.id) + " en localidad " + str(self.free_areas_table.baseDirColumn[index]))
            self.partitions_table.add_partition(process.id, self.free_areas_table.baseDirColumn[index], process.size)
            self.update_free_areas_table(index, process.size)
        elif self.free_areas_table.free_area() >= process.size:
            print("No hubo espacio para el proceso. Reubicando particiones...")
            self.reubicate_partitions()
            self.assing_memory(process)
        else:
            print("No hubo espacio para el proceso, se ha devuelto a la cola.")
            self.event_admin.add_event(Event("LLEGA", process.id, process.size))

    def reubicate_partitions(self):
        event_list = []
        for index, process_id in enumerate(self.partitions_table.processColumn):
            process_size = self.partitions_table.limitColumn[index]
            event_list.append(Event("LLEGA", process_id, process_size))

        self.clear_tables()
        self.free_areas_table.add_element(self.so_size, self.memory_size - self.so_size)

        for event in event_list:
            self.assing_memory(Process(event.process_id, event.size))

    def clear_tables(self):
        self.partitions_table.baseDirColumn.clear()
        self.partitions_table.limitColumn.clear()
        self.partitions_table.processColumn.clear()

        self.free_areas_table.baseDirColumn.clear()
        self.free_areas_table.limitColumn.clear()

    def free_memory(self, process_id):
        for index, id in enumerate(self.partitions_table.processColumn):
            if id == process_id:
                print("Eliminando partición: " + process_id)
                base_dir = self.partitions_table.baseDirColumn[index]
                limit = self.partitions_table.limitColumn[index]
                self.free_areas_table.add_element(base_dir, limit)

                self.partitions_table.delete_partition(index)
                self.compact_free_areas()

    def compact_free_areas(self):
        # looking for continuos memory after the new free area
        index = self.free_areas_table.get_last_index()
        last_dir = self.free_areas_table.baseDirColumn[index] + self.free_areas_table.limitColumn[index]
        done = False

        print("Buscando áreas libres de memoria contiguas...")

        for idx, base_dir in enumerate(self.free_areas_table.baseDirColumn):
            if base_dir == last_dir:
                size = self.free_areas_table.limitColumn[idx]
                self.free_areas_table.limitColumn[index] += size
                self.free_areas_table.remove_element(idx)
                done = True
                break

        # looking for continuos memory before the new free area
        index = self.free_areas_table.get_last_index()
        base_dir = self.free_areas_table.baseDirColumn[index]

        for idx, base_dir_ in enumerate(self.free_areas_table.baseDirColumn):
            last_dir = base_dir + self.free_areas_table.limitColumn[idx]
            if last_dir == base_dir:
                size = self.free_areas_table.limitColumn[index]
                self.free_areas_table.limitColumn[idx] += size
                self.free_areas_table.remove_element(index)
                done = True
                break

        if done:
            print("Compactando areas libres...")
        else:
            print("No se encontraron áreas contiguas.")

    def update_free_areas_table(self, index, size):
        self.free_areas_table.limitColumn[index] -= size
        self.free_areas_table.baseDirColumn[index] += size

        if self.free_areas_table.limitColumn[index] == 0:
            self.free_areas_table.remove_element(index)

    def request_memory(self, size):
        for index, limit in enumerate(self.free_areas_table.limitColumn):
            if limit >= size:
                return index
        return -1

    def print_tables(self):
        self.partitions_table.print()
        self.free_areas_table.print()
