class MainMemory:

    def __init__(self, size):
        self.size = size
        self.free_space = size
        self.partitions_list = []

    def add_partition(self, partition):
        self.partitions_list.append(partition)
