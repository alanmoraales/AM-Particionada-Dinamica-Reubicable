from model.Event import Event
from model.EventAdmin import EventAdmin
from model.MemoryAdmin import MemoryAdmin

event_admin = EventAdmin()
event_admin.add_event(Event("LLEGA", "P1", 78))
event_admin.add_event(Event("LLEGA", "P2", 82))
event_admin.add_event(Event("LLEGA", "P3", 60))
event_admin.add_event(Event("LLEGA", "P4", 94))
event_admin.add_event(Event("LLEGA", "P5", 74))
event_admin.add_event(Event("TERMINA", "P3", -1))
event_admin.add_event(Event("LLEGA", "P6", 96))
event_admin.add_event(Event("TERMINA", "P2", -1))
event_admin.add_event(Event("LLEGA", "P7", 74))
event_admin.add_event(Event("TERMINA", "P5", -1))
event_admin.add_event(Event("TERMINA", "P1", -1))
event_admin.add_event(Event("LLEGA", "P8", 44))
event_admin.add_event(Event("LLEGA", "P9", 28))

memory_admin = MemoryAdmin(512, 64, event_admin)