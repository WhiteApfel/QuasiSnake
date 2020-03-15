import os

os.system("pip install -U --user numpy multiprocessing matplotlib copy")

from map_controller import MapController
from multiprocessing import Process, cpu_count


def start_game():
	MC = MapController(8)
	MC.start_loop()


p = []

for i in range(cpu_count() - 2):
	p.append(Process(target=start_game))
for i in p:
	i.start()
for i in p:
	i.join()
