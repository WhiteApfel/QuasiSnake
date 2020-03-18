from map_controller import MapController
from multiprocessing import Process, cpu_count


def start_game():
	try:
		MC = MapController(8)
		print("Запустилось...")
		MC.start_loop()
	except Exception as e:
		print(e)
		start_game()



p = []

if __name__ == "__main__":
	for i in range(cpu_count() + 2):
		p.append(Process(target=start_game))
	for i in p:
		i.start()
	for i in p:
		i.join()
